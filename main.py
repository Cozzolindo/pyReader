import glob
import re
import os

import parse
import pdfplumber
import pandas as pd
from collections import namedtuple

lines = namedtuple('Line', [
    'Category', 'Received_date', 'Invoice_date', 'Due_Date', 'Amount', 'Currency', 'Supplier', 'Description',
    'Expense_Period', 'Requester', 'Approval', 'Jeeves_Holding_Brasil_Jeeves_Brasil_Financas', 'Booked_AP',
    'Paid_Not_Paid', 'Date_for_schedule_payment', 'Payment_Date', 'Month', 'Year', 'Invoice', 'Link', 'Note',
    'PAID', 'Tax_to_pay', 'Banco', 'VENDOR_ID', 'DEP', 'Approval_status', 'Approval_support', 'Email_subject',
    'Email_sender', 'Payment_receipt', 'Booked_Expense', 'Booked_payment'
])

line_num = 0
file_folder = './pdf'
output = './csv/output.csv'

supplier = re.compile(r'DE (.*) OS')
invoiceDate = re.compile(r'(\d{2}/\d{2}/\d{4})')
invoice = re.compile(r'Nº (.*)')
description = re.compile(r'\d+\s+(.*?)\s+\d+')
amount = re.compile(r'(\S+)$')

# Check if the output file exists
file_exists = os.path.isfile(output)


for file in glob.glob(os.path.join(file_folder, '*.pdf')):
    print("Processing file:", file)

    line_num = 0
    supplierName = None
    totalAmount = None
    invoiceNum = None
    invoiceDateValue = None
    jeevesName = None
    prodName = None
    prodList = []

    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            lines_list = text.split('\n')
            for line in lines_list:
                #print(line)
                match = supplier.search(line)
                if match and supplierName is None:
                    supplierName = match.group(1)
                match = invoice.search(line)
                if match and invoiceNum is None:
                    invoiceNum = match.group(1)
                
                if line.endswith("DATA DA EMISSÃO") and invoiceDateValue is None:
                    nextLine = lines_list[line_num + 1]
                    match = amount.search(nextLine)
                    if match:
                        invoiceDateValue = match.group(1)
                if line.startswith("J") and jeevesName is None:
                    jeevesList = line.split(' ')
                    jeevesName = ' '.join(jeevesList[:3])
                if line.startswith("DADOS DO PRODUTO"):
                    count = line_num
                    while True:
                        nextLine = lines_list[count + 1]
                        match = description.search(nextLine)
                        if match:
                            prodName = match.group(1)
                            prodList.append(prodName)
                        count += 1
                        if nextLine.startswith("CÁLCULO DO"):
                            break
                if line.endswith("VALOR TOTAL DA NOTA"):
                    nextLine = lines_list[line_num + 1]
                    match = amount.search(nextLine)
                    if match and totalAmount is None:
                        totalAmount = match.group(1)
                        

                line_num += 1

    # Extracting the month and year from the invoice date
    dateList = invoiceDateValue.split('/')

    # Join the product names into a single string
    prodList = ', '.join(prodList)  

    # Create a namedtuple instance with the extracted values
    line_instance = lines(
        Category=None, Received_date=None, Invoice_date=invoiceDateValue, Due_Date=None, Amount=totalAmount, Currency="BRL",
        Supplier=supplierName, Description=prodList, Expense_Period=None, Requester=None, Approval=None,
        Jeeves_Holding_Brasil_Jeeves_Brasil_Financas=jeevesName, Booked_AP=None, Paid_Not_Paid=None,
        Date_for_schedule_payment=None, Payment_Date=None, Month=dateList[1], Year=dateList[2], Invoice=invoiceNum,
        Link=None, Note=None, PAID=None, Tax_to_pay=None, Banco=None, VENDOR_ID=None, DEP=None,
        Approval_status=None, Approval_support=None, Email_subject=None, Email_sender=None,
        Payment_receipt=None, Booked_Expense=None, Booked_payment=None
    )

    # Create a DataFrame from the namedtuple instance
    df = pd.DataFrame([line_instance._asdict()])

    

    # Export to CSV: append if exists, write header only if not exists
    df.to_csv(output, mode='a', header=not file_exists, index=False)
    file_exists = True