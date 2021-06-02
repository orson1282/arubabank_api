## Aruba Bank API Client

This is a Python script that logs in to https://onlinebank.arubabank.com/ and retrieves your data.
__*It's still in early development*__. At the moment it can login and retrieve the first 50 transactions of the first account of your default portfolio and save this to a json or csv file. You will need to have an existing account with Aruba Bank, and have signed up for the ***New** Aruba Bank App as you need the App to generate your password.

### Developers Wanted: If you're a developer located in Aruba and would like to contribute please contact me.


## Use Cases

Some of the use cases:
- Automate the reconcilation process with existing accounting packages drastically improving effeciency.
- Aid in developing financial apps to track expenses and help with budgeting
- Find a way to facilitate E-Commerce on the island. With an API, bank transfers can be confirmed without user intervention.
Businesses can then choose to use bank transfers as a payment method on their websites,
making wide adoption of E-Commerce by the Aruban people much more likely, as credit cards are not widely used.


## Usage

Every time you run this script you'll need to generate a new password with the ***New** Aruba Bank Mobile App.

    # login and retrieve first 50 transactions of default portfolio and dump it into a csv file
    python3 -m arubabank -u jcroes -p 123456 -o csv

    # login and retrieve first 50 transactions of default portfolio and dump it into a json file
    python3 -m arubabank -u bwerleman -p 321654 -o json

    # login and retrieve first 50 transactions of bank account 9876540190 and dump it into a csv file
    python3 -m arubabank -u eodor -p 124578 -o csv -b 9876540190

--more examples coming soon--


## API

This API was sort of reversed engineered from the Aruba Bank website. It's not an official API so Aruba Bank can change it at any time. It's more of a way to show that it is possible for local Aruban banks to make an API and to show that there is a growing demand for local banks to offer an official API.

## Getting Started

Run the following commands to set up a new virtualenv and run the Aruba Bank API example:

    git clone https://github.com/orson1282/arubabank_api
    cd arubabank_api
    python3 -m venv venv                             # create a new virtual environment in the directory 'venv'
    . venv/bin/activate                              # activate this environment
    ./setup.py install                               # install all dependencies
    python3 -m arubabank -u <username> -p <password> -o json # Use the mobile app to generate your password


## Disclaimer

This is just a personal project that I decided to share and see what the demand out there is like. It's purely for educational purposes. I'm not affiliated with Aruba Bank and this project is not sponsored or supported by Aruba Bank. I can only hope that this project is an eye opener for the local banks and they decide to make it possible for local developers / businesses to get access to an official API. If you do use this API please share your experience.

## To Do List

- Recruit more local developers to the project
- Maybe develop it into a rest api ?
