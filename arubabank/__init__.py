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
        Get the __RequestVerificationToken from the main website
        Not the most elegant way to do this. Better way needed
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
        login_payload = {'username':username,'tokentype':'softToken','password':password}
        login_response = self.session.post(self.get_url('api/v2/account/login'), headers=headers, data=login_payload)
        return login_response



    def get_portfolios(self):
        """
        Get all portfolios
        """
        response = self.session.get(self.get_url('api/v2/general/portfolio'))
        
        data = json.loads(response.content.decode('utf-8'))
        return data


    def transaction_accounts(self):
        """
        Get transaction accounts of default portfolio
        """
        response = self.session.get(self.get_url('api/v2/transactionaccount/get'))
        
        data = json.loads(response.content.decode('utf-8'))
        return data


    def transactions_overview(self, account_number):
        """
        Get transaction details of a specific account
        """
        response = self.session.get(self.get_url(f'api/v2/transactionoverview/get?accountNumber={account_number}&pageNumber=1'))
        
        data = json.loads(response.content.decode('utf-8'))
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

