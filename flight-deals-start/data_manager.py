import os
import requests
# from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

# You'll need to load the information in the .env file before you try to read from it.
# Install the python-dotenv package to help with this.
# create a .env file with your environment variables, and import the environment variables AKA Load environment variables from .env file
# MY_ENV_VAR = os.getenv('MY_ENV_VAR') -> just like that you can don't have to copy paste the environment variables
# to the Run Tab and Edit configuration
load_dotenv()


SHEETY_PRICES_ENDPOINT = "https://api.sheety.co/9f9e0a2f749ae9b4e7e5a1bb5e97b184/flightDealsProject/prices"
SHEETY_USERS_ENDPOINT = "https://api.sheety.co/9f9e0a2f749ae9b4e7e5a1bb5e97b184/flightDealsProject/users"
SHEETY_AUTH_HEARDER = "Basic ZmF1emlhaDE1OjM2NTExMQ=="


class DataManager:
    # This class is responsible for talking to the Google Sheet.
    def __init__(self):
        self._username = os.getenv("SHEETY_USERNAME")
        self._password = os.getenv("SHEETY_PASSWORD")
        # self._authorization = HTTPBasicAuth(self._username, self._password)
        # Destination and Customer fields data start out empty
        self.destination_data = {}
        self.customer_data = {}

    def get_destination_data(self):
        # 2. Use the Sheety API to GET all the data in that sheet and print it out.
        spreadsheet_response = requests.get(url=SHEETY_PRICES_ENDPOINT, auth=(self._username, self._password))
        data = spreadsheet_response.json()
        self.destination_data = data["prices"]
        # 3. Try importing pretty print and printing the data out again using pprint() to see it formatted.
        # print(data)
        return self.destination_data

# 6. In the DataManager Class make a PUT request and use the row id from sheet_data
    # to update the Google Sheet with the IATA codes. (Do this using code).
    def update_destination_codes(self):
        for city_item in self.destination_data:
            new_data = {
                "price": {
                    "iataCode": city_item["iataCode"]
                }
            }
            response = requests.put(url=f"{SHEETY_PRICES_ENDPOINT}/{city_item['id']}", json=new_data, auth=(self._username, self._password))
            # PUT = https://api.sheety.co/9f9e0a2f749ae9b4e7e5a1bb5e97b184/flightDealsProject/prices/[Object ID]
            print(response.text)

    def get_customer_emails(self):
        users_response = requests.get(url=SHEETY_USERS_ENDPOINT,auth=(self._username, self._password))
        data = users_response.json()
        # Name of spreadsheet 'tab' with the customer emails should be "users".
        self.customer_data = data["users"]
        return self.customer_data
