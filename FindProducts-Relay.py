import requests
import sys
import datetime
from pathlib import Path
import os.path
from csv import reader


#Custom Rates on account for SPOD 24852080 (staging)

#prod account with many invoices: 39955162


i = 0
#years = 1
#filepath = 'Desktop/Python2/'

#Since this is a large extract| loop through calls using the account creation date
#Nested loops by year and month
isProduction = True

#Need to read a CSV file| lookup each account| then output the same data with "Country" added.


#set the attributes for production or staging Aria
if isProduction:
    # Point to Production

    ariaoutfile = 'isRelayacct--prod.csv' #setting the file variable to store the output of the API call
    readfile = 'input-files/relayProd.csv'

    clientID= '5747004'
    auth= 'HBAETeMpu3Hn9nmQgD9dtnaMQtWqGfFG'
    ariaCoreUrl= 'https://secure.ariasystems.net/api/ws/api_ws_class_dispatcher.php'
    #ariaObjectURL = 'XXXhttps://secure.ariasystems.net/api/AriaQuery/objects.php'
    #ariaAdminURL = 'XXXhttps://admintools.ariasystems.net/index.php/Dispatcher/index'
    #              ^Remove XXX if ready to update - extra safety measure to prevent accidental update
    #Set Update Flags: True will enable; False Disable.  Revert will repopulate old LHGUID using same existing file. Should always retain orginal to get back to original values.

else:
    # Point to Staging
    clientID = '4934683'
    auth = 'DtcWUTxMYSySytSMtAerN3H67be5mH5n'
    ariaCoreUrl = 'https://secure.future.stage.ariasystems.net/api/ws/api_ws_class_dispatcher.php' #core URL
    #ariaObjectURL = 'XXXhttps://secure.future.stage.ariasystems.net/api/AriaQuery/objects.php'
    #ariaAdminURL = 'xxxhttps://admintools.future.stage.cph.ariasystems.net/AdminTools.php/Dispatcher'
    ariaoutfile = 'isRelayacct--staging.csv' #setting the file variable to store the output of the API call
    #changefile = 'newrates.txt'
    readfile = 'input-files/relayProd.csv'

#using two methods to check for the file.
if os.path.isfile(ariaoutfile):
    print('path was found to file')




#Execute the call to Aria to pull accounts based on a date range and write them to the file defined in ariaoutfile variable
#include an account number
def callAria ():
#This function calls the get_acct_plans Aria API to retrieve all the plan and rate data on the account
#It parses the output and builds a text file with the data necessary to build a load file for the modify plan rates call
    with open(ariaoutfile, 'w') as outfile:

        infile1 = open(readfile, 'r')
        writestring = 'Acct,Status,isRelay' + '\n'
        outfile.write(writestring)
        bloop = -1

        for line in reader(infile1):
            acct, status = line

            if bloop > -1:

                # set the URL with the account number for the lookup
                ariaGetAcctUrl = ariaCoreUrl + '?client_no=' + clientID + '&auth_key=' + auth + '&rest_call=get_acct_plans_all&acct_no='+str(acct)+'&output_format=json'

                # Execute the API call
                print(ariaGetAcctUrl+'\n')
                response2 = requests.get(ariaGetAcctUrl)

                # copy the json response to a dictionary
                response_dict = response2.json()

                # copy the account plan records for the Get account plans all API to a dictionary
                resp_dict = response_dict['all_acct_plans']
                #print(resp_dict)
                # Determine the number of plans returned
                j = len(resp_dict)
                print('the length is: ' + str(j))
                # set a variable for using as an index in the for loop below for dictionary reference| and increment at the end
                b = 0

                if j > 1:
                    print('has a supp plan')

                    vsuppPlanIndicator = 'None'

                    # loop through the response records
                    for i in resp_dict:
                        print(str(b))


                        vclientPlanID = resp_dict[b]['client_plan_id']
                        vsuppPlanIndicator = resp_dict[b]['supp_plan_ind']
                        vsuppPlanStatus = resp_dict[b]['supp_plan_status_cd']
                        print(str(vsuppPlanIndicator))
                        print(vclientPlanID)
                        writestring = str(acct)+','+status+','
                        if vsuppPlanIndicator == 1:
                            if "Relay_" in vclientPlanID:
                                writestring = writestring+'y,'+vclientPlanID+'\n'
                                outfile.write(writestring)
                            else:
                                writestring = writestring+'\n'
                                outfile.write(writestring)
                            break






            # Increment the indexing variable| and continue the loop
                        b = b + 1
                else:
                    writestring = str(acct) + ',' + status + ',\n'
                    outfile.write(writestring)
            bloop = bloop + 1





callAria()

#modRates()
