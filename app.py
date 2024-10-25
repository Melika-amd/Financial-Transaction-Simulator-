from flask import Flask, jsonify, request, render_template
from flask_bootstrap import Bootstrap
from transactions import generate_users, generate_transactions_with_risk

app = Flask(__name__)
Bootstrap(app)
users = generate_users()
transactions_df = generate_transactions_with_risk(users)

@app.route("/api/transactions", methods=["GET"])
def get_transactions():
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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
