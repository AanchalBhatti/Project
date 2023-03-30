# Here we write the smart contract for creating loan request by borrower api
from pyteal import *


def approval_program():

    on_creation = Seq(
        [
            Assert(Txn.application_args.length() == Int(4)),
            App.globalPut(Bytes("title"), Txn.application_args[0]),
            App.globalPut(Bytes("amount"), Txn.application_args[1]),
            App.globalPut(Bytes("loan_end_date"), Txn.application_args[2]),
            App.globalPut(Bytes("interest"), Txn.application_args[3]),
            Return(Int(1))

        ]
    )

    # return_borrowed_amount = inner transaction for payment
    return_borrowed_amount = Seq(
        InnerTxnBuilder.Begin(),

        InnerTxnBuilder.SetFields({
            TxnField.type_enum: TxnType.Payment,
            # sender's account is borrower's address

            # account of the lender's address
            TxnField.receiver: Txn.application_args[2],
            # amount to return
            TxnField.amount: Btoi(Txn.application_args[1]),
            TxnField.fee: Int(0)

        }),

        # submit the transaction
        InnerTxnBuilder.Submit(),
        Approve()
    )

    # PAYMENT
    inner_txn1 = Seq(
        InnerTxnBuilder.Begin(),

        InnerTxnBuilder.SetFields({
            TxnField.type_enum: TxnType.Payment,
            TxnField.sender: 'C6SK43SCCQ22POB7W7N3PAXKGPD3Z34RR5HDLQEU3PQCCY7UYTCGJHNAP4',
            # account of the lender's address
            TxnField.receiver: Txn.application_args[3],
            # amount to lend
            TxnField.amount: Btoi(App.globalGet(Bytes("amount"))),
            TxnField.fee: Int(0)

        }),

        # submit the transaction
        InnerTxnBuilder.Submit(),
        Approve()
    )

    # will assert that lender's amount and global loan amount is same then make payment
    make_payment_to_borrower = Seq(

        Assert(Txn.application_args[2] == App.globalGet(Bytes("amount"))),
        inner_txn1
    )

    # if lender has a counter offer and his counter amount is not equal to global loan amount then just return.. Else make payment
    response_to_lender_acceptance = If(
        And(
            Btoi(Txn.application_args[1]) == Int(1),  # 1 means lender has a counter offer
            Txn.application_args[2] != App.globalGet(Bytes("amount"))
        ), Approve(), make_payment_to_borrower)

    update_loan_request = Seq(
        App.globalPut(Bytes("amount"), Txn.application_args[2]),
        Return(Int(1))
    )

    make_payment_to_borrower_2 = Seq(
        App.globalPut(Bytes("amount"), Txn.application_args[2]),
        inner_txn1
    )

    # If borrower also counter and his counter amount not equal to counter amount of lender then just update the amount of loan request with borrower's new counter amount
    # Else make payment with lender's counter amount (when borrower has accepted the lender's counter amount)
    response_to_borrower_counter = If(
        And(
            Btoi(Txn.application_args[1]) == Int(1),  # 1 means borrower has a counter offer
            Btoi(Txn.application_args[2]) != Btoi(Txn.application_args[5])   # borrower's counter amount should not be equal to lender's last counter amount
        ), update_loan_request, make_payment_to_borrower_2)

    call_transactions = Cond(

        # Condition 1
        # when lender accepts the loan request with either same or counter amount
        [And(
            Txn.application_args.length() == Int(5),
            Txn.application_args[0] == Bytes('Accept by lender')

        ), response_to_lender_acceptance],

        # Condition 2
        # when lender has not accepted the loan amount then borrower replies either with accepting the lender's counter amount or gives own counter amount
        [And(
            Txn.application_args.length() == Int(6),
            Txn.application_args[0] == Bytes('borrower_counter'),

        ), response_to_borrower_counter],

        # Condition 3
        [And(
            Txn.application_args.length() == Int(5),
            Txn.application_args[0] == Bytes('Return borrowed amount'),
            Txn.application_args[2] == Txn.application_args[3]
        ), return_borrowed_amount]

    )

    program = Cond(
        [Txn.application_id() == Int(0), on_creation],
        [Txn.on_completion() == OnComplete.NoOp, call_transactions],
        [Txn.on_completion() == OnComplete.UpdateApplication, Approve()]

    )

    return program

def clearstate_contract():
    return Approve()

# teal_program = compileTeal(approval_program(), Mode.Application, version=5)
#
# # # print the TEAL program
# print(teal_program)
