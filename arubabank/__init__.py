name = "arubabankAPI"


import requests
from bs4 import BeautifulSoup as bs
import json


class ArubaBankAPI:
    server_url = 'https://onlinebank.arubabank.com/'
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36'}


    def __init__(self):
        self.session = requests.Session()


    def get_url(self, page=None):
        """
        Helper function to get the page url
        """
        if page == None:
            return self.server_url
        else:
            return f'{self.server_url}{page}'


    def login(self, username, password):
        """
        Function to log the user in.
        Gets the __RequestVerificationToken from the main website with BeautifulSoup
        and adds it to the the headers. Maybe this can be improved.
        """
        headers = self.headers
        response = self.session.get(self.get_url())
        soup = bs(response.content, 'lxml')
        data = str(soup.find(id="my-app-state").contents[0])
        request_verification_token_start = data.find('value&q;:&q;')+12 # Find the start of the token section
        request_verification_token_end = data.find('&', request_verification_token_start) # Find the end of the token section
        request_verification_token = data[request_verification_token_start:request_verification_token_end] # Extract the actual token

        # Add the __RequestVerificationToken to the headers to login
        headers['__RequestVerificationToken'] = request_verification_token
        login_payload = {'username':username,'tokentype':'softToken','password':password} # create the login payload.
        login_response = self.session.post(self.get_url('api/v2/account/login'), headers=headers, data=login_payload)
        return login_response



    def get_portfolios(self):
        """
        Returns all user portfolios
        """
        response = self.session.get(self.get_url('api/v2/general/portfolio'))
        
        data = json.loads(response.content.decode('utf-8'))
        return data


    def get_account_overview(self):
        """
        Returns the accounts of the selected portfolio
        """
        response = self.session.get(self.get_url('api/v2/JSSTBAccounts/getaccountoverview'))
        data = json.loads(response.content.decode('utf-8'))
        return data


    def get_account_id(self, bank_account_number=None):
        """
        The account_number used for the various API endpoints is different than the actual bank account number
        This returns the api account_number, if the account argument is specified otherwise it
        returns the first account_number from the default portfolio
        """
        if not bank_account_number:
            account_number = self.get_transaction_accounts()[0]['accountNumber'] # selects the first account from the default portfolio
        else:
            for account in self.get_account_overview()['portfolios'][0]['products']:
                if account['accountNumber'] == bank_account_number: # selects the account_number that matches the account argument
                    account_number = account['accountId']
        return account_number

    
    def get_transaction_accounts(self):
        """
        Returns all transaction accounts of the selected portfolio
        """
        response = self.session.get(self.get_url('api/v2/transactionaccount/get'))
        
        data = json.loads(response.content.decode('utf-8'))
        return data


    def get_transactions(self, account_number, clean=None):
        """
        Returns the first 50 transaction details of a specific account
        """
        if not clean:
            response = self.session.get(self.get_url(f'api/v2/transactionoverview/get?accountNumber={account_number}&pageNumber=1'))
            data = json.loads(response.content.decode('utf-8'))['items']
        else:
            response = self.session.get(self.get_url(f'api/v2/transactionoverview/get?accountNumber={account_number}&pageNumber=1'))
            data = json.loads(response.content.decode('utf-8'))['items']

            for transaction in data:
                transaction['description'] = transaction['description'].replace('\n', '') # Remove the \n from the descriptions
                transaction['transactionDate'] = transaction['transactionDate'].split('T', 1)[0] # Remove the time from the transactionDate
                transaction['amount'] = transaction['amountCurrency']['amount'] # Split the amountCurrency dictionary
                transaction['amountCurrencyCode'] = transaction['amountCurrency']['currencyCode'] # Split the amountCurrency dictionary
                transaction.pop('amountCurrency', None)
                transaction['balance'] = transaction['balanceCurrency']['amount'] # Split the balanceCurrency dictionary
                transaction['balanceCurrencyCode'] = transaction['balanceCurrency']['currencyCode'] # Split the balanceCurrency dictionary
                transaction.pop('balanceCurrency', None)
            new_transactions = []
            for transaction in data:
                new = {}
                new["transactionDate"] = transaction['transactionDate']
                new["transactionCode"] = transaction['transactionCode']
                new["description"] = transaction['description']
                new["amount"] = transaction['amount']
                new["amountCurrencyCode"] = transaction['amountCurrencyCode']
                new["balance"] = transaction['balance']
                new["balanceCurrencyCode"] = transaction['balanceCurrencyCode']
                new["isDebit"] = transaction['isDebit']
                new["beneficiaryName"] = transaction['beneficiaryName']
                new["referenceNumber"] = transaction['referenceNumber']
                new["bankMateReferenceNumber"] = transaction['bankMateReferenceNumber']
                new["transactionDetailRefId"] = transaction['transactionDetailRefId']
                new["isRecreatable"] = transaction['isRecreatable']
                new_transactions.append(new)
            data = new_transactions
        
        return data


    def refresh_session(self):
        """
        Refresh the session
        """
        response = self.session.get(self.get_url('api/v2/general/refreshsession'))
        
        return response

    
    def logout(self):
        """
        Logout the session
        """
        self.session.cookies.clear()
        
        pass

