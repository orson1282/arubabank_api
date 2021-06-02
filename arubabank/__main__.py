from arubabank import ArubaBankAPI
import argparse
import json
import csv


parser = argparse.ArgumentParser()
parser.add_argument("-u", "--username", metavar='', type=str, help="Your username", required=True)
parser.add_argument("-p", "--password", metavar='', type=str, help="Your password", required=True)
parser.add_argument("-o", "--output", metavar='', type=str, help="Set output file (json or csv)", choices=['json', 'csv'], required=True)
parser.add_argument("-b", "--bankaccount", metavar='', type=str, help="Bank Account Number", required=False)
args = parser.parse_args()


api = ArubaBankAPI()
login = api.login(args.username, args.password)


account_number = api.get_account_id(args.bankaccount) # returns the account_number used for api endpoints based on bank account number
transactions = api.get_transactions(account_number, clean=True) # returns the transactions in a clean format for json or csv


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