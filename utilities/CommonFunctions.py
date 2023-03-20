from API import connection
import time, datetime
from algosdk import encoding

# connect to indexer
myindexer = connection.connect_indexer()
algodclient = connection.algod_conn()

def check_balance(wallet_address, amt):
    acc_info = algodclient.account_info(wallet_address)
    locked_bal = acc_info['min-balance']
    balance = acc_info['amount']
    available_balance = balance - locked_bal

    if balance >= amt and available_balance > amt:
        return True
    else:
        return False


# get today second in epoch time
def Today_seconds():
    today_time = time.localtime()
    # print(today_time)
    seconds_today_time = time.mktime(today_time)
    today_seconds = int(seconds_today_time)
    return today_seconds


# convert the maturity date to unix timestamp
def convert_to_unix_timestamp(date_str):
    # Convert date string to datetime object
    date_obj = datetime.datetime.strptime(date_str, '%Y-%m-%d')

    # Convert datetime object to Unix timestamp
    unix_timestamp = int(time.mktime(date_obj.timetuple()))
    # print(unix_timestamp)
    return unix_timestamp


# gets the address from the application
def get_address_from_application(app_id):
    # Get the creator address of the application
    response = myindexer.applications(app_id)
    account_address = response['application']['params']['creator']
    return account_address

# gets the address from the txid
def get_address_from_txid(tx_id):

    print('hii')
    # Get the creator address of the application
    tx_info = myindexer.search_transactions(txid=tx_id)
    print(tx_info)
    sender_pk = tx_info["transactions"][0]["sender"]
    print(sender_pk)
    # sender_address = encoding.encode_address(sender_pk)

    # response = myindexer.applications(app_id)
    # account_address = response['application']['params']['creator']
    return sender_pk

