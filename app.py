from flask import Flask, jsonify, request, render_template, send_file, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from transactions import generate_users, generate_transactions_with_risk, export_transactions_to_csv
from datetime import datetime
from utils import calculate_risk_score
import tempfile
import os

app = Flask(__name__)
Bootstrap(app)
users = generate_users()
transactions_df = generate_transactions_with_risk(users)

@app.route("/api/transactions", methods=["GET"])
def get_transactions_api():
    return jsonify(transactions_df.to_dict(orient="records"))

@app.route("/api/transaction", methods=["POST"])
def add_transaction():
    data = request.json
    
    risk_score = calculate_risk_score(data["Amount"], data["Type"])
    
    new_transaction = {
        "Sender": data["Sender"],
        "Receiver": data["Receiver"],
        "Type": data["Type"],
        "Amount": float(data["Amount"]),
        "Timestamp": datetime.now().isoformat(),
        "IsFraud": False,
        "RiskScore": risk_score
    }
    
    global transactions_df
    transactions_df = transactions_df.append(new_transaction, ignore_index=True)
    return jsonify({"message": "Transaction added successfully"}), 201

@app.route("/")
def dashboard():
    return render_template("dashboard.html", transactions=transactions_df.to_dict(orient="records"))

@app.route('/refresh-transactions')
def get_transactions():
    global transactions_df, users
    transactions_df = generate_transactions_with_risk(users)
    transactions = transactions_df.to_dict(orient="records")
    return jsonify(transactions)

@app.route('/export-csv')
def export_csv():
    global transactions_df
    
    try:
        temp_dir = tempfile.gettempdir()
        temp_file = os.path.join(temp_dir, 'transactions_export.csv')
        
        transactions_df.to_csv(temp_file, index=False)
        
        response = send_file(
            temp_file,
            mimetype='text/csv',
            as_attachment=True,
            download_name='transactions_export.csv'
        )
        
        response.headers["Cache-Control"] = "no-cache"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
        response.headers['Cache-Control'] = 'public, max-age=0'
        
        return response
        
    except Exception as e:
        print(f"Error exporting CSV: {str(e)}")
        return jsonify({"error": "Failed to export CSV"}), 500

@app.route("/create-transaction", methods=["POST"])
def create_transaction():
    try:
        sender = request.form.get("sender")
        receiver = request.form.get("receiver")
        amount = float(request.form.get("amount"))
        trans_type = request.form.get("type")
        
        risk_score = calculate_risk_score(amount, trans_type)
        
        new_transaction = {
            "Sender": sender,
            "Receiver": receiver,
            "Type": trans_type,
            "Amount": amount,
            "Timestamp": datetime.now().isoformat(),
            "IsFraud": False,
            "RiskScore": risk_score
        }
        
        global transactions_df
        transactions_df = transactions_df.append(new_transaction, ignore_index=True)
        
        return redirect(url_for('dashboard'))
        
    except Exception as e:
        print(f"Error creating transaction: {str(e)}")
        return jsonify({"error": "Failed to create transaction"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
