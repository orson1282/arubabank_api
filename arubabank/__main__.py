from arubabank import ArubaBankAPI
import argparse
import json
import csv
import threading
import time
import sys


def background(args, api, transactions, t_diff):
    """
    Define what the background running thread must do
    https://stackoverflow.com/a/31768999/861597 .
    """
    while True:
        # time between reconnects to keep the session connected
        time.sleep(120)
        t_new = get_transactions(args, api)
        diff = len(t_new) - len(transactions)
        if diff > 0:
            t_diff = t_new[0:diff]
            # append solely new "rows" of data
            for t in t_diff:
                # send each transaction to output
                print(t)
                # TODO: insert is expensive, maybe change to deque or asc sort?
                transactions.insert(0, t)
            return save_transactions(transactions, args)


def get_transactions(args, api):
    """
    Encapsulator for the fetching of new data.
    """
    api.refresh_session()
    # Returns the account_id used for api endpoints based on bank account number
    account_id = api.get_account_id(args.bankaccount)
    # Returns the transactions in a clean format for json or csv processing
    return api.get_transactions(
        account_id,
        from_date=args.fromdate,
        to_date=args.todate,
        transaction_type=args.transaction_type,
    )


def save_transactions(transactions, args):
    """
    Save the extracted transactions. We pass a copy of transactions in case it
    ever happens that transactions global gets new data while we are saving.
    TODO: suppose this app is running for months, what issues will arise?
    """
    # Write transactions to JSON File
    if args.output == "json":
        with open("transactions.json", "w") as file:
            json.dump(transactions, file, indent=4)
        file.close()
    # Write transactions to CSV File
    if args.output == "csv":
        keys = transactions[0].keys()
        with open("transactions.csv", "w", newline="") as file:
            dict_writer = csv.DictWriter(file, keys)
            dict_writer.writeheader()
            dict_writer.writerows(transactions)
        file.close()


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-u", "--username", metavar="", type=str, help="Your username", required=True
    )
    parser.add_argument(
        "-p", "--password", metavar="", type=str, help="Your password", required=True
    )
    parser.add_argument(
        "-o",
        "--output",
        metavar="",
        type=str,
        help="Set output format (json or csv)",
        choices=["json", "csv"],
        required=True,
    )
    parser.add_argument(
        "-b",
        "--bankaccount",
        metavar="",
        type=str,
        help="Your Bank Account Number (optional)",
        required=False,
    )
    parser.add_argument(
        "-f", "--fromdate", metavar="", type=str, help="From Date", required=True
    )
    parser.add_argument(
        "-t", "--todate", metavar="", type=str, help="To Date", required=False
    )
    parser.add_argument(
        "-tt",
        "--transaction_type",
        metavar="",
        type=str,
        help="The transaction type you wish to get (optional)",
        choices=["debit", "credit"],
        required=False,
    )
    parser.add_argument(
        "-m",
        "--mode",
        metavar="",
        type=str,
        help="Mode can be either 1 'active' (keep-alive) or 0 'passive'",
        required=False,
        default=0,
    )
    return parser.parse_args()


def main():
    args = parse_arguments()
    # Start api and log in
    api = ArubaBankAPI()
    api.login(args.username, args.password)

    if args.mode == "1":
        # Cancel todate for active mode
        args.todate = None
        # Initial save
        transactions = get_transactions(args, api)
        save_transactions(transactions, args)
        t_diff = transactions
        instructions = "Please wait while new transactions are "
        instructions += "being listened to or type 'quit' to terminate.\n"
        print(instructions)
        th1 = threading.Thread(
            target=background, args=(args, api, transactions, t_diff)
        )
        th1.daemon = True
        th1.start()
        while True:
            if input("") == "quit":
                print("Quitting...")
                if api != None:
                    print("Logging out...")
                    api.logout()
                sys.exit()
    else:
        transactions = get_transactions(args, api)
        save_transactions(transactions, args)


if __name__ == "__main__":
    main()
