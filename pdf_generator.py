import datetime
import os
import pandas as pd
import numpy as np
from datetime import datetime as dt
from reportlab.pdfgen.canvas import Canvas
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.platypus import Paragraph, Frame, Table, TableStyle, Image, Spacer, SimpleDocTemplate
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

pdfmetrics.registerFont(TTFont('Calibri-Bold', 'calibrib.ttf'))
pdfmetrics.registerFont(TTFont('Calibri', 'calibri.ttf'))

# Pull in Student Names

def generate_pdf_by_data(store_info, order_list, payment_info, invoice_no, pdf_name):
    styles = getSampleStyleSheet()
    styleN = styles['Normal']

    styleT = styles['Title']
    styleB = styles["BodyText"]
    styleN.wordWrap = 'CJK'
    styleB.wordWrap = 'CJK'
    tblstyle = TableStyle([('INNERGRID', (0, 0), (-1, -10), 0.25, colors.black),
                        ('BOX', (0, 0), (-1, -10), 0.25, colors.black),
                        ('FONTSIZE', (0, 0), (-1, 0), 7),
                        ('FONTSIZE', (0, 1), (-1, -1), 7),
                        ('TEXTFONT', (0, 0), (-1, 0), 'Calibri'),
                        ('TEXTFONT', (0, 1), (-1, -1), 'Calibri'),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                        ('TEXTCOLOR', (1, 1), (0, -1), colors.black),
                        #    ('LEFTPADDING', (0, 0), (-1, -1), 1),
                        #    ('RIGHTPADDING', (0, 0), (-1, -1), 1),
                        #    ('TOPPADDING', (0, 0), (-1, -1), 5),
                        #    ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
                        ('ROWBACKGROUNDS', (0, 0), (-1, -1), (colors.HexColor('#FFFFFF'), colors.HexColor('#FFFFFF'))),
                        ('ROWBACKGROUNDS', (0, -5), (-1, -5), (colors.HexColor('#D8D8D8'), colors.HexColor('#D8D8D8'))),
                        ('WORDWRAP', (0, 0), (-1, 0), 'CJK'),
                        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#D8D8D8')),
                        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                        ('ALIGN', (0, 1), (-1, -7), 'RIGHT'),
                        ('ALIGN', (0, -6), (-1, -2), 'LEFT'),
                        ('ALIGN', (0, -1), (-1, -1), 'RIGHT'),
                        ])



    # Create a document
    c = canvas.Canvas(pdf_name)
    # Convert the order_list dictionary into a list of lists
    order_list_values = [list(order.values()) for order in order_list]

    # Combine the order_list_values with the existing data_summary
    data_summary = order_list_values

    # Convert the combined list of lists back to a DataFrame
    #data_summary = pd.DataFrame(data_summary)
    # turn datatable the table into a list of lists which is the format reportlab wants


    # config the widths and heights of this specific table
    colwidths_2 = [57, 63, 46, 52, 74, 43, 46, 35, 40]
    rowheights_2 = [20] * len(data_summary)
    
    


    

    headers = ["Date", "Description", "Markup (10%)", "Discount", "Platform fees (Commission + Tax 12%)", "Selling price", "Payout from platforms", "Unit Price", "Sales Tax", "Total"]
    all_headers = []
    for header in headers:
        header_paragrph = Paragraph(header, styleN)
        all_headers.append([header_paragrph])


    data_summary.insert(0, all_headers)

    # create table using the platypus Table object & set the style
    tbl_summary = Table(data_summary, colwidths_2, None, hAlign='LEFT', repeatRows=1)

    tbl_summary.setStyle(tblstyle)


    # Build Story - Add a spacer at the beginning for your heading
    story = [
        Spacer(1, 4 * inch)
    ]# Create a paragraph containing the text

    story.append(tbl_summary)
    # Create Page 1 Formatting
    def myFirstPage(canvas: canvas.Canvas, doc):
        canvas.saveState()
        image_path = 'logo.jpg'
        canvas.setFont("Calibri-Bold", 15) 
        # create header on first page
        canvas.drawString(270, 780, 'INVOICE')
        canvas.line(50, 770, 544, 770)
        canvas.drawImage(image_path, 50, 685, width=300, height=80)
        canvas.setFont("Calibri", 12) 
        canvas.drawString(400, 730, 'Date:')
        canvas.setFont("Calibri-Bold", 12) 
        canvas.drawString(440, 730, payment_info["payment_date"])
        canvas.setFont("Calibri", 12) 
        canvas.drawString(400, 710, 'Invoice #:')
        canvas.setFont("Calibri-Bold", 12) 
        canvas.drawString(450, 710, str(invoice_no))
        cl  = 0.8470588235294118
        canvas.setFillColorRGB(cl, cl, cl)  # Set background color

        canvas.rect(50, 670, 494, 15, fill=True, stroke=False)
        canvas.rect(50, 600, 494, 15, fill=True, stroke=False)

        # Draw "Pay to" text on the background
        canvas.setFont("Calibri", 12)
        canvas.setFillColorRGB(0, 0, 0)  # Set text color
        canvas.drawString(55, 674, "Pay to")
        canvas.drawString(55, 604, "From")
        
        canvas.drawString(57, 655, store_info["Store Name"])
        canvas.drawString(57, 640, store_info["Owner Address"])
        canvas.drawString(57, 585, 'Thunder Digital Kitchen')
        canvas.drawString(57, 570, '200 - 13571 COMMERCE PKY, RICHMOND BC V6V 2R2, CANADA')
        canvas.drawString(57, 555, 'Sales Tax (GST # 79387 4819 RT 0001)')
        canvas.setFont("Calibri-Bold", 12) 
        canvas.drawString(57, 520, 'Charges')
    # Use a Document Template so the flowable can flow to the next page.  
    pdf_name = f"invoices/{pdf_name}"
    doc = SimpleDocTemplate(
        pdf_name,
        pageSize=A4,
        rightMargin=0.6 * inch, leftMargin=0.6 * inch, topMargin=0.6 * inch, bottomMargin=0.6 * inch,
    )

    # Build and save
    doc.build(story, onFirstPage=myFirstPage)
    