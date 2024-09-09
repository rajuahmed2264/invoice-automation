from account_sheet_data import LarkSuiteCredentialsFetcher
import read_from_gsheet as rg
from pdf_generator import generate_pdf_by_data
from generate_inv_no import inv_num_generator
from send_invoice_mail import send_email
from organize_all_row import row_organization
from update_sheet import LarkSuiteCredentialsFetcherupload as lbsupld
from datetime import datetime

#get data from accounting sheet rows.
while True:
    starting_row_num = input("Row will start from: ")
    end_row_num = input("Row will stop at: ")
    try: 
        starting_row_num = int(starting_row_num)
        end_row_num = int(end_row_num)
    except:
        starting_row_num = ''
        end_row_num = ''
    if type(starting_row_num) == int and type(end_row_num) == int:
        break
    else:
        print('Type a valid row number')


app_id = 'cli_a4c43163ceb85009'
app_secret = 'v568vapQUJSC06DokmmvkfD7uBL8AyDW'

credentials_fetcher = LarkSuiteCredentialsFetcher(app_id, app_secret)
print("Reading Data from Account base")
all_rows = credentials_fetcher.fetch_credentials()

all_rows  = all_rows[starting_row_num-1:end_row_num]


#get  invoice row 
for single_row in all_rows:
    
    store_name = single_row['fields']['Restaurant name']
    owner_mail = single_row['fields']['Invoice Email Address'][0]['text']
    receiver_email = owner_mail
    record_id = single_row["record_id"]
    receiver_name = "Raju Ahammod"
    from_date = single_row['fields']['Date- start']
    to_date = single_row['fields']['Date End']

    from_date = from_date / 1000
    from_date = datetime.fromtimestamp(from_date)
    from_date = from_date.strftime("%d/%m/%Y")

    to_date = to_date / 1000
    to_date = datetime.fromtimestamp(to_date)
    to_date = to_date.strftime("%d/%m/%Y")


    # get data by invoice numbers
    print(f"Working on the store: {store_name}")
    
    print(f"Got all order details for {store_name}")
    

    owner_address = single_row['fields']['Address'][0]["text"]
    store_info = {"Store Name": store_name, "Owner Mail": owner_mail, "Owner Address": owner_address}
    
    payment_amount = single_row['fields']['Payment_Amount']
    r_payment_amount = float(payment_amount.replace("$", ""))
    payment_date = single_row['fields']['Payment_date']

    payment_number = single_row['fields']['Payment_Confirmation_Number']

    order_list, sub_total_row, total_total= rg.fetch_data_from_gsheet(store_name, r_payment_amount)
    
    invoice_no = inv_num_generator(payment_number, payment_date, store_name)
    pdf_name = f"{invoice_no}-{store_name}.pdf"

    
    timestamp_milliseconds = payment_date

    # Convert to seconds
    timestamp_seconds = timestamp_milliseconds / 1000.0

    # Create a datetime object from the Unix timestamp
    dt_object = datetime.fromtimestamp(timestamp_seconds)

    # Format the datetime object as a string
    formatted_date = dt_object.strftime("%B %d, %Y")
    payment_date = formatted_date
    order_list = row_organization(order_list, payment_date, payment_number, payment_amount, total_total, r_payment_amount)
    payment_info = {"payment_amount": payment_amount, "payment_date": payment_date, "payment_number": payment_number}
    #generate pdf
    print(f"Generating PDF for {store_name}")
    generate_pdf_by_data(store_info, order_list, payment_info, invoice_no, pdf_name)
    #send invoice

    send_email(receiver_email, receiver_name, from_date, to_date, pdf_name)

    #upload invoice to base
    lbsupld.upload_invoic_to_base(record_id, invoice_no, pdf_name)

program  = 'running'