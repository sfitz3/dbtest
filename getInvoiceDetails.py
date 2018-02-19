import requests
import datetime
import sys
from datetime import date
from datetime import time
# from datetime import datetime
from csv import reader
from pathlib import Path
import os.path

isProduction = False #Need to Add a loop for year and month to build the output file, otherwise the query for payment method takes too long and times out

#Input File - Save original file so you can always revert back later
f2=open('invaccount2.csv','r')
#filename='no-country-subscriptions.csv'
fout=open('invoiceaccountshistory','a+')

#set the attributes for production or staging Aria
if isProduction:
    # Point to Production

    ariaoutfile = 'accountsWithInvoices_Prod.txt'

    clientID= '5747004'
    auth= 'HBAETeMpu3Hn9nmQgD9dtnaMQtWqGfFG'
    ariaCoreUrl= 'https://secure.ariasystems.net/api/ws/api_ws_class_dispatcher.php'
    #ariaObjectURL = 'https://secure.ariasystems.net/api/AriaQuery/objects.php'
    #ariaAdminURL = 'XXXhttps://admintools.ariasystems.net/index.php/Dispatcher/index'
    #              ^Remove XXX if ready to update - extra safety measure to prevent accidental update
    #Set Update Flags: True will enable; False Disable.  Revert will repopulate old LHGUID using same existing file. Should always retain orginal to get back to original values.

else:
    # Point to Staging
    clientID = '4934683'
    auth = 'DtcWUTxMYSySytSMtAerN3H67be5mH5n'
    ariaCoreUrl = 'https://secure.future.stage.ariasystems.net/api/ws/api_ws_class_dispatcher.php' #core URL
    #ariaObjectURL = 'https://secure.future.stage.ariasystems.net/api/AriaQuery/objects.php'
    #ariaAdminURL = 'xxxhttps://admintools.future.stage.cph.ariasystems.net/AdminTools.php/Dispatcher'
    ariaoutfile = 'accountsWithInvoices_Stage.txt'
# Set Update Flags: True will enable; False Disable.  Revert will repopulate old LHGUID using same existing file. Should always retain orginal to get back to original values.

print(ariaCoreUrl)

#object API
#Example query string: query_string=where status_cd = 1 and supp_field_name = Product_Family and supp_field_value = PBSP

#ariaGetAcctUrl= ariaObjectURL + '?client_no=' + clientID + '&auth_key=' + auth + '&rest_call=get_account_details&query_string=where last_name = Marley&output_format=json'
ariaGetAcctUrl= ariaCoreUrl + '?client_no=' + clientID + '&auth_key=' + auth + '&rest_call=get_invoice_details&acct_no='
#UKariaGetAcctUrl=ariaCoreURL + '?client_no=' + UKclientID + '&auth_key=' + UKauth + '&rest_call=get_acct_details_all&acct_no='
#AUariaGetAcctUrl=ariaCoreURL + '?client_no=' + AUclientID + '&auth_key=' + AUauth + '&rest_call=get_acct_details_all&acct_no='


#ariaGetAcctUrl= ariaObjectURL + '?client_no=' + clientID + '&auth_key=' + auth + '&rest_call=get_account_details&query_string=where pay_method = 14 or pay_method = 29&output_format=json'

#ariaGetAcctUrl= ariaObjectURL + '?client_no=' + clientID + '&auth_key=' + auth + '&rest_call=get_account_details&query_string=where pay_method = 14&output_format=json'


usurl = ariaGetAcctUrl + str(25022259) + '&src_transaction_id=131567998&output_format=json'
print(usurl)
#print ('passed A2 check')

#print('US ID: '+str(aria_us_id))
response2 = requests.get(usurl)
response_dict = response2.json()
print(response_dict)



