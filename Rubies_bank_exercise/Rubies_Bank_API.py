from flask import Flask, request, jsonify


app = Flask(__name__)

""" 
      intialized the list of customers details 
      and also include a new key "Transaction_History",
      which value is a list that store the transactions.
"""

customers = [
              {"Customer_name": "Chinua Achebe", "Account_Balance": 5000.00, "Password": "firetrees", "Account_Number": "1002345678", "Transaction_History": [{"Opening_Bal": 5000}]},
              {"Customer_name": "Wole Soyinka", "Account_Balance": 2500.75, "Password": "kongiharvest", "Account_Number": "2005678910", "Transaction_History": [{"Opening_Bal": 2500.75}]}, 
              {"Customer_name": "Chimamanda Ngozi Adichie", "Account_Balance": 3871.25, "Password": "halfofayellowsun", "Account_Number": "3008912345", "Transaction_History": [{"Opening_Bal": 3871.25}]}, 
              {"Customer_name": "Ahamefula Achebe", "Account_Balance": 1298.50, "Password": "thingsfall", "Account_Number": "4001234567", "Transaction_History": [{"Opening_Bal": 1298.5}]}, 
              {"Customer_name": "Ngozi Okonjo-Iweala", "Account_Balance": 7542.00, "Password": "okonjonomics", "Account_Number": "5004567890", "Transaction_History": [{"Opening_Bal": 7542}]}, 
              {"Customer_name": "Ben Okri", "Account_Balance": 987.65, "Password": "invisiblecity", "Account_Number": "6007890123", "Transaction_History": [{"Opening_Bal": 987.65}]}, 
              {"Customer_name": "Adichie Ozumba", "Account_Balance": 2154.90, "Password": "purplehibiscus", "Account_Number": "7001123456", "Transaction_History": [{"Opening_Bal": 2154.9}]}, 
              {"Customer_name": "Fela Kuti", "Account_Balance": 4328.10, "Password": "afrobeat", "Account_Number": "8004456789", "Transaction_History": [{"Opening_Bal": 4328.1}]}, 
              {"Customer_name": "John Amaechi", "Account_Balance": 6789.50, "Password": "celtics", "Account_Number": "9007789012", "Transaction_History": [{"Opening_Bal": 6789.5}]},
              {"Customer_name": "Asa", "Account_Balance": 1592.35, "Password": "jata", "Account_Number": "1001012345", "Transaction_History": [{"Opening_Bal": 1592.35}]}
              ]


@app.route("/check-balance")
def check_balance():
    """
    This function returns the account balance of the customer

    Parameters:
    account_number (str): Account number of customer
    password (str): Password of customer

    Returns:
    reply (str): Account balance of customer or error message
    """

    # Extract JSON data from request
    data = request.get_json()

    # Get the variables
    account_number = request.args.get('account_number')
    password = request.args.get('password')

    reply = ""  # Initialize the response string
    name = ""

    # Loop through all customers to find the matching account number
    for customer in customers:
        # Check if this is the right customer based on account number
        if customer["Account_Number"] == account_number:
            name = customer["Customer_name"]
            print(f"\nDear {name} ")
            # If account number matches, verify password
            if customer["Password"] == password:
                # If password matches, return account balance
                reply = "Account Balance is " + str(customer["Account_Balance"])
            else:
                # If password is incorrect
                reply = "Password Incorrect: Kindly confirm the entered password"
            break  # Exit loop once account is found
        else:
            # If account number is not found
            reply = "Account not Found: Kindly Confirm Account Number"

    return jsonify({"user": name, "message": reply}), 200


@app.route("/withdraw-cash", methods=['POST'])
def withdraw_cash():
    """
    This function allows a customer to withdraw a specified amount

    Parameters:
    account_number (str): Account number of customer
    password (str): Password of customer
    amount (float): Amount to withdraw

    Returns:
    reply (str): Withdrawal confirmation or error message
    """
    data = request.get_json()

    # Get the variables
    account_number = data.get('account_number')
    password = data.get('password')
    amount = data.get("amount")

    reply = ""  # Initialize reply message
    name = ""

    for customer in customers:
        # Check if account number matches
        if customer["Account_Number"] == account_number:
            name = customer["Customer_name"]
            print(f"\nDear {name}")
            # Check if password is correct
            if customer["Password"] == password:
                # Check if balance is sufficient for withdrawal
                if customer["Account_Balance"] > amount:
                    # Deduct the amount
                    customer["Account_Balance"] -= amount
                    # Log the transaction
                    customer["Transaction_History"].append({"withdrawal": amount})
                    reply = f"The Sum of #{amount} has been withdrawn"
                else:
                    # Insufficient funds
                    reply = "Insufficient funds: Kindly deposit funds to perform transaction"
            else:
                # If Password is incorrect
                reply = "Password Incorrect: Kindly confirm the entered password"
            break  # Exit loop
        else:
            # If account number not found
            reply = "Account not Found: Kindly Confirm Account Number"

    return jsonify({"user": name,"message": reply}), 200


