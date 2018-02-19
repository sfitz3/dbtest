import requests
import datetime
import sys
from datetime import date
from datetime import time
# from datetime import datetime
from csv import reader

#This version does a lookup using an account list in a file to pull each account status.
isProduction = True


ariaAPI = '&rest_call=get_acct_details_all&acct_no='
#ariaAPI2 = '&rest_call=get_acct_details_all&acct_no='

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
    ariaCoreUrl = 'XXXhttps://secure.future.stage.ariasystems.net/api/ws/api_ws_class_dispatcher.php' #core URL
    #ariaObjectURL = 'https://secure.future.stage.ariasystems.net/api/AriaQuery/objects.php'
    #ariaAdminURL = 'xxxhttps://admintools.future.stage.cph.ariasystems.net/AdminTools.php/Dispatcher'
    ariaoutfile = 'ariaAccountList_staging.txt'
#              ^Remove XXX if ready to update - extra safety measure to prevent accidental update

#Example query string: query_string=where status_cd = 1 and supp_field_name = Product_Family and supp_field_value = PBSP

#ariaGetAcctUrl= ariaObjectURL + '?client_no=' + clientID + '&auth_key=' + auth + '&rest_call=get_account_details&query_string=where last_name = Marley&output_format=json'

#ariaGetAcctUrl= ariaObjectURL + '?client_no=' + clientID + '&auth_key=' + auth + '&rest_call=get_account_details&query_string=where pay_method = 14 or pay_method = 29&output_format=json'

#ariaGetAcctUrl= ariaObjectURL + '?client_no=' + clientID + '&auth_key=' + auth + '&rest_call=get_account_details&query_string=where pay_method = 14&output_format=json'

def callAria ():
#This function calls the get_acct_plans Aria API to retrieve all the plan and rate data on the account
#It parses the output and builds a text file with the data necessary to build a load file for the modify plan rates call
    with open(ariaoutfile, 'a+') as outfile:

        infile1 = open(readfile, 'r')

        writestring = 'Acct,status' + '\n'
        outfile.write(writestring)
        bloop = -1


        for line in reader(infile1):
            Acct,junk = line

            if bloop > -1:

                # set the URL with the account number for the lookup
                ariaGetAcctUrl = ariaCoreUrl + '?client_no=' + clientID + '&auth_key=' + auth + ariaAPI + str(Acct)+'&output_format=json'

                # Execute the API call
                print(ariaGetAcctUrl+'\n')
                response2 = requests.get(ariaGetAcctUrl)

                # copy the json response to a dictionary
                response_dict = response2.json()





                vAccount = Acct
                vStatus = response_dict['status_cd']
                vclientPlanID = 'None'
                vSrvNo = 'None'
                vIsRecurring = 'None'
                vIsUsage = 'None'
                vrateSchedNum = 'None'
                vratePlanNum = 'None'
                vrateSeqNo = 'None'
                vfromUnit = 'None'
                vtoUnit = 'None'
                vratePerUnit = 'None'
                vsuppPlanIndicator = 'None'
                vclientRateSchedID = 'None'
                masterrateschedule = 'None'




                writestring = str(Acct)+','+vStatus+'\n'
                print(writestring)
                outfile.write(writestring)





                # Increment the indexing variable| and continue the loop

            bloop = bloop+1

callAria()