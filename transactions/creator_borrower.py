from algosdk.future.transaction import *
from algosdk import mnemonic
import API.connection
from Contracts import request_contract, teal

# Declare application state storage(immutable)

local_ints = 0
local_bytes = 0
global_ints = 2
global_bytes = 2
global_schema = StateSchema(global_ints, global_bytes)
local_schema = StateSchema(local_ints, local_bytes)

# connecting to algorand client
algod_client = API.connection.algod_conn()

def create_request_app(client, mnemonic_keys, borrower_app_id, title, amount, maturity_date, roi):

    # define the sender for the transactions
    print(f'Creating Loan Request by {borrower_app_id}...')
    private_key = mnemonic.to_private_key(mnemonic_keys)
    sender = account.address_from_private_key(private_key)

#     importing smart contract for the application
    approval_program_request = teal.to_teal(request_contract.approval_program())
    clear_program = teal.to_teal(request_contract.clearstate_contract())


    on_complete = OnComplete.NoOpOC.real  #telling transaction to do nothng after completion of the execution of lohgic (means just create the request and do nothing after that)
    params = client.suggested_params()


#     create request application
    args_list = [bytes(title, 'utf8'), int(amount), bytes(maturity_date, 'utf8'), int(roi)]
    txn = ApplicationCreateTxn(sender=sender, sp=params, on_complete=on_complete,
                               approval_program=approval_program_request, clear_program=clear_program,
                               global_schema=global_schema, local_schema=local_schema, app_args=args_list,
                               note="Loan Request Creation")

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
    print(txid)


    return app_id



