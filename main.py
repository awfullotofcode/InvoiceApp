from datetime import datetime
import re
import sqlite3
import us

# Setup database connection
conn = sqlite3.connect('test.db')
cursor = conn.cursor()

def main():
    # Main menu create/edit/preview invoice
    menu()

def menu():
    while True:
        menu_action = input("Menu Actions\n[1]CREATE | [2]EDIT\n[3]VIEW   | [4]EXIT\nEnter selection:\n").strip().lower()

        if menu_action in ('c','create','cre','creat','1'):
            # create invoice
            create_invoice()
        elif menu_action in ('edit','edt','eit','2'):
            print("TODO: edit_invoice()")
        elif menu_action in ('view','v','vie','vew','veiw','vw','3'):
            print("TODO: view_invoices()")
        elif menu_action == 'exit':
            exit_program()
            return
        else:
            print("Please enter valid command.")

def create_invoice():
    cursor.execute("BEGIN")

    # Get invoice details and assign a client id for invoice items
    client_id = get_invoice_details()



def get_invoice_details():
    # TODO
    while True:
        # get details
        invoice_details = {
            # Client details
            'name': input("Billing Name: "),
            'street': input("Street address: "),
            'city': input("City: "),
            'state': get_state_abbreviation(input("State: ")) or '',
            'zip': input("Zip: "),
            # Invoice details
            'date': get_date_input("Date (MM-DD-YYYY): "),
            'invoice no': get_invoice_no('Invoice no:'),
            'po': input("PO #: "),
            'sales rep': input("Sales rep: "),
            'project': input("Project name: ")
        }

        preview_invoice_details(invoice_details)

        if invoice_details_confirmed():
            # submit into db and get client id
            # Check if the client already exists
            existing_client = check_if_client_exists(invoice_details)

            if existing_client:
                return existing_client[0] # Returns existing client id
            else:
                try:
                    client_id = insert_new_client()
                    return client_id

                except sqlite3.Error as e:
                    print(f"An error occurred: {e}")
                    conn.rollback()

def preview_invoice_details(invoice_details):
    #TODO
    print("____________________")
    print("Please review the following details:")
    for key, value in invoice_details.items():
        print(f"{key.capitalize()}: {value}")
    return

def get_client_id():
    return

def invoice_details_confirmed():
    
    while True:
        confirm_details = input("Does this information look correct? Y/N: ").strip().lower()

        if confirm_details in ('y','yes','yea','yee','yeah','ya','ye'):
            print("Invoice details confirmed.")
            return True
        elif confirm_details in ('no','nah','na','n'):
            print("Re-enter details below.")
            return False
        else:
            print("Enter Y or N.")

def check_if_client_exists(invoice_details):
    cursor.execute("""
        SELECT id FROM clients WHERE name = ? AND street = ? AND city = ? AND state = ? AND zip = ?
    """, (
        invoice_details['name'],
        invoice_details['street'],
        invoice_details['city'],
        invoice_details['state'],
        invoice_details['zip']
    ))
    existing_client = cursor.fetchone()
    return existing_client

def insert_new_client(invoice_details):
    cursor.execute("""
        INSERT INTO clients (name, street, city, state, zip) VALUES (?,?,?,?,?)
    """, (
        invoice_details['name'],
        invoice_details['street'],
        invoice_details['city'],
        invoice_details['state'],
        invoice_details['zip']
    ))

    client_id = cursor.lastrowid
    return client_id


def exit_program():
    while True:
        save_changes = input("Save changes? Y/N: ").strip().lower()

        if save_changes in ('y','yes','yea','yee','yeah','ya','ye'):
            print("Changes saved.\nTODO: save_changes()")
            conn.commit()
            conn.close()
            return
        elif save_changes in ('no','nah','na','n'):
            print("Exiting program.")
            conn.rollback()
            conn.close()
            return
        else:
            print("Enter Y or N.")


# Data validation and formatting functions
def get_state_abbreviation(state_input):
    state = us.states.lookup(state_input)
    if state:
        return state.abbr
    else:
        # Check if input is already an abbreviation
        state = us.states.lookup(state_input.upper())
        if state:
            return state.abbr
        else:
            return None
        
def get_date_input(prompt):
    date_formats = ['%m%d%Y', '%m/%d/%Y', '%m-%d-%Y']
    
    while True:
        date_str = input(prompt).strip()
        
        # Use today's date if no input is given
        if not date_str:
            date_obj = datetime.now()
            return date_obj.strftime('%Y-%m-%d')
        
        for date_format in date_formats:
            try:
                # Attempt to parse the date string
                date_obj = datetime.strptime(date_str, date_format)
                # Format the date in SQL format YYYY-MM-DD
                return date_obj.strftime('%Y-%m-%d')
            except ValueError:
                # Continue to try other formats if parsing fails
                continue
        
        # If none of the formats match, prompt the user again
        print("Invalid date format. Please use MMDDYYYY, MM/DD/YYYY, or MM-DD-YYYY.")

def get_invoice_no(prompt):
    invoice_no_input = input(prompt)

    if invoice_no_input.isdigit():
        return invoice_no_input
    elif invoice_no_input == '':
        DEFAULT_INVOICE_NO = 9999
        invoice_no_input = DEFAULT_INVOICE_NO
        return invoice_no_input
    else:
        print("Invalid number, invoice number updated to 9999")

        
main()