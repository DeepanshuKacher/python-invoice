import win32print
from datetime import datetime
from typing import List, Union, TypedDict
# import asyncio
# import websockets




class Item(TypedDict):
    size: str  # Size can be "L", "M", or "S"
    quantity: int  # Quantity as a number
    halfFull: str  # "H" or "F"
    dishName: str  # Name of the dish
    kotCount: int  # Kot count as a number
    printCount: int  # Print count as a number
    kotId: str  # Kot ID as a string

def format_integer_string_back_whitespace(n,length):
    # Convert integer to string
    str_n = str(n)
    
    # Check if length is less than 7
    if len(str_n) < length:
        # Add whitespace at the end to make it 7 characters long
        formatted_string = str_n.rjust(length)
    else:
        # If length is already 7 or more, keep the string as it is
        formatted_string = str_n
    
    return formatted_string

def make_40_characters_long(input_string):
    # Check if input string length is less than 40
    if len(input_string) < 40:
        # Calculate the required whitespace on both sides
        total_spaces = 40 - len(input_string)
        left_spaces = total_spaces // 2
        right_spaces = total_spaces - left_spaces

        # Center the string with whitespace on both sides
        # result_string = input_string.center(40 - right_spaces, ' ')
        result_string = (' '*left_spaces) + input_string
    else:
        # If length is already 40 or more, keep the string as it is
        result_string = input_string[:40]  # Trim the string to 40 characters

    return result_string


def kotPrint(printer_name:str, itemsArr:List[Item], top_margin=0, bottom_margin=5):


    printer = win32print.OpenPrinter(printer_name)
 
# Item----------Qyt-----------RATE---------Amount-    48

# ----------------------------------------    40
# Item      Qyt         RATE        Amount    40

    # textHead_array = ['DUTT GURUKARIPA',]

    # processedText = ''

    # for index, string in enumerate(textHead_array):
    #     if index != len(textHead_array) - 1:
    #         processedText = processedText + make_40_characters_long(string) + '\n'
    #     else:
    #         processedText += make_40_characters_long(string)

    heading = """
DATE & TIME:- {date}
KOT NO. :- {kotCount}     PRINT NO.:- {printCount}
----------------------------------------
Size    Qyt        Item
----------------------------------------
"""

#  
#    


    newHeading = heading.format(
        date = datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
        kotCount = itemsArr[0]['kotCount'],
        printCount = itemsArr[0]['printCount']
    )


    try:
        
        h_printer = win32print.GetDefaultPrinter()
        raw_data = newHeading.encode('utf-8')  # Convert text to bytes
        h_job = win32print.StartDocPrinter(printer, 1, ("Printing with Margins and Cutting", None, "RAW"))
        win32print.StartPagePrinter(printer)
        win32print.WritePrinter(printer, raw_data)
        win32print.EndPagePrinter(printer)
        win32print.EndDocPrinter(printer)
        # Send command for paper cutting
        for item in itemsArr:


            printItem = """{size}    {quantity}   {halfFull}   {dishName}"""+"\n"

            puttingValuesinprintItem = printItem.format(
               halfFull = item['halfFull'],
               quantity = format_integer_string_back_whitespace(item['quantity'],4),
               size = item['size'],
               dishName=item['dishName']
            )
            
            h_printer = win32print.GetDefaultPrinter()
            raw_data = puttingValuesinprintItem.encode('utf-8')  # Convert text to bytes
            h_job = win32print.StartDocPrinter(printer, 1, ("Printing with Margins and Cutting", None, "RAW"))
            win32print.StartPagePrinter(printer)
            win32print.WritePrinter(printer, raw_data)
            win32print.EndPagePrinter(printer)
            win32print.EndDocPrinter(printer)    



        h_printer = win32print.GetDefaultPrinter()
        raw_data = (''+ '\n' * bottom_margin).encode('utf-8')  # Convert text to bytes
        h_job = win32print.StartDocPrinter(printer, 1, ("Printing with Margins and Cutting", None, "RAW"))
        win32print.StartPagePrinter(printer)
        win32print.WritePrinter(printer, raw_data)
        win32print.EndPagePrinter(printer)
        win32print.EndDocPrinter(printer)
    finally:

        cut_command = b'\x1D\x56\x01'  # ESC/POS command for paper cutting
        h_job = win32print.StartDocPrinter(printer, 1, ("Cutting Paper", None, "RAW"))
        win32print.StartPagePrinter(printer)
        win32print.WritePrinter(printer, cut_command)
        win32print.EndPagePrinter(printer)
        win32print.EndDocPrinter(printer)
        win32print.ClosePrinter(printer)


        return itemsArr[0]['kotId']





""" {
    size: Order['size']
    quantity: number
    halfFull: "H" | "F"
    dishName: string
} """