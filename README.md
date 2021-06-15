## Aruba Bank API Client

This is a Python script that logs in to https://onlinebank.arubabank.com/ and retrieves your data.
__*It's still in early development*__. At the moment it can login and retrieve transactions of any bank account within your default portfolio and save this to a json or csv file. You will need to have an existing account with Aruba Bank, and have signed up for the ***New** Aruba Bank App as you need the App to generate your password.


#### Developers Wanted: If you're a developer located in Aruba and would like to contribute please contact me.
<a href="https://www.twitter.com/orson_297" target="_blank"><img src="https://raw.githubusercontent.com/rahuldkjain/github-profile-readme-generator/master/src/images/icons/Social/twitter.svg" alt="orson_297" height="30" width="40"></a>


## API

This API was sort of reversed engineered from the Aruba Bank website. It's not an official API so Aruba Bank can change it at any time. It's more of a way to show that it is possible for local Aruban banks to make an API and to show that there is a growing demand for local banks to offer an official API.


## Use Cases

Some of the use cases:
- Automate booking bank transactions into existing accounting programs (ex. QuickBooks) to improve efficiency and reduce human error.
- Aid in developing financial apps to track expenses and help with budgeting
- Find a way to facilitate E-Commerce on the island. With an API, bank transfers can be confirmed without user intervention.
Businesses can then choose to use bank transfers as a payment method on their websites,
making wide adoption of E-Commerce by the Aruban people much more likely, as credit cards are not widely used.


## Getting Started

Run the following commands to set up a new virtualenv and run the Aruba Bank API example:

    git clone https://github.com/orson1282/arubabank_api
    cd arubabank_api
    python3 -m venv venv                             # create a new virtual environment in the directory 'venv'
    . venv/bin/activate                              # activate this environment
    sudo python3 setup.py install                    # install all dependencies


## Usage

Every time you run this script you'll need to generate a new password with the ***New** Aruba Bank Mobile App.

    # retreive all transactions between May 1 and May 31 from bank account number 9876540190
    # from the default portfolio

    python3 -m arubabank -u jcroes -p 123456 -o csv -b 9876540190 -f 2021-05-01 -t 2021-05-31

The module with command line arguments is just to show how the api functions, ideally you would just import the module into your own application using:

    from arubabank import ArubaBankAPI

--more examples coming soon--


## Disclaimer

This is just a personal project that I decided to share and see what the demand out there is like. It's purely for educational purposes. I'm not affiliated with Aruba Bank and this project is not sponsored or supported by Aruba Bank. I can only hope that this project is an eye opener for the local banks and they decide to make it possible for local developers / businesses to get access to an official API. If you do use this API please share your experience.


## To Do List

- Recruit more local developers to the project
- ~~Get transactions based on date range~~
- Get transactions of accounts located in other portfolios
