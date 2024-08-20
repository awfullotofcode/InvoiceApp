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
            edit_invoice()
        elif menu_action in ('view','v','vie','vew','veiw','vw','3'):
            print("TODO: view_invoices()")
        elif menu_action == 'exit' or menu_action == '4':
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
    display_invoice()
    current_invoice_actions()
    return

def edit_invoice():
    while True:
        search_by_selection = input("____________________\n     EDIT  MENU     \nSearch by:\n[1]Invoice\n[2]Client\n[3]Date\n[4]Location\nSelect: ")
        
        if search_by_selection in ('1','invoice','i'):
            # TODO: Open invoice submenu search_by_invoice()
            search_by_invoice()
            return
        elif search_by_selection in ('2','client','clint','cient','c'):
            # TODO: Open client submenu
            return
        else:
            print("Invalid selection.")

def search_by_invoice():
    while True:
        # Get invoice selection
        invoice_selection = input("___________________\nSearch by invoice:\n[1]Invoice no.\n[2]Invoice ID\nSelect: ").strip().lower()
        # Query for client, invoice, invoice items
        if invoice_selection in ('1','invoice no.','invoice no','invoice number','no','number'):
            # Search by invoice no
            while True:
                invoice_no_selection = input("Enter invoice no: ").strip()
                if invoice_no_selection.isdigit():
                    search_invoice_no(invoice_no_selection)
                    return
                else:
                    print("Enter valid invoice number.")    
        elif invoice_selection in ('2','id','invoice id'):
            # TODO
            # Search by id
            return

def search_invoice_no(invoice_no):
    
    
    # Query for all matching invoices
    cursor.execute('''
        SELECT id, invoice_no, client_id, date, po, sales_rep, project
        FROM invoices
        WHERE invoice_no = ?
    ''', (invoice_no,))
    
    results = cursor.fetchall()
    
    if results:
        # Display the list of results
        print("__________________\nSelect an Invoices:\n\n")
        for index, row in enumerate(results, start=1):
            invoice_id, _, client_id, date, po, sales_rep, project = row
            print(f"[{index}] Invoice No: {invoice_no}  Date: {date}\nProject: {project}  Sales Rep: {sales_rep}\n----------")
  

        # User selects which invoice to edit
        while True:
            try:
                selection = int(input("Select invoice number to edit: ").strip())
                if 1 <= selection <= len(results):
                    invoice_id = results[selection - 1][0]  # Get the invoice_id of the selected invoice
                    break
                else:
                    print("Invalid selection. Please choose a valid number.")
            except ValueError:
                print("Invalid input. Please enter a number.")
        
        # Get client details
        cursor.execute('''
            SELECT name, street, city, state, zip
            FROM clients
            WHERE id = (
                SELECT client_id
                FROM invoices
                WHERE id = ?
            )
        ''', (invoice_id,))
        client = cursor.fetchone()
        client_name, street, city, state, zip = client if client else ("Unknown", "", "", "", "")
        
        # Populate invoice details
        global invoice_details
        cursor.execute('''
            SELECT invoice_no, date, po, sales_rep, project
            FROM invoices
            WHERE id = ?
        ''', (invoice_id,))
        result = cursor.fetchone()
        invoice_no, date, po, sales_rep, project = result
        
        invoice_details = {
            'invoice no': invoice_no,
            'name': client_name,
            'street': street,
            'city': city,
            'state': state,
            'zip': zip,
            'date': date,
            'po': po,
            'sales rep': sales_rep,
            'project': project
        }
        
        # Query for invoice items
        cursor.execute('''
            SELECT item_no, name, description, quantity, amount
            FROM invoice_items
            WHERE invoice_id = ?
        ''', (invoice_id,))
        
        global invoice_items
        invoice_items = [
            {
                'item no': row[0],
                'name': row[1],
                'description': row[2],
                'quantity': row[3],
                'usd': row[4]
            }
            for row in cursor.fetchall()
        ]
        

        print("Invoice found")
        invoice_editor(invoice_details,invoice_items)
    else:
        print("Invoice number not found.")
    
# turn invoice query results into invoice_details(dictionary) & invoice_items(list of dictionaries)
# Pass invoice_details and invoice_items into invoice_editor
# invoice_editor(invoice_details,invoice_items)

def search_by_client():
    # TODO
    return

def invoice_editor(invoice_details=None,invoice_items=None):
    # Use global variables if no arguments are provided
    if invoice_details is None:
        invoice_details = globals().get('invoice_details', {})
    if invoice_items is None:
        invoice_items = globals().get('invoice_items', [])

    while True:
        display_invoice(invoice_details,invoice_items)
        edit_option = input("___________________\n    EDIT OPTIONS    \n[1]Details\n[2]Items\n[3]Save changes ->\n\nSelect: ").strip().lower()
        if edit_option in ('1','d','det','details','dtails','dtls'):
            edit_invoice_details(invoice_details)
        elif edit_option in ('2','items','itms','iems','i'):
            edit_invoice_items(invoice_items)
            # TODO
            return
        elif edit_option in ('3','save changes','sc','save change'):
            # Display to user invoice details then menu options
            display_invoice(invoice_details,invoice_items)
            return
        else:
            print("Please enter a valid selection.")

