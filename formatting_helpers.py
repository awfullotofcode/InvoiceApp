from datetime import datetime
import us


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
