import requests
import datetime
import sys
from datetime import date
from datetime import time
# from datetime import datetime
from csv import reader

#Since this is a large extract, loop through calls using the account creation date
#Nested loops by year and month
isProduction = False


ariaAPI = '&rest_call=create_order&account_no='
ariaAPI2 = '&rest_call=get_acct_details_all&acct_no='

readfile = 'uniqMulti.csv'

#Need to read a CSV file, lookup each account, then output the same data with "Country" added.


#set the attributes for production or staging Aria
if isProduction:
    # Point to Production

    ariaoutfile = 'ariaAcctStatMultiplan.csv'

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
    ariaoutfile = 'ariaAccountList_staging.txt'
#              ^Remove XXX if ready to update - extra safety measure to prevent accidental update
# Set Update Flags: True will enable; False Disable.  Revert will repopulate old LHGUID using same existing file. Should always retain orginal to get back to original values.



#core API
#ariaURL2 = ariaEndPoint + '?client_no=' + clientID + '&auth_key=' + auth + '&rest_call=update_acct_complete&acct_no=' + str(
#    ACCT_NO) + '&client_acct_id=' + GuamOkta + '&application_id=' + appName + '&application_date=' + processDate + '&output_format=json'


#object API
#Example query string: query_string=where status_cd = 1 and supp_field_name = Product_Family and supp_field_value = PBSP

#ariaGetAcctUrl= ariaObjectURL + '?client_no=' + clientID + '&auth_key=' + auth + '&rest_call=get_account_details&query_string=where last_name = Marley&output_format=json'

#ariaGetAcctUrl= ariaObjectURL + '?client_no=' + clientID + '&auth_key=' + auth + '&rest_call=get_account_details&query_string=where pay_method = 14 or pay_method = 29&output_format=json'

#ariaGetAcctUrl= ariaObjectURL + '?client_no=' + clientID + '&auth_key=' + auth + '&rest_call=get_account_details&query_string=where pay_method = 14&output_format=json'
ariaorderAcctUrl = ariaCoreUrl + '?client_no=' + clientID + '&auth_key=' + auth + ariaAPI + str(18608441)+'&client_sku=pbfund&units=1&amount=25&output_format=json'
print(ariaorderAcctUrl)
i = 0
while i < 50:
    bb=requests.post(ariaorderAcctUrl)
    print(str(i))
    i = i+1

print('done')
