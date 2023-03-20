from pyteal import *
from Contracts.teal import to_teal

def return_payment():

    call_transactions = Cond(

        [And(
            Txn.application_args[0] == Bytes('Return borrowed amount')

        )]

    )

    program = Cond(
        [Txn.on_completion() == OnComplete.NoOp, call_transactions]
    )