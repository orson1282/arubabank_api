from arubabank import ArubaBankAPI
import argparse
from helper_functions import fix_transactions
import json
import csv


parser = argparse.ArgumentParser()
parser.add_argument("-u", "--username", metavar='', type=str, help="Your username", required=True)
parser.add_argument("-p", "--password", metavar='', type=str, help="Your password", required=True)
parser.add_argument("-o", "--output", metavar='', type=str, help="Set output file (json or csv)", choices=['json', 'csv'], required=True)
args = parser.parse_args()


api = ArubaBankAPI()
login = api.login(args.username, args.password)


account_number = api.transaction_accounts()[0]['accountNumber']


transactions = api.transactions_overview(account_number)['items']
transactions = fix_transactions(transactions)


# Write transactions to JSON File
if args.output == 'json':
    with open('transactions.json', 'w') as file:
        json.dump(transactions, file)


# Write transactions to CSV File
if args.output == 'csv':
    keys = transactions[0].keys()
    with open('transactions.csv', 'w', newline='')  as file:
        dict_writer = csv.DictWriter(file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(transactions)