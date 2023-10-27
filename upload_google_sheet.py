import gspread

def upload(exchange_rate):
    # Authorize the API
    # Use the full URL to my JSON file on PythonAnywhere
    gc = gspread.service_account(filename='/home/olenamykhailova/mysite/service_account.json')

    st = gc.open('Python Sheet')

    # selecting a worksheet
    worksheet = st.sheet1

    # clear a worksheet
    worksheet.clear()
    #Write the array to worksheet starting from the A1 cell
    worksheet.update(exchange_rate, 'A1')