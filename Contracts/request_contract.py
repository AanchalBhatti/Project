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

    # return_borrowed_amount = inner transaction for payment
    return_borrowed_amount = Seq(
        InnerTxnBuilder.Begin(),

        InnerTxnBuilder.SetFields({
            TxnField.type_enum: TxnType.Payment,
            # account of the lender's address
            TxnField.receiver: Txn.application_args[2],
            # amount to return
            TxnField.amount: Btoi(Txn.application_args[1]),
            TxnField.fee: Int(0)

        }),

        #submit the transaction
        InnerTxnBuilder.Submit(),
        Approve()
    )

    call_transactions = Cond(

        [And(
            Txn.application_args[0] == Bytes('Return borrowed amount'),
            Assert(Txn.application_args[2] == Txn.application_args[3])
        ), return_borrowed_amount]

    )

    program = Cond(
        [Txn.application_id() == Int(0), on_creation],
        [Txn.on_completion() == OnComplete.NoOp, call_transactions],
        [Txn.on_completion() == OnComplete.DeleteApplication, Approve()]

    )

    return program


def clearstate_contract():
    return Approve()