def edit_invoice_details(invoice_details=None):
    if invoice_details is None:
        invoice_details = globals().get('invoice_details', {})
    while True:
        print("Current invoice details:")
        for idx, (key, value) in enumerate(invoice_details.items(), start=1):
            if key == 'usd':
                value = f"${value:,.2f}"
            print(f"[{idx}] {key.capitalize()}: {value}")

        print("[0] Save and exit")
        selection = input("Select detail to edit: ").strip()

        if selection == '0':
            return

        try:
            detail_index = int(selection)
            if 1 <= detail_index <= len(invoice_details):
                detail_key = list(invoice_details.keys())[detail_index - 1]
                current_value = invoice_details[detail_key]
                print(f"Editing '{detail_key.capitalize()}'.\nCurrent: {current_value}")

                # Collect new value for the selected detail
                if detail_key == 'state':
                    new_value = get_state_abbreviation(input(f"New value for {detail_key.capitalize()}: ") or current_value)
                elif detail_key == 'date':
                    new_value = get_date_input(f"New value for {detail_key.capitalize()} (MM-DD-YYYY): ") or current_value
                elif detail_key == 'invoice no':
                    new_value = get_invoice_no(f"New value for {detail_key.capitalize()}: ") or current_value
                else:
                    new_value = input(f"New value for {detail_key.capitalize()}: ") or current_value

                # Update the invoice details dictionary with the new value
                invoice_details[detail_key] = new_value
            else:
                print("Invalid selection. Please select a valid number.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def edit_invoice_items(invoice_items=None):
    if invoice_items is None:
        invoice_items = globals().get('invoice_items', [])

    if not invoice_items:
        print("No items to edit.")
        return

    while True:
        # Display all items with their index as item_no
        print("____________________\nCurrent invoice items:\n\n")
        for index, item in enumerate(invoice_items):

            print(f"Item [{index + 1}]:\nName: {item['name']}\nDescription: {item['description']}\nQty: {item['quantity']}\nAmount: ${item['usd']:,.2f}")
            print("----------")

        # Select item to edit based on index
        item_no_to_edit = input("Enter the Item No to edit (or '0' to return): \n\n").strip()

        if item_no_to_edit == '0':
            return
        
        try:
            item_no_to_edit = int(item_no_to_edit) - 1
            if 0 <= item_no_to_edit < len(invoice_items):
                item_to_edit = invoice_items[item_no_to_edit]

                print(f"Editing Item No: {item_no_to_edit + 1}")
                print(f"[1]Name: {item_to_edit['name']}")
                print(f"[2]Description: {item_to_edit['description']}")
                print(f"[3]Quantity: {item_to_edit['quantity']}")
                print(f"[4]Amount: ${item_to_edit['usd']:,.2f}")
                print("[0]Save and exit")

                while True:
                    edit_field = input("Select: ").strip()

                    if edit_field == '1':
                        new_name = input("Enter new name (or press Enter to keep current): \n\n").strip()
                        if new_name:
                            item_to_edit['name'] = new_name
                    elif edit_field == '2':
                        new_description = input("Enter new description (or press Enter to keep current): \n\n").strip()
                        if new_description:
                            item_to_edit['description'] = new_description
                    elif edit_field == '3':
                        new_quantity = get_quantity_input("Enter new quantity (or press Enter to keep current): \n\n")
                        if new_quantity is not None:
                            item_to_edit['quantity'] = new_quantity
                    elif edit_field == '4':
                        new_amount = get_usd_amount_input("Enter new amount (or press Enter to keep current): \n\n")
                        if new_amount is not None:
                            item_to_edit['usd'] = new_amount
                    elif edit_field == '0':
                        break
                    else:
                        print("Invalid selection. Please enter a valid number.")
            else:
                print("Invalid Item No. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

def current_invoice_actions():
    print("____________________")
    while True:
        menu_action = input("[1]SAVE | [2]EDIT\n[3]PRINT| [4]EXIT\n[5]RETURN TO MENU ->\nSelect: ").strip().lower()

        if menu_action in ('save','sve','sae','s','1'):
            display_invoice()
            save_invoice()
        elif menu_action in ('edit','edt','eit','2'):
            invoice_editor()
        elif menu_action in ('print','pirnt','prnt','pint','p','3'):
            # TODO
            print("TODO: print_invoice()")
        elif menu_action in ('menu','men','meu','m','rtm','return to menu','r','5'):
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
            # TODO insert po into clients
            # TODO Alter clients and invoices table (po column is in invoices table when it should be in clients)
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
            INSERT INTO invoices (invoice_no, client_id, date, sales_rep, project)
            VALUES (?, ?, ?, ?, ?)
        """, (
            invoice_details['invoice no'],
            client_id,
            invoice_details['date'],
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