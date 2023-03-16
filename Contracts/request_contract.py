# Here we write the smart contract for creating loan request by borrower api

from pyteal import *

def approval_program():

    # time_check = Cond(
    #     #to check that the request has not expired
    #
    # )
    on_creation = Seq(
        [
            Assert(Txn.application_args.length() == Int(4)),
            App.globalPut(Bytes("title"), Txn.application_args[0]),
            App.globalPut(Bytes("amount"), Txn.application_args[1]),
            App.globalPut(Bytes("loan_end_date"), Txn.application_args[2]),
            App.globalPut(Bytes("interest"), Txn.application_args[3]),
            Return(Int(1))
            # time_check

        ]
    )

    program = Cond(
        [Txn.application_id() == Int(0), on_creation],
        [Txn.on_completion() == OnComplete.NoOp, Approve()],
        [Txn.on_completion() == OnComplete.DeleteApplication, Approve()]

    )

    return program


def clearstate_contract():
    return Approve()