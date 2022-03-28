import gspread
from google.oauth2.service_account import Credentials
from pprint import pprint

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS  = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('love_sandwiches')


def get_sales_data():
    """
    Get sales figures input from the user
    run while loop to collect valid string of data from the user
    via the terminal, which must be a string of 6 numbers separated
    separated by commas. the loop will repeadetly request data, until it is valid
    """
    while True:
        print('please enter sales data from the last market')
        print('data should be six numbers separated by commas')
        print('example: 10, 20, 30, 40, 50, 60\n')

        data_str = input('enter your data here: ')
        
        sales_data = data_str.split(',')
                
        if validate_data(sales_data):
            print('data is valid')
            break

    return sales_data


def validate_data(values):
    """
    inside the try, converts all values into integers,
    raises ValueError if strings cannot be converted into int,
    or if there aren't exactly 6 values.
    """
    try:
        [int(value) for value in values]
        if len(values) != 6:
            raise ValueError(
                f'6 values are required, you provided {len(values)}'
            )
    except ValueError as e:
        print(f'invalid data: {e}, please try again\n')
        return False

    return True


def update_sales_worksheet(data):
    """
    update sales worksheet, add new row with the list data provided
    """
    print('updating sales worksheet...\n')
    sales_worksheet = SHEET.worksheet('sales')
    sales_worksheet.append_row(data)
    print('worksheet updated successfully\n')


def calculate_surplus_data(sales_row):
    """
    compare sales with stock and calculate the surplus for each item type
    the surplus is defined as the sales figure subtracted from the stock:
    - positive surplus indicates waste
    - negative surplus indicates extra made when stock was sold out
    """
    print('calculating surplus data...\n')
    stock = SHEET.worksheet('stock').get_all_values()
    stock_row = stock[-1]
    
    surplus_data = []
    for stock, sales in zip(stock_row, sales_row):
        difference = int(stock) - sales
        surplus_data.append(difference)
    
    return surplus_data 


def main():
    """
    Run all program functions
    """
    data = get_sales_data()
    sales_data = [int(num) for num in data]
    update_sales_worksheet(sales_data)
    new_surplus_data = calculate_surplus_data(sales_data)
    print(new_surplus_data)


print(
'''
##############################################
# welcome to love sandwiches data automation #
##############################################
'''
     )


main()