import platform
from datetime import datetime
from typing import List, TypedDict

if platform.system() == "Windows":
    import win32print
else:
    import cups  # For Linux printing

class Item(TypedDict):
    size: str  # Size can be "L", "M", or "S"
    quantity: int  # Quantity as a number
    halfFull: str  # "H" or "F"
    dishName: str  # Name of the dish
    kotCount: int  # Kot count as a number
    printCount: int  # Print count as a number
    kotId: str  # Kot ID as a string

def format_integer_string_back_whitespace(n, length):
    str_n = str(n)
    if len(str_n) < length:
        formatted_string = str_n.rjust(length)
    else:
        formatted_string = str_n
    return formatted_string

def make_40_characters_long(input_string):
    if len(input_string) < 40:
        total_spaces = 40 - len(input_string)
        left_spaces = total_spaces // 2
        result_string = (' ' * left_spaces) + input_string
    else:
        result_string = input_string[:40]
    return result_string

def print_windows(printer_name, itemsArr, top_margin=0, bottom_margin=5):
    printer = win32print.OpenPrinter(printer_name)
    heading = """
DATE & TIME:- {date}
KOT NO. :- {kotCount}     PRINT NO.:- {printCount}
----------------------------------------
Size    Qyt        Item
----------------------------------------
"""
    newHeading = heading.format(
        date=datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
        kotCount=itemsArr[0]['kotCount'],
        printCount=itemsArr[0]['printCount']
    )

    try:
        raw_data = newHeading.encode('utf-8')
        h_job = win32print.StartDocPrinter(printer, 1, ("Printing with Margins and Cutting", None, "RAW"))
        win32print.StartPagePrinter(printer)
        win32print.WritePrinter(printer, raw_data)
        win32print.EndPagePrinter(printer)
        win32print.EndDocPrinter(printer)

        for item in itemsArr:
            printItem = """{size}    {quantity}   {halfFull}   {dishName}\n"""
            puttingValuesinprintItem = printItem.format(
                halfFull=item['halfFull'],
                quantity=format_integer_string_back_whitespace(item['quantity'], 4),
                size=item['size'],
                dishName=item['dishName']
            )

            raw_data = puttingValuesinprintItem.encode('utf-8')
            h_job = win32print.StartDocPrinter(printer, 1, ("Printing Item", None, "RAW"))
            win32print.StartPagePrinter(printer)
            win32print.WritePrinter(printer, raw_data)
            win32print.EndPagePrinter(printer)
            win32print.EndDocPrinter(printer)

        raw_data = ('\n' * bottom_margin).encode('utf-8')
        h_job = win32print.StartDocPrinter(printer, 1, ("Printing Margins", None, "RAW"))
        win32print.StartPagePrinter(printer)
        win32print.WritePrinter(printer, raw_data)
        win32print.EndPagePrinter(printer)
        win32print.EndDocPrinter(printer)
    finally:
        cut_command = b'\x1D\x56\x01'
        h_job = win32print.StartDocPrinter(printer, 1, ("Cutting Paper", None, "RAW"))
        win32print.StartPagePrinter(printer)
        win32print.WritePrinter(printer, cut_command)
        win32print.EndPagePrinter(printer)
        win32print.EndDocPrinter(printer)
        win32print.ClosePrinter(printer)

    return itemsArr[0]['kotId']

def print_linux(printer_name, itemsArr, top_margin=0, bottom_margin=5):
    conn = cups.Connection()
    printers = conn.getPrinters()
    if printer_name not in printers:
        raise Exception(f"Printer '{printer_name}' not found.")

    heading = """
DATE & TIME:- {date}
KOT NO. :- {kotCount}     PRINT NO.:- {printCount}
----------------------------------------
Size    Qyt        Item
----------------------------------------
"""
    newHeading = heading.format(
        date=datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
        kotCount=itemsArr[0]['kotCount'],
        printCount=itemsArr[0]['printCount']
    )

    job_name = "KOT Printing"
    for item in itemsArr:
        printItem = """{size}    {quantity}   {halfFull}   {dishName}\n"""
        puttingValuesinprintItem = printItem.format(
            halfFull=item['halfFull'],
            quantity=format_integer_string_back_whitespace(item['quantity'], 4),
            size=item['size'],
            dishName=item['dishName']
        )
        content = newHeading + puttingValuesinprintItem + '\n' * bottom_margin
        conn.printFile(printer_name, content, job_name, {})

def kotPrint(printer_name: str, itemsArr: List[Item], top_margin=0, bottom_margin=5):
    if platform.system() == "Windows":
        return print_windows(printer_name, itemsArr, top_margin, bottom_margin)
    else:
        return print_linux(printer_name, itemsArr, top_margin, bottom_margin)
