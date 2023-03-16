# Here we deploy and communicate with the smart contract
from algosdk import mnemonic
from algosdk.future.transaction import *
# from utilities.CommonFunctions import get_address_from_application, Today_seconds
# from algodsk import encoding
from Contracts import user_contract, teal
from algosdk.future.transaction import ApplicationCreateTxn, StateSchema, OnComplete

# Declaring the application state storage
local_ints = 0
local_bytes = 0
global_ints = 0
global_bytes = 1   #bcz we only stored one string (i.e. usertype) in global storage
global_schema = StateSchema(global_ints, global_bytes)
local_schema = StateSchema(local_ints, local_bytes)

# This method will generate a new account for both the lender and borrower
# also will generate new user_id for each user that will register

def create_app(client, sender, mnemonic_key, usertype):

    print("Creating user application...")

#   import smart contract for the application
    approval_program = teal.to_teal(user_contract.approval_program())
    clear_program = teal.to_teal(user_contract.clearstate_contract())

    on_complete = OnComplete.NoOpOC.real

    params = client.suggested_params()

    args_list = [bytes(usertype, 'utf8')]

    txn = ApplicationCreateTxn(sender, params, on_complete,
                               approval_program, clear_program,
                               global_schema, local_schema, args_list)

    private_key = mnemonic.to_private_key(mnemonic_key)
    # sign transaction
    signed_txn = txn.sign(private_key)

    # submit transaction
    txid = client.send_transaction(signed_txn)
    print("Signed transaction with txID: {}".format(txid))

    # await confirmation
    wait_for_confirmation(client, txid)
    # displaying results
    transaction_response = client.pending_transaction_info(txid)

    app_id = transaction_response['application-index']
    print(f'Created {usertype} Account: ', app_id)


    return app_id



