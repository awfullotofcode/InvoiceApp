from datetime import datetime
import re
import sqlite3
import sys
import us

# Setup database connection
conn = sqlite3.connect('test.db')
cursor = conn.cursor()

invoice_details = {}
invoice_items = []

def main():
    # Main menu create/edit/preview invoice
    try:
        menu()
    finally:
        conn.commit()
        conn.close()

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
            sys.exit()
        else:
            print("Please enter valid command.")

# Main menu functions
def create_invoice():
    global invoice_details
    global invoice_items

    # reset invoice details and items for new entry
    invoice_details = {}
    invoice_items = []

    get_invoice_details()
    get_invoice_items()
    current_invoice_actions()


def current_invoice_actions():
    print("____________________")
    while True:
        display_invoice()
        menu_action = input("[1]SAVE | [2]EDIT\n[3]PRINT| [4]EXIT\n[5]RETURN TO MENU ->\nSelect: ").strip().lower()

        if menu_action in ('save','sve','sae','s','1'):
            # save_invoice()
            save_invoice()
        elif menu_action in ('edit','edt','eit','2'):
            print("TODO: edit_invoice()")
        elif menu_action in ('print','pirnt','prnt','pint','p','3'):
            # TODO
            return
        elif menu_action in ('menu','men','meu','m','rtm','return to menu','r','5'):
            print("menu()")
            menu()
        elif menu_action == 'exit' or menu_action == '4':
            while True:
                confirm_details = input("Save invoice? Y/N: ").strip().lower()

                if confirm_details in ('y','yes','yea','yee','yeah','ya','ye'):
                    save_invoice()
                    sys.exit()
                elif confirm_details in ('no','nah','na','n'):
                    print("Invoice discarded.\nClosing program...\nProgram closed.")
                    sys.exit()
                else:
                    print("Enter Y or N.")  
        else:
            print("Please enter valid command.")   

def get_invoice_details():
    global invoice_details
    while True:
        # Collect and update invoice details
        invoice_details['name'] = input("Billing Name: ")
        invoice_details['street'] = input("Street address: ")
        invoice_details['city'] = input("City: ")
        invoice_details['state'] = get_state_abbreviation(input("State: ")) or ''
        invoice_details['zip'] = input("Zip: ")
        invoice_details['po'] = input("PO #: ")
        invoice_details['date'] = get_date_input("Date (MM-DD-YYYY): ")
        invoice_details['invoice no'] = get_invoice_no('Invoice no:')
        invoice_details['sales rep'] = input("Sales rep: ")
        invoice_details['project'] = input("Project name: ")

        preview_invoice_details()

        if details_confirmed():
            return

def preview_invoice_details():
    #TODO
    print("____________________")
    print("Please review the following details:")
    for key, value in invoice_details.items():
        print(f"{key.capitalize()}: {value}")
    return

def get_invoice_items():
    global invoice_items
    while True:
        item = {
            'name': input("Item name: "),
            'description': input("Description: "),
            'quantity': get_quantity_input("Quantity: "),
            'usd': get_usd_amount_input("Price(USD): ")
        }

        preview_invoice_item(item)
        
        if details_confirmed():
            while True:
                add_item_response = input("Add another item? Y/N:  ").lower()
                if add_item_response in ('no','nah','na','n'):
                    invoice_items.append(item)
                    return
                elif add_item_response in ('yeah','yes','yea','ya','y'):
                    invoice_items.append(item)
                    break
                else:
                    print("please enter Y/N")

def preview_invoice_item(item):
    print("____________________")
    print("Please review the following:")
    for key, value in item.items():
        if key == 'usd':
            value = f"${value:,.2f}"
        print(f"{key.capitalize()}: {value}")

def display_invoice(invoice_details=None, invoice_items=None):
    # Use global variables if no arguments are provided
    if invoice_details is None:
        invoice_details = globals().get('invoice_details', {})
    if invoice_items is None:
        invoice_items = globals().get('invoice_items', [])
    # Print invoice billing details
    print(f"____________________")
    print(f"Bill to:\n{invoice_details['name']}\n{invoice_details['street']}")
    print(f"{invoice_details['city']} {invoice_details['state']}  {invoice_details['zip']}")
    if invoice_details['po'] != '':
        print(f"{invoice_details['po']}")
    print(f"--------------------")
    # Print invoice details
    print(f"{invoice_details['date']} | {invoice_details['invoice no']}")
    print(f"--------------------")
    print(f"Sales Rep: {invoice_details['sales rep']}")
    print(f"--------------------")
    print(f"{invoice_details['project']}")
    print(f"____________________")
    # Print invoice items
        # Print invoice items
    print("  INVOICE ITEMS   ")
    for idx, item in enumerate(invoice_items, start=1):
        print(f"Item {idx}:")
        for key, value in item.items():
            if key == 'usd':
                value = f"${value:,.2f}"
            print(f"  {key.capitalize()}: {value}")
        print("____________________")
    return

def save_invoice():
    # Start a transaction
    try:
        # Check if the client already exists
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

        if existing_client:
            # Client exists, use existing client ID
            client_id = existing_client[0]
        else:
            # Insert into clients table
            cursor.execute("""
                INSERT INTO clients (name, street, city, state, zip)
                VALUES (?, ?, ?, ?, ?)
            """, (
                invoice_details['name'],
                invoice_details['street'],
                invoice_details['city'],
                invoice_details['state'],
                invoice_details['zip']
            ))
            # Get the id of the newly inserted client
            client_id = cursor.lastrowid

        # Insert into invoices table
        cursor.execute("""
            INSERT INTO invoices (invoice_no, client_id, date, po, sales_rep, project)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            invoice_details['invoice no'],
            client_id,
            invoice_details['date'],
            invoice_details['po'],
            invoice_details['sales rep'],
            invoice_details['project']
        ))

        # Get the id of the newly inserted invoice
        invoice_id = cursor.lastrowid

        # Insert items into invoice_items table
        for item_no, item in enumerate(invoice_items, start=1):

            amount_in_cents = int(round(item['usd'] * 100))
            cursor.execute("""
                INSERT INTO invoice_items (invoice_id, item_no, name, description, quantity, amount)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                invoice_id,
                item_no,  # item_no is the index + 1 in the list
                item['name'],
                item['description'],
                item['quantity'],
                amount_in_cents  # Ensure this is a float value
            ))

        # Commit all changes after the loop
        conn.commit()
        print("Invoice saved succesfully.")

    except sqlite3.Error as e:
        # Roll back in case of error
        print(f"An error occurred: {e}")
        conn.rollback()
    return

def details_confirmed():
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
    while True:
        invoice_no_input = input(prompt)

        if invoice_no_input.isdigit():
            return invoice_no_input
        elif invoice_no_input == '':
            DEFAULT_INVOICE_NO = 9999
            invoice_no_input = DEFAULT_INVOICE_NO
            return invoice_no_input
        else:
            print("Invalid number.")

def get_quantity_input(prompt):
    while True:
        quantity_input = input(prompt).strip()
        
        if quantity_input.isdigit():  # Handle optional negative sign
            return int(quantity_input)
        elif quantity_input == '':
            return 1
        else:
            print("Invalid input. Please enter a valid quantity.")

def get_usd_amount_input(prompt):
    while True:
        amount_input = input(prompt).strip()

        if amount_input == '':
            return 0.0
        else:
            try:
                # Convert input to float
                amount = float(amount_input)
                
                # Return the valid amount
                return amount
            except ValueError:
                print("Invalid input. Please enter a valid amount (e.g., 123.45).")

        
main()