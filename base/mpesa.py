import requests
import json
from requests.auth import HTTPBasicAuth
from datetime import datetime
import base64


class Credentials:
    consumer_key = 'AnX7PSj45DKl8JsO0lPLkLo0WwqUeHaokRedzbfnhfnfMEq9'
    consumer_secret = 'ognbgffC0zGadFrH5WBtg9BT8KQmOwe9Dam7q57YfGAiRE23OJxQcdCuv5OOAF90'
    api_URL = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'



class AccessToken:
    request = requests.get(Credentials.api_URL,
                     auth=HTTPBasicAuth(Credentials.consumer_key, Credentials.consumer_secret))
    access_token = json.loads(request.text)['access_token']



class Password:
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    short_code = '174379'
    pass_key = 'bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919'
    to_encode = short_code + pass_key + timestamp
    encoded_password = base64.b64encode(to_encode.encode()).decode('utf-8')  # ✅ FIXED

# Now `encoded_password` is a string, ready for JSON serialization.


# class Password:
#     timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
#     short_code = '174379'
#     pass_key = 'bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919'
#     to_encode = short_code + pass_key + timestamp
#     encoded_password = base64.b64encode(to_encode.encode())
#     decoded_password = encoded_password.decode('utf-8')



# import requests
# import json
# from requests.auth import HTTPBasicAuth
# from datetime import datetime
# import base64

# class Credentials:
#     consumer_key = 'AnX7PSj45DKl8JsO0lPLkLo0WwqUeHaokRedzbfnhfnfMEq9'
#     consumer_secret = 'ognbgffC0zGadFrH5WBtg9BT8KQmOwe9Dam7q57YfGAiRE23OJxQcdCuv5OOAF90'
#     api_URL = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'


# class AccessToken:
#     response = requests.get(Credentials.api_URL,
#                             auth=HTTPBasicAuth(Credentials.consumer_key, Credentials.consumer_secret))
#     access_token = json.loads(response.text)['access_token']


# class Password:
#     timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
#     short_code = '174379'
#     pass_key = 'bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919'
#     to_encode = short_code + pass_key + timestamp
#     encoded_password = base64.b64encode(to_encode.encode()).decode('utf-8')


# class STKPush:
#     stk_push_url = 'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest'
    
#     headers = {
#         'Authorization': f'Bearer {AccessToken.access_token}',
#         'Content-Type': 'application/json'
#     }
    
#     payload = {
#         "BusinessShortCode": Password.short_code,
#         "Password": Password.encoded_password,
#         "Timestamp": Password.timestamp,
#         "TransactionType": "CustomerPayBillOnline",
#         "Amount": 1,  # Amount in KES
#         "PartyA": "254708374149",  # Replace with a valid phone number
#         "PartyB": Password.short_code,
#         "PhoneNumber": "254708374149",  # Replace with the number receiving the STK push
#         "CallBackURL": "https://yourcallbackurl.com/callback",  # Change this to your real callback URL
#         "AccountReference": "CompanyXLTD",
#         "TransactionDesc": "Payment for goods"
#     }
    
#     response = requests.post(stk_push_url, json=payload, headers=headers)
    
#     print(response.json())  # Debugging output

# # Run STK Push request
# STKPush()
