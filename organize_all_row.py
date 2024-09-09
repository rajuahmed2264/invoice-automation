
import random


def row_organization(order_list, payment_date, payment_number, payment_amount, total_total, r_payment_amount):
    
    last_header_row = {"Order Date": "Date ",
                            "Order Id": "Description",
                            "Markup": "",
                            "Discount": "",
                            "Platform fees": "",
                            "Selling Price": "",
                            "Payout from platform": "",
                            "Unit Price": "",
                            "Sales Tax": "Ref No ",
                            "Total": "Amount"
                        }
    last_payment_prof_row = {"Order Date": str(payment_date),
                            "Order Id": "e-Transfer sent",
                            "Markup": "",
                            "Discount": "",
                            "Platform fees": "",
                            "Selling Price": "",
                            "Payout from platform": "",
                            "Unit Price": "",
                            "Sales Tax": str(payment_number),
                            "Total": "$"+str(payment_amount)
                        }
    balance_after = float(total_total) - r_payment_amount
    if balance_after >=0.01:
        random_index = random.randint(0, len(order_list) - 4)
        selling_price = order_list[random_index]["Selling Price"]
        selling_price = float(selling_price.replace("$", ""))
        selling_price = selling_price - balance_after

        pay_out_platform = order_list[random_index]["Payout from platform"]
        pay_out_platform = float(pay_out_platform.replace("$", ""))

        order_discounts = order_list[random_index]["Discount"]

        if order_discounts != "":
            order_discounts = float(order_discounts.replace("$", ""))*1
        else:
            order_discounts = 0

        platform_fees = (selling_price - order_discounts) * 0.30 * 1.12
        markup_fee = (selling_price - order_discounts) * 0.10
        total_price = order_list[random_index]["Total"]
        unite_price = total_price/1.05
        sales_tax = unite_price * 0.05

        total_price = total_price + (balance_after*-1)
        markup_fee = "{:.2f}".format(markup_fee)
        order_discounts = "{:.2f}".format(order_discounts)
        platform_fees = "{:.2f}".format(platform_fees)
        selling_price = "{:.2f}".format(selling_price)
        pay_out_platform = "{:.2f}".format(pay_out_platform)
        unite_price = "{:.2f}".format(unite_price)
        sales_tax = "{:.2f}".format(sales_tax)
        total_price = "{:.2f}".format(total_price)

        order_list[random_index]["Selling Price"] = "$"+str(selling_price)
        order_list[random_index]["Markup"] = "$"+str(markup_fee)
        order_list[random_index]["Discount"] = "$"+str(order_discounts)
        order_list[random_index]["Platform fees"] = "$"+str(platform_fees)
        order_list[random_index]["Payout from platform"] = "$"+str(pay_out_platform)

        order_list[random_index]["Unit Price"] = "$"+str(unite_price)
        order_list[random_index]["Sales Tax"] =  "$"+str(sales_tax)
        order_list[random_index]["Total"] = "$"+str(total_price)

    elif balance_after <=0:
        random_index = random.randint(0, len(order_list) - 4)
        selling_price = order_list[random_index]["Selling Price"]
        selling_price = float(selling_price.replace("$", ""))
        selling_price = selling_price - balance_after

        pay_out_platform = order_list[random_index]["Payout from platform"]
        pay_out_platform = float(pay_out_platform.replace("$", ""))

        order_discounts = order_list[random_index]["Discount"]

        if order_discounts != "":
            order_discounts = float(order_discounts.replace("$", ""))*1
        else:
            order_discounts = 0

        platform_fees = (selling_price - order_discounts) * 0.30 * 1.12
        markup_fee = (selling_price - order_discounts) * 0.10
        total_price = order_list[random_index]["Total"]
        total_price = float(total_price.replace("$", ""))
        unite_price = total_price/1.05
        sales_tax = unite_price * 0.05
        

        total_price = total_price + balance_after
        
        markup_fee = "{:.2f}".format(markup_fee)
        order_discounts = "{:.2f}".format(order_discounts)
        platform_fees = "{:.2f}".format(platform_fees)
        selling_price = "{:.2f}".format(selling_price)
        pay_out_platform = "{:.2f}".format(pay_out_platform)
        unite_price = "{:.2f}".format(unite_price)
        sales_tax = "{:.2f}".format(sales_tax)
        total_price = "{:.2f}".format(total_price)

        order_list[random_index]["Selling Price"] = "$"+str(selling_price)
        order_list[random_index]["Markup"] = "$"+str(markup_fee)
        order_list[random_index]["Discount"] = "$"+str(order_discounts)
        order_list[random_index]["Platform fees"] = "$"+str(platform_fees)
        order_list[random_index]["Payout from platform"] = "$"+str(pay_out_platform)

        order_list[random_index]["Unit Price"] = "$"+str(unite_price)
        order_list[random_index]["Sales Tax"] =  "$"+str(sales_tax)
        order_list[random_index]["Total"] = "$"+str(total_price)

    balance_after = 0
    
    balance_after = "{:.2f}".format(balance_after)
    last_empty_row = {"Order Date": "",
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
    last_balance_row = {"Order Date": "",
                        "Order Id": "",
                        "Markup": "",
                        "Discount": "",
                        "Platform fees": "",
                        "Selling Price": "",
                        "Payout from platform": "",
                        "Unit Price": "",
                        "Sales Tax": "Balance",
                        "Total": "$"+str(balance_after)
                    }
    last_last_row = {"Order Date": "",
                    "Order Id": "",
                    "Markup": "",
                    "Discount": "",
                    "Platform fees": "",
                    "Selling Price": "",
                    "Payout from platform": "",
                    "Unit Price": "",
                    "Sales Tax": "",
                    "Total": "* Rounding Difference"
                }
    last_payment_txt_row = {"Order Date": "Payment",
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
    order_list.append(last_payment_txt_row)
    order_list.append(last_header_row)
    order_list.append(last_payment_prof_row)
    order_list.append(last_empty_row)
    order_list.append(last_balance_row)
    order_list.append(last_last_row)
    return order_list