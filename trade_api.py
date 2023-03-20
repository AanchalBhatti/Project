from flask import Flask, request, jsonify
from flask_cors import CORS
from API import connection

from utilities import check, CommonFunctions
from transactions import create_account_module, creator_borrower, creator_lender

app = Flask(__name__)
cors = CORS(app, resources={
    r"/*": {"origin": "*"}
})

# setting up the connection with algorand client
algod_client = connection.algod_conn()

@app.route('/create_account', methods=["POST"])
def create_account():
    try:
        user_details = request.get_json()
        address = user_details['wallet_address']
        mnemonic_key = user_details['mnemonic_key']
        usertype = user_details['user_type']

    except Exception as error:
        return jsonify({'message': f'Payload Error! Key Missing: {error}'}), 500

#     check details of the user
    user_type = check.check_user(usertype)
    if user_type == "Approved":
        try:
            if CommonFunctions.check_balance(address, 1000):

                 #give the user id for the user
                try:

                    usertxn = create_account_module.create_app(algod_client, address,mnemonic_key, usertype)
                    return jsonify(usertxn), 200

                except Exception as error:
                    return jsonify({"message": str(error)}), 500

                #if there was not required balance in the account
            else:
                error_msg = {"message:" "For Account Creation, Minimum Balance should be 1000 MicroAlgos " }
                return jsonify(error_msg), 400

        except Exception as wallet_error:
            error_msg = {"message" : "Wallet Error!" + str(wallet_error)}
            return jsonify(error_msg), 400

    #else the user was not approved
    else:
        error_msg = {"message" : "wrong user type"}
        return jsonify(error_msg), 400

# creating loan request from the borrower
@app.route('/create_request', methods=["POST"])
def create_request():
    try:
        #getting the details of the request from the borrower
        request_details = request.get_json()
        address = request_details['create_wallet_address']
        mnemonic_keys = request_details['mnemonic_keys']
        borrower_app_id = request_details['borrower_app_id']

        #request details
        title = request_details['title']
        amount = request_details['amount']
        maturity_date = request_details['maturity_date']
        roi = request_details['roi']

    except Exception as error:
        return jsonify({'message': f'Payload Error! Key Missing: {error}'}), 500

    try:
        if CommonFunctions.check_balance(address, 3000):

            try:

                requestID_txn = creator_borrower.create_request_app(algod_client, mnemonic_keys, borrower_app_id, title, amount, maturity_date, roi)
                print(requestID_txn)
                return jsonify(requestID_txn), 200
            except Exception as error:

                error_msg = {"message": str(error)}
                return jsonify(error_msg), 500

        else:
            error_msg = {"message": "To create a request, Minimum Balance should be 3000 microAlgos"}
            return jsonify(error_msg), 400
    except Exception as wallet_error:
        error_msg = {"message": str(wallet_error)}
        return jsonify(error_msg), 400


# creating loan request from the borrower
@app.route('/accept_request', methods=["POST"])
def accept_request():
    try:
        #getting the details of lender who accepted the request
        request_details = request.get_json()
        address = request_details['wallet_address']
        lender_app_id = request_details['lender_app_id']
        request_app_id = request_details['request_app_id']
        amount = request_details['amount']
        lender_mnemonic_key = request_details['lender_mnemonic_key']

    except Exception as error:
        return jsonify({'message': f'Payload Error! Key Missing: {error}'}), 500

    try:
        if CommonFunctions.check_balance(address, 3000):

            try:

                requestID_txn = creator_lender.accept_request_app(algod_client, address, lender_mnemonic_key,
                                                                  lender_app_id, request_app_id, amount)

                print(requestID_txn)
                return jsonify(requestID_txn), 200
            except Exception as error:

                error_msg = {"message": str(error)}
                return jsonify(error_msg), 500

        else:
            error_msg = {"message": "To create a request, Minimum Balance should be 3000 microAlgos"}
            return jsonify(error_msg), 400
    except Exception as wallet_error:
        error_msg = {"message": str(wallet_error)}
        return jsonify(error_msg), 400

# creating loan request from the borrower
@app.route('/return_payment', methods=["POST"])
def return_payment():
    try:
        #getting the details of lender who accepted the request
        request_details = request.get_json()
        address = request_details['wallet_address']
        mnemonic_key = request_details['mnemonic_key']
        amount = request_details['amount']
        lender_address = request_details['lender_address']
        request_app_id = request_details['request_app_id']
        accept_request_aap_id = request_details['accept_request_aap_id']
        print('a')
        roi = request_details['roi']
        maturity_date = request_details['maturity_date']

    except Exception as error:
        return jsonify({'message': f'Payload Error! Key Missing: {error}'}), 500

    try:
        if CommonFunctions.check_balance(address, 3000):

            try:

                requestID_txn = creator_lender.return_by_borrower(algod_client, address, mnemonic_key,
                                                                  lender_address, request_app_id, accept_request_aap_id, amount, roi, maturity_date)


                print(requestID_txn)
                return jsonify(requestID_txn), 200
            except Exception as error:

                error_msg = {"message": str(error)}
                return jsonify(error_msg), 500

        else:
            error_msg = {"message": "To create a request, Minimum Balance should be 3000 microAlgos"}
            return jsonify(error_msg), 400
    except Exception as wallet_error:
        error_msg = {"message": str(wallet_error)}
        return jsonify(error_msg), 400

# running the API
if __name__ == "__main__":
    app.run()