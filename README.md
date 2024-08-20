# Invoice App
#### Video Demo: <URL HERE>
## Description

As an aspiring developer with a keen interest in simplifying workflows, I built the Invoice App to tackle the inefficiencies I experienced while creating invoices manually. Using Google Docs for this task felt cumbersome—constant reformatting and excessive clicking were major time sinks. To solve this, I designed the Invoice App, a command-line interface (CLI) tool crafted to streamline invoicing by minimizing mouse usage and enabling rapid data entry through keyboard commands.

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

## Conclusion

Overall, the Invoice App is designed to make invoicing faster, more accurate, and less tedious. By leveraging a CLI for efficient data entry and incorporating features for creating, editing, and viewing invoices, the app provides a powerful tool for managing invoicing tasks with minimal effort.
