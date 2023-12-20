import win32print
# import asyncio
# import websockets

def format_integer_string_back_whitespace(n):
    # Convert integer to string
    str_n = str(n)
    
    # Check if length is less than 7
    if len(str_n) < 7:
        # Add whitespace at the end to make it 7 characters long
        formatted_string = str_n.ljust(7)
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


def print_with_margins_and_cut(printer_name, itemsArr, top_margin=0, bottom_margin=5):


    printer = win32print.OpenPrinter(printer_name)
 
# Item----------Qyt-----------RATE---------Amount-    48

# ----------------------------------------    40
# Item      Qyt         RATE        Amount    40

    textHead_array = ['Retail invoice','DUTT GURUKARIPA','SOUTH TUKOGANJ','INDORE','Tel:- (0731 4222227)']

    processedText = ''

    for index, string in enumerate(textHead_array):
        if index != len(textHead_array) - 1:
            processedText = processedText + make_40_characters_long(string) + '\n'
        else:
            processedText += make_40_characters_long(string)

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

    newHeading = processedText+heading

    totalPrice = 0

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


        printItem = """
{item_name}
          {item_quantity}     {item_price}     {calculate_price}
"""        
        calculateRow = item['quantity']*item['price']

        puttingValuesinprintItem = printItem.format(
           item_name = item['name'],
           item_quantity = format_integer_string_back_whitespace(item['quantity']),
           item_price = format_integer_string_back_whitespace(item['price']),
           calculate_price = calculateRow
        )
        totalPrice+=calculateRow

        h_printer = win32print.GetDefaultPrinter()
        raw_data = puttingValuesinprintItem.encode('utf-8')  # Convert text to bytes
        h_job = win32print.StartDocPrinter(printer, 1, ("Printing with Margins and Cutting", None, "RAW"))
        win32print.StartPagePrinter(printer)
        win32print.WritePrinter(printer, raw_data)
        win32print.EndPagePrinter(printer)
        win32print.EndDocPrinter(printer)
       # Send command for paper cutting
       h_printer = win32print.GetDefaultPrinter()
       raw_data = new_footer.format(total_price = totalPrice).encode('utf-8')  # Convert text to bytes
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
# printer_name = 'RETSOL RTP-80'

# itemsArr = [
#     {"name":'Mongo juice Mongo juice',"quantity":100,"price":2.00},
#     # {"name":'Mongo juice Mongo juice Mongo juice Mongo juice',"quantity":50,"price":20.00},
#     # {"name":'Mongo juice Mongo juice Mongo juice Mongo juice Mongo juice Mongo juice',"quantity":5,"price":20.00},
#     # {"name":'Cow urine juice',"quantity":7,"price":5.00},
#     {"name":'Laptop',"quantity":15,"price":50.00},
#     {"name":'Speaker',"quantity":20,"price":700.00},
# ]
# print_with_margins_and_cut(printer_name, itemsArr, top_margin=0, bottom_margin=5)

# async def websocket_handler(websocket, path):
#     # Receive data from the WebSocket connection

#     try:
#      # Your code goes here
#         data = await websocket.recv()
#         print(data)
#     except Exception as e:
#          print(f"An error occurred: {e}")

    
#     # Process the received data and call the print_with_margins_and_cut() function
#     # with the appropriate arguments
#     printer_name = "your_printer_name"  # Replace with your desired printer name
#     itemsArr = []  # Replace with your actual data
    
#     # print_with_margins_and_cut(printer_name, itemsArr)

#     # Send a response back to the WebSocket client if needed
#     await websocket.send("Data received and processed successfully")

# # Add this line inside your print_with_margins_and_cut() function
# # to establish the WebSocket server and start listening for connections
# start_server = websockets.serve(websocket_handler, "localhost", 8765)

# # Run the WebSocket server
# asyncio.get_event_loop().run_until_complete(start_server)
# asyncio.get_event_loop().run_forever()


# text = """
# ----------------------------------------
#                 INVOICE
# ----------------------------------------
# Item           |    Quantity    |  Price
# ----------------------------------------
# Item 1        
#                |       2        |  $10.00
# Item 2         
#                |       1        |  $5.00
# ----------------------------------------
# Total:                        $15.00
# ----------------------------------------

# Thank you for your purchase!
# """



