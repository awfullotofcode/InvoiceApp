from formatting_helpers import get_state_abbreviation, get_date_input, get_invoice_no, get_quantity_input, get_usd_amount_input

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