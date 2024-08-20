# Invoice App
#### [Video Demo](https://www.youtube.com/watch?v=X3A4YukxwSI&t=4s)
## Description

As an aspiring developer with a keen interest in simplifying workflows, I built the Invoice App to tackle the inefficiencies I experienced while creating invoices manually. Using Google Docs for this task felt cumbersome—constant reformatting and excessive clicking were major time sinks. To solve this, I designed the Invoice App, a command-line interface (CLI) tool crafted to streamline invoicing by minimizing mouse usage and enabling rapid data entry through keyboard commands.
# Summary of Files

## `main.py`

The `main.py` file is the core of the invoice management system. It establishes a connection to a SQLite database and provides a menu-driven interface for creating, editing, and viewing invoices. Users can navigate through options to create a new invoice, edit existing ones, or view details. The file manages invoice details and items, allowing for comprehensive invoice handling, including saving changes to the database. It also includes functionality for user interactions, such as confirming details and printing invoices, ensuring that all actions are correctly processed and recorded.

## `formatting_helpers.py`

The `formatting_helpers.py` file contains functions to validate and format user input related to invoice data. It includes functions for converting state names to abbreviations, parsing dates in multiple formats, and ensuring numeric input for invoice numbers, quantities, and monetary amounts. These functions handle user input errors by prompting for re-entry and apply appropriate formatting, such as converting dates to SQL format and monetary amounts to float. This ensures that all user inputs are correctly formatted and validated before being used in invoice processing.

## `invoice_editing_helpers.py`

The `invoice_editing_helpers.py` file provides functions for editing invoice details and items. It allows users to modify various invoice details like state, date, and invoice number, applying necessary formatting and validation. The file also enables users to update individual invoice items, including fields such as name, description, quantity, and amount. It displays current values for review, prompts for new input, and applies changes based on user selections. This interactive editing ensures that invoice data can be accurately updated and maintained.

## `print_helpers.py`

The `print_helpers.py` file includes functions for confirming and previewing invoice details. The `details_confirmed()` function prompts users to confirm if the displayed information is correct, handling various affirmative and negative responses. The `preview_invoice_item()` function provides a formatted display of an invoice item, including monetary values formatted with a dollar sign and commas. These functions enhance user interaction by ensuring that invoice information is reviewed and confirmed before finalization, contributing to accurate and clear invoice processing.

## Key Features

### Create Invoice

The `create_invoice` feature is the heart of the app, designed to automate and simplify the invoicing process. When you initiate this feature, you begin by entering essential billing details such as the client's name, address, city, state, and zip code. The app also prompts for a purchase order number, although this is optional. This ensures that all critical billing information is collected upfront.

Once the billing information is provided, you have a chance to review and confirm your entries. This confirmation step is crucial, as it allows you to catch and correct any errors before moving to the next stage. Following the confirmation of billing details, you enter additional invoice metadata, including the invoice date, number, sales representative, and project name. If you do not provide a date or invoice number, the app intelligently assigns default values, which helps to speed up the process and minimize manual input.

The next step involves entering details for each invoice item. You input the item’s name, description, quantity, and amount. To make this process even more user-friendly, the app defaults the quantity to 1 and the amount to $0.00 if no values are provided. This ensures that valid data is entered, and you can quickly move through the data entry phase.

After gathering all necessary information, the app presents a summary of the invoice for your review. This summary allows you to verify the accuracy of the data before finalizing the invoice. The flexibility to add more items or complete the invoice at this stage means you can tailor the level of detail as needed. Finally, the app displays a formatted view of the completed invoice and offers options to save, print, or exit, making invoice management straightforward and efficient.

### Edit Invoice

The `edit_invoice` feature empowers you to search for and modify existing invoices. This feature is particularly useful for correcting errors or updating details after an invoice has been created. You can search for invoices based on criteria such as invoice number, client, date, or location, which simplifies the process of finding and editing specific invoices.

By offering these search options, the app enhances its flexibility and usability, making it easier for you to keep invoices accurate and up-to-date. This feature is a vital component for managing corrections and ensuring that all invoices reflect the most current and accurate information.

### View Invoice

With the `view_invoice` feature, you can easily retrieve and review invoices. This functionality is essential for verifying that completed invoices meet the required standards before finalizing them. You can search for invoices by criteria like invoice number, which provides a quick and efficient way to access specific records without navigating through multiple files or systems.

This streamlined access to invoice data improves efficiency and helps you manage your invoicing tasks with ease. The ability to quickly view and verify invoices is a key aspect of the app’s design, ensuring that you can maintain accuracy and organization in your invoicing process.

## Data Storage and Management

To manage invoice and client data, the app utilizes an SQLite database. SQLite was chosen due to its lightweight and efficient nature, which aligns perfectly with the app’s goal of providing a fast and streamlined invoicing experience. SQLite’s simplicity allows for quick data access and manipulation without the overhead of a larger, more complex database system.

This choice of database technology ensures that the app remains responsive and easy to maintain while still providing robust data storage and retrieval capabilities. SQLite’s integration into the app reflects a thoughtful approach to balancing performance with simplicity.

## User Confirmation and Validation

A key design choice in the app is the emphasis on user confirmation and validation throughout the invoicing process. By including multiple prompts for you to review and confirm your input, the app reduces the likelihood of errors and ensures that all invoices are created with accurate information.

These validation steps are strategically placed at various points in the workflow, helping to catch mistakes early and maintain data integrity. This approach not only enhances the reliability of the invoicing process but also fosters a smoother user experience by providing opportunities to correct errors before they impact billing or client relationships.
