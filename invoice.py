import win32print

def print_with_margins_and_cut(printer_name, itemsArr, top_margin=0, bottom_margin=5):
    # Add top and bottom margins to the text
    # text_with_margins = '\n' * top_margin + text_to_print + '\n' * bottom_margin

    printer = win32print.OpenPrinter(printer_name)


    heading = """
----------------------------------------
                INVOICE
----------------------------------------
Item           |    Quantity    |  Price
----------------------------------------
"""

    

    footer = """
----------------------------------------
Total:                        $15.00
----------------------------------------

Thank you for your purchase!
"""
    new_footer = footer + '\n' * bottom_margin




    try:
        
       h_printer = win32print.GetDefaultPrinter()
       raw_data = heading.encode('utf-8')  # Convert text to bytes
       h_job = win32print.StartDocPrinter(printer, 1, ("Printing with Margins and Cutting", None, "RAW"))
       win32print.StartPagePrinter(printer)
       win32print.WritePrinter(printer, raw_data)
       win32print.EndPagePrinter(printer)
       win32print.EndDocPrinter(printer)
       # Send command for paper cutting
       for item in itemsArr:

        printItem = """{item_name}         |       {item_quantity}        |  ₹{item_price}"""+'\n'

        puttingValuesinprintItem = printItem.format(
           item_name = item['name'],
           item_quantity = item['quantity'],
           item_price = item['price']
        )

        h_printer = win32print.GetDefaultPrinter()
        raw_data = puttingValuesinprintItem.encode('utf-8')  # Convert text to bytes
        h_job = win32print.StartDocPrinter(printer, 1, ("Printing with Margins and Cutting", None, "RAW"))
        win32print.StartPagePrinter(printer)
        win32print.WritePrinter(printer, raw_data)
        win32print.EndPagePrinter(printer)
        win32print.EndDocPrinter(printer)
       # Send command for paper cutting
       h_printer = win32print.GetDefaultPrinter()
       raw_data = new_footer.encode('utf-8')  # Convert text to bytes
       h_job = win32print.StartDocPrinter(printer, 1, ("Printing with Margins and Cutting", None, "RAW"))
       win32print.StartPagePrinter(printer)
       win32print.WritePrinter(printer, raw_data)
       win32print.EndPagePrinter(printer)
       win32print.EndDocPrinter(printer)
       # Send command for paper cutting
    
    finally:
        cut_command = b'\x1D\x56\x01'  # ESC/POS command for paper cutting
        h_job = win32print.StartDocPrinter(printer, 1, ("Cutting Paper", None, "RAW"))
        win32print.StartPagePrinter(printer)
        win32print.WritePrinter(printer, cut_command)
        win32print.EndPagePrinter(printer)
        win32print.EndDocPrinter(printer)
        win32print.ClosePrinter(printer)

# Replace 'RETSOL RTP-80' with the name of your printer
printer_name = 'RETSOL RTP-80'
text = """
----------------------------------------
                INVOICE
----------------------------------------
Item           |    Quantity    |  Price
----------------------------------------
Item 1         |       2        |  $10.00
Item 2         |       1        |  $5.00
----------------------------------------
Total:                        $15.00
----------------------------------------

Thank you for your purchase!
"""

# Adjust top_margin and bottom_margin values as needed (in number of blank lines)
num_copies = 3  # Change this value to the number of copies you want
itemsArr = [
    {"name":'Mongo juice',"quantity":5,"price":20.00},
    {"name":'Cow urine juice',"quantity":7,"price":5.00},
    {"name":'Laptop',"quantity":15,"price":50.00},
    {"name":'Speaker',"quantity":2,"price":700.00},
]
print_with_margins_and_cut(printer_name, itemsArr, top_margin=0, bottom_margin=5)




"""     cut_command = b'\x1D\x56\x01'  # ESC/POS command for paper cutting
        win32print.StartDocPrinter(printer, 1, ("Cutting Paper", None, "RAW"))
        win32print.StartPagePrinter(printer)
        win32print.WritePrinter(printer, cut_command)
        win32print.EndPagePrinter(printer)
        win32print.EndDocPrinter(printer) """