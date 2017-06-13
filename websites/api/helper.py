def is_int(val):
    try:
        a = int(val)
        return True
    except ValueError:
        return False

def is_empty(val):
    if bool(val):
        return False
    else:
        return True
        
def check_id_valid(id):
    error = ""
    if is_empty(id):
        error = "This field is required"
    elif not is_int(id):
        error = "This value must be is integer."

    return error

def get_card_status(card_status_code, reissued_to_card): 
    card_status_text = ""
    if card_status_code == 0:
        card_status_text = "Active"
    elif card_status_code == 2 and not reissued_to_card:
        card_status_text = "Suspended"
    elif card_status_code == 2 and reissued_to_card:
        card_status_text = "Reissued"
    return card_status_text
