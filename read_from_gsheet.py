# read.py
import gspread
from google.oauth2 import service_account

from googleapiclient.discovery import build


def read_data_from_sheet(spread_sheet_id, sheet_name, store_name):
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    SERVICE_ACCOUNT_FILE = 'keys.json'

    print(f"Getting data from the google sheet: {sheet_name}")
    credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    client = gspread.authorize(credentials)
    spreadsheet = client.open_by_url(f"https://docs.google.com/spreadsheets/d/{spread_sheet_id}/edit")
    worksheet = spreadsheet.worksheet(sheet_name)
    results = worksheet.get_all_values()
    all_rows = []
    starting = False
    store_name = str(store_name).strip().title()
    print(f"Finding Order list for: {store_name}")
    for result in results:
    
        name = result[0]
        name = str(name).strip().title()
        order_price = result[2]



        if store_name in name or store_name == name:
            starting = True
        if 'Total' in name:
            starting = False
            
        if starting == True and result !=[] and order_price != '':
            all_rows.append(result)
        final_rows = all_rows[1:]
    return final_rows


def read_data_from_sheet2(spread_sheet_id, sheet_name):
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    SERVICE_ACCOUNT_FILE = 'keys.json'

    print(f"Getting all orders from {sheet_name}")
    credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    client = gspread.authorize(credentials)
    spreadsheet = client.open_by_url(f"https://docs.google.com/spreadsheets/d/{spread_sheet_id}/edit")
    worksheet = spreadsheet.worksheet(sheet_name)
    results = worksheet.get_all_values()

    return results

def fetch_data_from_gsheet(store_name, r_payment_amount):
    store_name = store_name
    spread_sheet_id = '1qBLaFA9VXVIU0ITcbmlWlgsB3kIyVVP7I86Lf1gaiXw'
    sheet_name= 'Today\'s Payout'
    all_rows = read_data_from_sheet(spread_sheet_id, sheet_name, store_name)
    sheet_name= 'Calculation'
    sub_total_row = all_rows[-1]
    all_rows.pop()
    all_order_id_extractions = read_data_from_sheet2(spread_sheet_id, sheet_name)
    order_list=[]
    print(f"Finding data for all order id")
    total_markup = 0
    total_payout = 0
    total_unit_price = 0
    total_sales_tax = 0
    total_total = 0

    for row in all_rows:
        try:
            order_id = row[1]
            order_date = row[0]
        except:
            order_date =''
            pass
        for all_order_id_extraction in all_order_id_extractions:
            try:
                order_id_for_s = all_order_id_extraction[1]
            except:
                order_id_for_s = ''


            if order_id == order_id_for_s and order_id_for_s !='':
                selling_price = float(all_order_id_extraction[2].replace("$", ""))
                
                pay_out_platform = float(all_order_id_extraction[6].replace("$", ""))
                order_discounts = all_order_id_extraction[3]
                if order_discounts != "":
                    order_discounts = float(all_order_id_extraction[3].replace("$", ""))*-1
                else:
                    order_discounts = 0

                platform_fees = (selling_price - order_discounts) * 0.30 * 1.12
                markup_fee = (selling_price - order_discounts) * 0.10
                total_price = pay_out_platform - markup_fee
                unite_price = total_price/1.05
                sales_tax = unite_price * 0.05
                

                
                total_markup = total_markup + markup_fee
                total_payout = total_payout + pay_out_platform
                total_unit_price = total_unit_price + unite_price
                total_sales_tax = total_sales_tax + sales_tax
                total_total = total_total + total_price

                markup_fee = "{:.2f}".format(markup_fee)
                order_discounts = "{:.2f}".format(order_discounts)
                platform_fees = "{:.2f}".format(platform_fees)
                selling_price = "{:.2f}".format(selling_price)
                pay_out_platform = "{:.2f}".format(pay_out_platform)
                unite_price = "{:.2f}".format(unite_price)
                sales_tax = "{:.2f}".format(sales_tax)
                total_price = "{:.2f}".format(total_price)

                order_row = {"Order Date": order_date,
                            "Order Id": order_id,
                            "Markup": "$"+str(markup_fee),
                            "Discount": "$"+str(order_discounts),
                            "Platform fees": "$"+str(platform_fees),
                            "Selling Price": "$"+str(selling_price),
                            "Payout from platform": "$"+str(pay_out_platform),
                            "Unit Price": "$"+str(unite_price),
                            "Sales Tax": "$"+str(sales_tax),
                            "Total": "$"+str(total_price)
                            }
                order_list.append(order_row)
    total_total = r_payment_amount
    total_markup = "{:.2f}".format(total_markup)
    total_payout = "{:.2f}".format(total_payout)
    total_unit_price = "{:.2f}".format(total_unit_price)
    total_sales_tax = "{:.2f}".format(total_sales_tax)
    total_total = "{:.2f}".format(total_total)
    last_second_row = {"Order Date": "",
                    "Order Id": "",
                    "Markup": "",
                    "Discount": "",
                    "Platform fees": "",
                    "Selling Price": "",
                    "Payout from platform": "",
                    "Unit Price": "",
                    "Sales Tax": "",
                    "Total": ""
                }
    last_row = {"Order Date": "",
                    "Order Id": "",
                    "Markup": "$"+str(total_markup),
                    "Discount": "",
                    "Platform fees": "",
                    "Selling Price": "",
                    "Payout from platform": "$"+str(total_payout),
                    "Unit Price": "$"+str(total_unit_price),
                    "Sales Tax": "$"+str(total_sales_tax),
                    "Total": "$"+str(total_total)
                }
    order_list.append(last_second_row)
    order_list.append(last_row)
    order_list.append(last_second_row)
    
    return order_list, sub_total_row, total_total

