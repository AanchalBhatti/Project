
from algosdk.v2client import algod, indexer

# connection to the algorand network
def algod_conn():
    algod_address = "https://testnet-algorand.api.purestake.io/ps2"
    algod_token = "gqXFTgP7M54pqYRdPxIm14LBaRGynGMO4BodJRoc"
    headers = {"X-API-Key": algod_token}
    conn = algod.AlgodClient(algod_token, algod_address, headers)
    return conn

#  Connection to Algorand Indexer
def connect_indexer():
    algod_indexer = "https://testnet-algorand.api.purestake.io/idx2"
    indexer_token = "K7DgVll3W19DdHA3FTduX4XZTuCvTFf32HXUP5E4"
    headers = {"X-API-Key": indexer_token}
    myindexer = indexer.IndexerClient(indexer_token, algod_indexer, headers)
    return myindexer
