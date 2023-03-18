# Description

This project is a Python script that collects data from a shipping company API, performs web scraping to get updated status and saves all the data in an Excel file.

# Installation
To run this script, you will need to install the following libraries:

selenium, 
pandas, 
requests, 
openpyxl

# Configuration
Before running the script, you need to set your access token and client code for the shipping company API. You can do this by editing the following lines in the code:

client_code = "your_client_code",
access_token = "your_access_token"

# Usage
To use this script, simply run the shipping_data.py file using a Python interpreter:

python shipping_data.py

The script will start collecting data from the shipping company API and performing web scraping to get updated status. The data will be saved in an Excel file named ShippingData.xlsx.
