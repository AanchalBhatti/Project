# Check the user type.

user_type_list = ["lender", "borrower"]

def check_user(user_type):
    if user_type in user_type_list:
        return "Approved"
    else:
        return "Error: Wrong user type."
