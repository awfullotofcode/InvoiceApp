
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

def preview_invoice_item(item):
    print("____________________")
    print("Please review the following:")
    for key, value in item.items():
        if key == 'usd':
            value = f"${value:,.2f}"
        print(f"{key.capitalize()}: {value}")