@app.route("/deposit-cash", methods=['POST'])
def deposit_cash():
    """
    This function deposits a specified amount into the customer's account

    Parameters:
    account_number (str): Account number of customer
    password (str): Password of customer
    amount (float): Amount to deposit

    Returns:
    reply (str): Deposit confirmation or error message
    """
    data = request.get_json()

    # Get the variables
    account_number = data.get('account_number')
    password = data.get('password')
    amount = data.get("amount")

    reply = ""  # Initialize response message
    name = ""

    for customer in customers:
        # Match account number
        if customer["Account_Number"] == account_number:
            name = customer["Customer_name"]
            print(f"\nDear {name} ")
            # Verify password
            if customer["Password"] == password:
                # Add deposit to balance
                customer["Account_Balance"] += amount
                # Log the transaction
                customer["Transaction_History"].append({"deposit": amount})
                reply = f"The Sum of #{amount} has been Deposited"
            else:
                # Incorrect password
                reply = "Password Incorrect: Kindly confirm the entered password"
            break  # Exit loop
        else:
            # Account not found
            reply = "Account not Found: Kindly Confirm Account Number"

    return jsonify({"user": name,"message": reply}), 200

@app.route("/change-password", methods=["POST"])
def change_password():
    """
    This function updates the customer's password

    Parameters:
    account_number (str): Account number of customer
    password (str): Current password of customer
    new_password (str): New password to set

    Returns:
    reply (str): Password update confirmation or error message
    """
    data = request.get_json()

    # Get the variables
    account_number = data.get('account_number')
    password = data.get('password')
    new_password = data.get("new_password")

    reply = ""  # Initialize response message
    name = ""

    for customer in customers:
        # Find matching account
        if customer["Account_Number"] == account_number:
            name = customer["Customer_name"]
            print(f"\nDear {name} ")
            # Confirm password
            if customer["Password"] == password:
                # Update to new password
                customer["Password"] = new_password
                reply = "Password had been updated"
            else:
                # if password is incorrect
                reply = "Password Incorrect: Kindly confirm the entered password"
            break  # Exit loop
        else:
            # Account number not found
            reply = "Account not Found: Kindly Confirm Account Number"

    return jsonify({"user": name,"message": reply}), 200

@app.route("/delete-account", methods=["POST"])
def delete_account():
    """
    This function deletes a customer's account after password and confirmation

    Parameters:
    account_number (str): Account number of customer
    password (str): Password of customer

    Returns:
    reply (str): Deletion confirmation or error message
    """
    data = request.get_json()

    # Get the variables
    account_number = data.get('account_number')
    password = data.get('password')

    reply = ""  # Response message
    index = 0   # Keep track of current index for deletion
    name = ""

    for customer in customers:
        # Check for matching account
        if customer["Account_Number"] == account_number:
            name = customer["Customer_name"]
            print(f"\nDear {name} ")
            # Check password
            if customer["Password"] == password:
                # Ask user to confirm deletion
                confirmation = "y"
                if confirmation.lower() == "y":
                    # Delete account
                    del customers[index]
                    reply = "Account deleted Successfully"
                else:
                    # Deletion cancelled
                    reply = "Account not deleted"
            else:
                # Wrong password
                reply = "Password Incorrect: Kindly confirm the entered password"
            break
        else:
            # if account not  found
            reply = "Account not Found: Kindly Confirm Account Number"
        index += 1  # Increment index for deletion reference

    return jsonify({"user": name,"message": reply}), 200

@app.route("/transaction-history")
def transaction_history():
    """
    This function displays and summarizes a customer's transaction history

    Parameters:
    account_number (str): Account number of customer
    password (str): Password of customer

    Returns:
    reply (str): Summary of deposits and withdrawals or error message
    """
    #retrieve args
    account_number = request.args.get('account_number')
    password = request.args.get('password')

    name = ""
    reply = ""  # Initialize message
    withdrawal = 0  # total withdrawals
    deposited = 0   # total deposits

    for customer in customers:
        # Locate customer
        if customer["Account_Number"] == account_number:
            name = customer["Customer_name"]
            print(f"\nDear {name} ")
            # confirm password
            if customer["Password"] == password:
                # Display transaction headers
                print(f"Description                         |                   Value")
                print(f"-------------------------------------------------------------")

                # Loop through transaction history
                for record in customer["Transaction_History"]:
                  for key, value in record.items():
                    # description = history.split()[0]  # gets description
                    # value = float(history.split()[1])   # gets numeric value of transaction

                    # Sum totals
                    if key == "withdrawal": #if withdrawal increase withdrawal sum total
                        withdrawal += value
                    elif key == "deposit": #if deposited increase deposited sum total
                        deposited += value

                    # Print transaction
                    print(f"{key}                         |                   {value}")

                # Print current balance
                value = customer["Account_Balance"]
                print(f"Current_Bal                         |                   {value}")

                # Create summary string
                return jsonify({"user": name,
                                "transaction_history": customer["Transaction_History"] + [{"Current_Bal": value}],
                                "total_withdrawal": withdrawal,
                                "total_deposited": deposited}), 200
            else:
                # Incorrect passwordc
                reply = "Password Incorrect: Kindly confirm the entered password"
            break
        else:
            # Account number not found
            reply = "Account not Found: Kindly Confirm Account Number"

    return reply




if __name__ == "__main__":
  app.run(debug=True)