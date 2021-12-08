name = "arubabankAPI"


import requests
from bs4 import BeautifulSoup as bs
import json
from datetime import datetime as dt
import sys


class ArubaBankAPI:
    server_url = "https://onlinebank.arubabank.com/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36"
    }

    def __init__(self):
        self.session = requests.Session()

    def get_url(self, page=None):
        """
        Helper function to get the page url
        """
        if page == None:
            return self.server_url
        else:
            return f"{self.server_url}{page}"

    def login(self, username, password):
        """
        Function to log the user in.
        Gets the __RequestVerificationToken from the main website with BeautifulSoup
        and adds it to the the headers. Maybe this can be improved.
        """
        try:
            response = self.session.get(self.get_url())
            response.raise_for_status()
        except requests.exceptions.ConnectionError as e:
            print(f"Error: {e}")
            sys.exit()
        except requests.exceptions.HTTPError as e:
            print(f"Error: {e}")
            sys.exit()

        soup = bs(response.content, "lxml")
        data = str(soup.find(id="my-app-state").contents[0])
        request_verification_token_start = (
            data.find("value&q;:&q;") + 12
        )  # Find the start of the token section
        request_verification_token_end = data.find(
            "&", request_verification_token_start
        )  # Find the end of the token section
        request_verification_token = data[
            request_verification_token_start:request_verification_token_end
        ]  # Extract the actual token

        # Add the __RequestVerificationToken to the headers to login
        self.headers.update(
            {"__RequestVerificationToken": request_verification_token}
        )
        login_payload = {
            "username": username,
            "tokentype": "softToken",
            "password": password,
        }  # create the login payload.
        try:
            login_response = self.session.post(
                self.get_url("api/v2/account/login"),
                headers=self.headers,
                data=login_payload
            )
            login_response.raise_for_status()
        except requests.exceptions.ConnectionError as e:
            print(f"Error: {e}")
            sys.exit()
        except requests.exceptions.HTTPError as e:
            print(f"Error: {e}")
            sys.exit()
        return login_response

    def get_portfolios(self):
        """
        Returns all user portfolios
        """
        try:
            response = self.session.get(self.get_url("api/v2/general/portfolio"))
            response.raise_for_status()
        except requests.exceptions.ConnectionError as e:
            print(f"Error: {e}")
            sys.exit()
        except requests.exceptions.HTTPError as e:
            print(f"Error: {e}")
            sys.exit()
        data = json.loads(response.content.decode("utf-8"))
        return data

    def get_portfolio_ids(self):
        """
        Returns all user portfolio IDs
        """
        data = self.get_portfolios()
        ids = []
        for p in data['portfolios']:
            ids.append(p['id'])
        return ids

    def get_account_overview(self):
        """
        Returns the accounts of the selected portfolio
        """
        try:
            response = self.session.get(
                self.get_url("api/v2/JSSTBAccounts/getaccountoverview")
            )
            response.raise_for_status()
        except requests.exceptions.ConnectionError as e:
            print(f"Error: {e}")
            sys.exit()
        except requests.exceptions.HTTPError as e:
            print(f"Error: {e}")
            sys.exit()
        data = json.loads(response.content.decode("utf-8"))
        return data

    def get_account_id(self, bank_account_number=None):
        """
        The account_number used for the various API endpoints is different than the actual bank account number
        This returns the api account_number, if the account argument is specified otherwise it
        returns the first account_number from the default portfolio
        """
        if not bank_account_number:
            account_number = self.get_transaction_accounts()[0][
                "accountNumber"
            ]  # selects the first account from the default portfolio
        else:
            for account in self.get_account_overview()["portfolios"][0]["products"]:
                if (
                    account["accountNumber"] == bank_account_number
                ):  # selects the account_number that matches the account argument
                    account_number = account["accountId"]
        return account_number

    def get_transaction_accounts(self):
        """
        Returns all transaction accounts of the selected portfolio
        """
        try:
            response = self.session.get(self.get_url("api/v2/transactionaccount/get"))
            response.raise_for_status()
        except requests.exceptions.ConnectionError as e:
            print(f"Error: {e}")
            sys.exit()
        except requests.exceptions.HTTPError as e:
            print(f"Error: {e}")
            sys.exit()
        data = json.loads(response.content.decode("utf-8"))
        return data

    def get_transactions(self, account_id, from_date, to_date, transaction_type=None):
        """
        Returns the transaction details of a specific account between a specific date range
        if to_date is not specified today's date is used
        """
        # Convert from_date to datetime object
        from_date = dt.strptime(from_date, "%Y-%m-%d")

        # Convert to_date to datetime object if it is passed in, if not leave it as is
        if isinstance(to_date, str):
            to_date = dt.strptime(to_date, "%Y-%m-%d")
        else:
            # somehow API is set to UTC and not AST
            to_date = dt.utcnow()

        # Get total pages of all transactions
        url = self.get_url(
            f"api/v2/transactionoverview/get?accountNumber={account_id}&pageNumber=1"
        )
        # https://stackoverflow.com/a/53899577/861597
        now = {"Cache-Control": "no-cache"}
        try:
            total_pages = self.session.get(url, headers=now)
            total_pages.raise_for_status()
        except requests.exceptions.ConnectionError as e:
            print(f"Error: {e}")
            sys.exit()
        except requests.exceptions.HTTPError as e:
            print(f"Error: {e}")
            sys.exit()
        total_pages = json.loads(total_pages.content.decode("utf-8"))["totalPages"]

        filtered_data = []

        for page_number in range(1, total_pages + 1):
            try:
                response = self.session.get(
                    self.get_url(
                        f"api/v2/transactionoverview/get?accountNumber={account_id}&pageNumber={page_number}"
                    )
                )
                response.raise_for_status()
            except requests.exceptions.ConnectionError as e:
                print(f"Error: {e}")
                sys.exit()
            except requests.exceptions.HTTPError as e:
                print(f"Error: {e}")
                sys.exit()
            data = json.loads(response.content.decode("utf-8"))["items"]

            first_date = dt.strptime(
                (data[0]["transactionDate"].split("T", 1)[0]), "%Y-%m-%d"
            )  # Get first date on transactions page

            if first_date >= from_date:
                for transaction in data:
                    transaction_date = dt.strptime(
                        transaction["transactionDate"].split("T", 1)[0], "%Y-%m-%d"
                    )
                    transaction["transactionDate"] = transaction[
                        "transactionDate"
                    ].split("T", 1)[
                        0
                    ]  # Remove the time from the transactionDate
                    transaction["description"] = transaction["description"].replace(
                        "\n", ""
                    )  # Remove the \n from the descriptions
                    transaction["amount"] = transaction["amountCurrency"][
                        "amount"
                    ]  # Split the amountCurrency dictionary
                    transaction["amountCurrencyCode"] = transaction["amountCurrency"][
                        "currencyCode"
                    ]  # Split the amountCurrency dictionary
                    transaction.pop("amountCurrency", None)
                    transaction["balance"] = transaction["balanceCurrency"][
                        "amount"
                    ]  # Split the balanceCurrency dictionary
                    transaction["balanceCurrencyCode"] = transaction["balanceCurrency"][
                        "currencyCode"
                    ]  # Split the balanceCurrency dictionary
                    transaction.pop("balanceCurrency", None)
                    if (from_date <= transaction_date) and (
                        to_date >= transaction_date
                    ):
                        if transaction_type == "debit":
                            if transaction["isDebit"]:
                                filtered_data.append(transaction)
                        elif transaction_type == "credit":
                            if not transaction["isDebit"]:
                                filtered_data.append(transaction)
                        else:
                            filtered_data.append(transaction)
                    else:
                        continue
            else:
                break

        reordered_data = []
        for transaction in filtered_data:
            dict = {}
            dict["transactionDate"] = transaction["transactionDate"]
            dict["transactionCode"] = transaction["transactionCode"]
            dict["description"] = transaction["description"]
            dict["amount"] = transaction["amount"]
            dict["amountCurrencyCode"] = transaction["amountCurrencyCode"]
            dict["balance"] = transaction["balance"]
            dict["balanceCurrencyCode"] = transaction["balanceCurrencyCode"]
            dict["isDebit"] = transaction["isDebit"]
            dict["beneficiaryName"] = transaction["beneficiaryName"]
            dict["referenceNumber"] = transaction["referenceNumber"]
            dict["bankMateReferenceNumber"] = transaction["bankMateReferenceNumber"]
            dict["transactionDetailRefId"] = transaction["transactionDetailRefId"]
            dict["isRecreatable"] = transaction["isRecreatable"]
            reordered_data.append(dict)

        return reordered_data

    def refresh_session(self):
        """
        Refresh the session
        """
        try:
            response = self.session.get(self.get_url("api/v2/general/refreshsession"))
            response.raise_for_status()
        except requests.exceptions.ConnectionError as e:
            print(f"Error: {e}")
            sys.exit()
        except requests.exceptions.HTTPError as e:
            print(f"Error: {e}")
            sys.exit()
        return response

    def logout(self):
        """
        Logout the session
        """
        self.session.cookies.clear()

        pass
