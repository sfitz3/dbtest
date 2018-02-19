import requests
import sys
import datetime
from pathlib import Path
import os.path
from csv import reader


#Custom Rates on account for SPOD 24852080 (staging)

#prod account with many invoices: 39955162


i = 0
years = 1
#filepath = 'Desktop/Python2/'

#Since this is a large extract| loop through calls using the account creation date
#Nested loops by year and month
isProduction = True

#Need to read a CSV file| lookup each account| then output the same data with "Country" added.


#set the attributes for production or staging Aria
if isProduction:
    # Point to Production

    ariaoutfile = 'ariaCustRatesAccount--Prod.txt'

    clientID= '5747004'
    auth= 'HBAETeMpu3Hn9nmQgD9dtnaMQtWqGfFG'
    ariaCoreUrl= 'https://secure.ariasystems.net/api/ws/api_ws_class_dispatcher.php'
    #ariaObjectURL = 'XXXhttps://secure.ariasystems.net/api/AriaQuery/objects.php'
    #ariaAdminURL = 'XXXhttps://admintools.ariasystems.net/index.php/Dispatcher/index'
    #              ^Remove XXX if ready to update - extra safety measure to prevent accidental update
    #Set Update Flags: True will enable; False Disable.  Revert will repopulate old LHGUID using same existing file. Should always retain orginal to get back to original values.
    ariaoutfile = 'ariaA3creditbalance--prod.csv'
    chkbalance = 'chkbalanceA3.csv'
else:
    # Point to Staging
    clientID = '4934683'
    auth = 'DtcWUTxMYSySytSMtAerN3H67be5mH5n'
    ariaCoreUrl = 'https://secure.future.stage.ariasystems.net/api/ws/api_ws_class_dispatcher.php' #core URL
    #ariaObjectURL = 'XXXhttps://secure.future.stage.ariasystems.net/api/AriaQuery/objects.php'
    #ariaAdminURL = 'xxxhttps://admintools.future.stage.cph.ariasystems.net/AdminTools.php/Dispatcher'
    ariaoutfile = 'ariaA3creditbalance--staging.csv' #setting the file variable to store the output of the API call
    changefile = 'newrates.txt'
    chkbalance = 'chkbalanceA3.csv'
    #ariaoutfileratesup = 'ariaRatesChanged--staging.txt'
#              ^Remove XXX if ready to update - extra safety measure to prevent accidental update
# Set Update Flags: True will enable; False Disable.  Revert will repopulate old LHGUID using same existing file. Should always retain orginal to get back to original values.

#filepath = filepath + ariaoutfile

#checking for the output file in the same path as the code.  If it exists| don't write the header| otherwise create and write header.
#using two methods to check for the file.
#if os.path.isfile(ariaoutfile):
    print('path was found to file')

#my_file = Path(ariaoutfile)
#if my_file.is_file():
 #   print('it is here')
    # file exists
#else:
  #  print('not found')
   # set_title= open(ariaoutfile,'a+')
    #set_title.write('Account|acctPlanArrayLnth|clientPlanID|lastBillDate|nextBillDate|billThroughDate|PlanSrvCount|SrvNo|clientSrvID|IsRecurring|IsUsage|usageType|usageTypeName|rateSchedNum|clientRateSchedID|rateSchedName|isDefaultSched|suppPlanInd|planSrvRatesCount|rateSeqNo|fromUnit|toUnit|ratePerUnit|'+ '\n')

    #set_title.close()


#Execute the call to Aria to pull accounts based on a date range and write them to the file defined in ariaoutfile variable
#include an account number
def callAria ():
#This function calls the get_acct_plans Aria API to retrieve all the plan and rate data on the account
#It parses the output and builds a text file with the data necessary to build a load file for the modify plan rates call
    with open(ariaoutfile, 'w') as outfile:
        infile1 = open(chkbalance, 'r')
        bloop = -1


        ariaGetCredits = ariaCoreUrl + '?client_no=' + clientID + '&auth_key=' + auth + '&rest_call=get_unapplied_service_credits&acct_no='
        writeline = 'acct,userid,trandate,payid,amt,currency,acctlvl,product,key,bpn,creditbalance\n'
        outfile.write(writeline)

        for line in reader(infile1):
            acct,userid,trandate,payid,amt,currency,acctlvl,product,key,bpn=line
            writeline=''

            if bloop > -1:
                getdatastring = ariaGetCredits + str(acct)+'&output_format=json'
                #call Aria to retrieve the balances
                print(getdatastring)
                response2 = requests.get(getdatastring)
                response_dict = response2.json()
                if response_dict['unapplied_service_credits']!= None:
                    resp_dict = response_dict['unapplied_service_credits']

                    j = len(resp_dict)
                    print('the length is: ' + str(j))

                    # set a variable for using as an index in the for loop below for dictionary reference| and increment at the end
                    b = 0
                    creditbalance = 0
                    for i in resp_dict:

                        availbalance =resp_dict[b]['amount_left_to_apply']
                        #print(availbalance)
                        creditbalance = creditbalance + availbalance
                        print(round(creditbalance,2))
                        b=b+1


                    writeline=str(acct)+","+str(userid)+","+str(trandate)+","+str(payid)+","+str(amt)+","+str(currency)+","+str(acctlvl)+","+str(product)+","+str(key)+','+str(bpn)+','+str(round(creditbalance,2))+ '\n'
                    outfile.write(writeline)

            bloop = bloop + 1


        #with open(ariaoutfileratesup, 'w') as outfile2:
             #outfile2.write('Acct|clientPID|RateSchedNum|RateSrvNo|Recurring|Usage|SeqNo|fromU|toU|rtPerU|' + '\n')  #start the lookup process
#parameters are the account to retrieve  ** if you need date manipulation look at "looptest.py" for examples

#lacct = "23024106"


callAria()



