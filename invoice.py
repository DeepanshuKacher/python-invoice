import platform

# Determine the operating system
current_os = platform.system()

# Conditional import based on the operating system
if current_os == 'Windows':
    import win32print
    # Add any other Windows-specific imports
elif current_os == 'Linux':
    # Import Linux-specific printing libraries if needed
    pass
elif current_os == 'Darwin':  # macOS
    # Import macOS-specific printing libraries if needed
    pass
else:
    raise OSError("Unsupported Operating System")

def format_integer_string_back_whitespace(n):
    str_n = str(n)
    return str_n.ljust(7) if len(str_n) < 7 else str_n

def make_40_characters_long(input_string):
    if len(input_string) < 40:
        total_spaces = 40 - len(input_string)
        left_spaces = total_spaces // 2
        return (' ' * left_spaces) + input_string
    else:
        return input_string[:40]

def print_with_margins_and_cut(printer_name, itemsArr, top_margin=0, bottom_margin=5):
    if current_os == 'Windows':
        printer = win32print.OpenPrinter(printer_name)
    # Add logic for Linux/macOS when implemented
    
    textHead_array = ['Retail invoice','DUTT GURUKARIPA','SOUTH TUKOGANJ','INDORE','Tel:- (0731 4222227)']

    processedText = ''
    for index, string in enumerate(textHead_array):
        processedText += make_40_characters_long(string) + '\n' if index != len(textHead_array) - 1 else make_40_characters_long(string)

    heading = """
----------------------------------------
                INVOICE
----------------------------------------
Item      Qyt         RATE        Amount
----------------------------------------
"""

    footer = """
----------------------------------------
Total:-               Rs:-  {total_price}
----------------------------------------

Thank you for your purchase!
"""
    new_footer = footer + '\n' * bottom_margin
    newHeading = processedText + heading
    totalPrice = 0

    try:
        if current_os == 'Windows':
            raw_data = newHeading.encode('utf-8')
            h_job = win32print.StartDocPrinter(printer, 1, ("Printing with Margins and Cutting", None, "RAW"))
            win32print.StartPagePrinter(printer)
            win32print.WritePrinter(printer, raw_data)
            win32print.EndPagePrinter(printer)
            win32print.EndDocPrinter(printer)

            for item in itemsArr:
                printItem = """
{item_name}
          {item_quantity}     {item_price}     {calculate_price}
"""
                calculateRow = item['quantity'] * item['price']
                puttingValuesinprintItem = printItem.format(
                    item_name=item['name'],
                    item_quantity=format_integer_string_back_whitespace(item['quantity']),
                    item_price=format_integer_string_back_whitespace(item['price']),
                    calculate_price=calculateRow
                )
                totalPrice += calculateRow
                raw_data = puttingValuesinprintItem.encode('utf-8')
                h_job = win32print.StartDocPrinter(printer, 1, ("Printing with Margins and Cutting", None, "RAW"))
                win32print.StartPagePrinter(printer)
                win32print.WritePrinter(printer, raw_data)
                win32print.EndPagePrinter(printer)
                win32print.EndDocPrinter(printer)

            raw_data = new_footer.format(total_price=totalPrice).encode('utf-8')
            h_job = win32print.StartDocPrinter(printer, 1, ("Printing with Margins and Cutting", None, "RAW"))
            win32print.StartPagePrinter(printer)
            win32print.WritePrinter(printer, raw_data)
            win32print.EndPagePrinter(printer)
            win32print.EndDocPrinter(printer)

    finally:
        if current_os == 'Windows':
            cut_command = b'\x1D\x56\x01'  # ESC/POS command for paper cutting
            h_job = win32print.StartDocPrinter(printer, 1, ("Cutting Paper", None, "RAW"))
            win32print.StartPagePrinter(printer)
            win32print.WritePrinter(printer, cut_command)
            win32print.EndPagePrinter(printer)
            win32print.EndDocPrinter(printer)
            win32print.ClosePrinter(printer)
        # Add paper cutting logic for other OS if needed

# Example usage
# printer_name = 'RETSOL RTP-80'
# itemsArr = [
#     {"name":'Mongo juice',"quantity":100,"price":2.00},
#     {"name":'Laptop',"quantity":15,"price":50.00},
#     {"name":'Speaker',"quantity":20,"price":700.00},
# ]
# print_with_margins_and_cut(printer_name, itemsArr)
