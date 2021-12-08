## Aruba Bank API Client

Unofficial API client for Aruba Bank Online written in Python. __*It's still in early development*__. At the moment it can login and retrieve transactions of any bank account within your **default portfolio** and save this to a json or csv file. You will need to have an existing account with Aruba Bank, and have signed up for the ***New** Aruba Bank App as you need the App to generate your one-time password.

## API

This API was reverse engineered from the Aruba Bank website and mobile app. It's not an official API so it can change at any time. It's more of a way to show that it is possible for local Aruban banks to make an API and to show that there is a growing demand for local banks to offer an official API to their clients.


## Use Cases

Some of the use cases:
- Automate booking bank transactions into existing accounting programs (ex. QuickBooks) to improve efficiency and reduce human error.
- Aid in developing financial apps to track expenses and help with budgeting.
- Facilitate E-Commerce on the island. With an official API, bank transfers can be confirmed without user intervention and almost instantly.

## Getting Started

Run the following commands to set up a new virtualenv and run the Aruba Bank API in Linux:

```bash
# Clone the git repo
git clone https://github.com/orson1282/arubabank_api
# CD into the repo
cd arubabank_api
# Create a virtual environment
python3 -m venv venv
# Activate the virtual environment
source venv/bin/activate
# Install the dependencies
sudo python3 setup.py install
```


## Usage

Every time you run this script you'll need to generate a new password with the ***New** Aruba Bank Mobile App.

```bash
# retreive all transactions between May 1 and May 31 from bank account number 9876540190
# from the default portfolio
python3 -m arubabank -u jcroes -p 123456 -o csv -b 9876540190 -f 2021-05-01 -t 2021-05-31
```

You can also just import the module into your own application using:

```python
from arubabank import ArubaBankAPI
```

--more usage examples coming soon--

## Contributing

Contributions are very **welcome** and will be fully credited. Please contribute via Pull Request on **Github.**


## Disclaimer

This is just a personal project that I decided to share to see what the demand out there is like. It's purely for educational purposes. I'm not affiliated with Aruba Bank and this project is not sponsored or supported by Aruba Bank. I can only hope that this project is an eye opener for all the local banks so they decide to make it possible for local developers / businesses to get access to an official API. If you do use this project please share your experience.


## To Do List

- Get transactions of accounts located in other portfolios
