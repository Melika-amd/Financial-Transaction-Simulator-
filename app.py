from flask import Flask, jsonify, request, render_template, send_file
from flask_bootstrap import Bootstrap
from transactions import generate_users, generate_transactions_with_risk, export_transactions_to_csv
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
    new_transaction = {
        "Sender": data["Sender"],
        "Receiver": data["Receiver"],
        "Type": data["Type"],
        "Amount": float(data["Amount"]),
        "Timestamp": data["Timestamp"],
        "IsFraud": data["IsFraud"],
        "RiskScore": data["RiskScore"]
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
    # Generate new transactions each time
    transactions_df = generate_transactions_with_risk(users)
    transactions = transactions_df.to_dict(orient="records")
    return jsonify(transactions)

@app.route('/export-csv')
def export_csv():
    # Generate transactions
    users = generate_users(5)
    transactions = generate_transactions_with_risk(users, 20)
    
    # Create a temporary file
    temp_dir = tempfile.gettempdir()
    temp_file = os.path.join(temp_dir, 'transactions_export.csv')
    
    # Export to CSV
    export_transactions_to_csv(transactions, temp_file)
    
    # Send file to user
    return send_file(
        temp_file,
        mimetype='text/csv',
        as_attachment=True,
        download_name='transactions_export.csv'
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
