from algosdk import encoding
from pyteal import *
import API.connection

# define the algod client
algod_client = API.connection.algod_conn()

# convert pyteal to teal
def to_teal(smart_contract):

    # First convert the Pyteal to TEAL
    teal_trade = compileTeal(smart_contract, Mode.Application, version=6)

    # Next compile our TEAL to algorand bytecode. (its' returned base64)
    b64_trade = algod_client.compile(teal_trade)['result']

    # Lastly decode the base64
    prog_trade = encoding.base64.b64decode(b64_trade)

    return prog_trade

