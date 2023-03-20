from algosdk.future.transaction import *
from algosdk import mnemonic
import API.connection

from utilities.CommonFunctions import get_address_from_application, Today_seconds, convert_to_unix_timestamp, get_address_from_txid

# connecting to algorand client
algod_client = API.connection.algod_conn()

def accept_request_app(client, sender, lender_mnemonic_key,  lender_app_id, request_app_id, amount):

    # define the sender for the transactions
    print(f'Request : {request_app_id} accepted by {lender_app_id}...')
    private_key = mnemonic.to_private_key(lender_mnemonic_key)

    borrower_address = get_address_from_application(request_app_id)

    # set suggested params for transaction
    params = client.suggested_params()
    params.fee = 1000
    params.flat_fee = constants.MIN_TXN_FEE

    txn = PaymentTxn(sender=sender, receiver=borrower_address, amt=amount, sp=params)
    # sign transaction
    signed_txn = txn.sign(private_key)

    # submit transaction
    txid = algod_client.send_transaction(signed_txn)
    print("Signed transaction with txID: {}".format(txid))
    # print(int(Today_seconds()))

    print(txid)
    # NOTE: payment transaction does not have an application id
    return txid



def return_by_borrower(client, sender, mnemonic_key, lender_address, request_app_id, accept_request_txn_id, amount, roi, maturity_date):
    private_key = mnemonic.to_private_key(mnemonic_key)
    params = client.suggested_params()
    params.fee = 1000
    params.flat_fee = constants.MIN_TXN_FEE
    amount = ((roi/100)*amount) + amount
    amount = int(amount)

    # deriving lender address who accepted the request from accept_request_app_id
    derived_lender_address = get_address_from_txid(accept_request_txn_id)


    if int(Today_seconds()) >= int(convert_to_unix_timestamp(maturity_date)) and lender_address == derived_lender_address:

        try:
            # define the sender for the transactions
            print(f'Returning the borrowed amount for Request Id :{request_app_id}')



            # UNCOMMENT THE NEXT TWO LINES FOR CONNECTING TO SMART CONTRACT

            # args_list = ["Return borrowed amount", int(amount), lender_address, derived_lender_address]
            # txn2 = ApplicationNoOpTxn(sender=sender, sp=params, index=request_app_id, app_args=args_list)

            print("creating transaction object....")
            txn2 = PaymentTxn(sender=sender, receiver=lender_address, amt=amount, sp=params)

            print("Signing Transaction...")
            signed_txn = txn2.sign(private_key)

            # submit transaction
            txid2 = algod_client.send_transaction(signed_txn)
            print("Signed transaction with txID: {}".format(txid2))

            # await confirmation
            wait_for_confirmation(client, txid2)

            # display the results
            client.pending_transaction_info(txid2)

            return txid2

        except Exception as error:

            error_msg = {"message": str(error)}
            return error_msg

    else:
        return ({'message': "Maturity date has not yet arrived"})




