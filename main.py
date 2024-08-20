from datetime import datetime
import re
import sqlite3
import sys
from formatting_helpers import get_state_abbreviation, get_date_input, get_invoice_no, get_quantity_input, get_usd_amount_input
from invoice_editing_helpers import edit_invoice_details, edit_invoice_items
from print_helpers import details_confirmed, preview_invoice_item

# Setup database connection
conn = sqlite3.connect('test.db')
cursor = conn.cursor()

invoice_details = {}
invoice_items = []

def main():
    # Main menu create/edit/preview invoice
    try:
        print_intro()
        menu()
    finally:
        conn.commit()
        conn.close()

def print_intro():
    print("   ____              _           ___           \n  /  _/__ _  _____  (_)______   / _ | ___  ___\n _/ // _ \ |/ / _ \/ / __/ -_) / __ |/ _ \/ _ \n/___/_//_/___/\___/_/\__/\__/ /_/ |_/ .__/ .__/\n                                   /_/  /_/    ")
    print("                    By: Abraham Gomez\n                    GitHub: awfullotofcode\n                    Salt Lake City, UT\n                    08-20-2024")
    return
def menu():

    while True:
        menu_action = input("Menu Actions\n[1]CREATE | [2]EDIT\n[3]VIEW   | [4]EXIT\nEnter selection:\n").strip().lower()

        if menu_action in ('c','create','cre','creat','1'):
            # create invoice
            create_invoice()
        elif menu_action in ('edit','edt','eit','2'):
            edit_invoice()
        elif menu_action in ('view','v','vie','vew','veiw','vw','3'):
            view_invoice()
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

def view_invoice():
    search_by_invoice()

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
            save_invoice()
            return
        else:
            print("Please enter a valid selection.")


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
            client_id = cursor.lastrowid

        # Check if the invoice already exists
        cursor.execute("""
            SELECT id FROM invoices WHERE invoice_no = ?
        """, (invoice_details['invoice no'],))
        existing_invoice = cursor.fetchone()

        if existing_invoice:
            # Invoice exists, use existing invoice ID
            invoice_id = existing_invoice[0]
            # Update the existing invoice
            cursor.execute("""
                UPDATE invoices
                SET client_id = ?, date = ?, sales_rep = ?, project = ?
                WHERE id = ?
            """, (
                client_id,
                invoice_details['date'],
                invoice_details['sales rep'],
                invoice_details['project'],
                invoice_id
            ))

            # Remove old items from this invoice
            cursor.execute("""
                DELETE FROM invoice_items WHERE invoice_id = ?
            """, (invoice_id,))
        else:
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
            invoice_id = cursor.lastrowid

        # Insert items into invoice_items table
        for item_no, item in enumerate(invoice_items, start=1):
            amount_in_cents = int(round(item['usd'] * 100))
            cursor.execute("""
                INSERT INTO invoice_items (invoice_id, item_no, name, description, quantity, amount)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                invoice_id,
                item_no,
                item['name'],
                item['description'],
                item['quantity'],
                amount_in_cents
            ))

        conn.commit()
        print("Invoice saved successfully.")

    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        conn.rollback()



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

        
main()