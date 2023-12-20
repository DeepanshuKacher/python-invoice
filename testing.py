def format_integer_string_front_whitespace(n):
    # Convert integer to string
    str_n = str(n)
    
    # Check if length is less than 7
    if len(str_n) < 7:
        # Add whitespace at the beginning to make it 7 characters long
        formatted_string = str_n.rjust(7)
    else:
        # If length is already 7 or more, keep the string as it is
        formatted_string = str_n
    
    return formatted_string

# Example usage:
input_integer = 123
formatted_output = format_integer_string_front_whitespace(input_integer)
print(f"Formatted string: '{formatted_output}'")



def format_integer_string(n):
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

# Example usage:
input_integer = 123
formatted_output = format_integer_string(input_integer)
print(f"Formatted string: '{formatted_output}'")
