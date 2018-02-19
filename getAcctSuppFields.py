import requests
import sys
import datetime
from pathlib import Path
import os.path
from csv import reader



i = 0
#years = 1
#filepath = 'Desktop/Python2/'


isProduction = False

#Need to read a CSV file| lookup each account| Check for Company Code


#set the attributes for production or staging Aria
if isProduction:
    # Point to Production

    ariaoutfile = 'isRelayacct--prod.csv' #setting the file variable to store the output of the API call
    #readfile = 'input-files/relayProd.csv' #input file for the account lookups

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
    ariaoutfile = 'updatedCompCode.csv' #setting the file variable to store the output of the API call
    #changefile = 'newrates.txt'
    #readfile = 'LBSacctStage.csv'
    #readfile = 'geoaccts.csv' #input file for the account lookups

#using two methods to check for the file.
if os.path.isfile(ariaoutfile):
    print('path was found to file')




#Execute the call to Aria to pull accounts

def callAria (readfile,nCC):
#This function calls the get_acct_supp_fields Aria API to retrieve all supplemental fields defined
#It will update company code based on varialble nCC to a new company code, either as a new supp field or update of populated one
    with open(ariaoutfile, 'a+') as outfile:

        infile1 = open(readfile, 'r')
        writestring = 'Acct,Old CC,New CC,Date Updated\n' #put in file header
        outfile.write(writestring)
        bloop = -1 #loop variable

        for line in reader(infile1):
            acct, junk = line

            if bloop > -1: #ignore the first row of the file, it is header text

                # set the URL with the account number for the lookup
                ariaGetAcctUrl = ariaCoreUrl + '?client_no=' + clientID + '&auth_key=' + auth + '&rest_call=get_acct_supp_fields&acct_no='+str(acct)+'&output_format=json'

                # Execute the API call
                print(ariaGetAcctUrl+'\n')
                response2 = requests.get(ariaGetAcctUrl)

                # copy the json response to a dictionary
                response_dict = response2.json()

                # copy the account supplemental fields array records for the Get acct supp fields API to a dictionary
                resp_dict = response_dict['supp_fields']

                # Determine the number of fields returned
                j = len(resp_dict)
                print('the length is: ' + str(j))
                # set a variable for using as an index in the for loop below for dictionary reference| and increment at the end
                b = 0

                if j > 1:


                    vsuppPlanIndicator = 'None'
                    vfoundit = False
                    vCC = None #original CompanyCode on the account
                    #nCC = 2570 New CompanyCode being assigned to the account
                    # loop through the response records
                    for i in resp_dict:
                        print(str(b))
                        print(resp_dict[b])
                        if resp_dict[b]['field_name'] == 'CompanyCode':
                            vfoundit = True
                            vCC = resp_dict[b]['field_value']
                        b = b + 1

                    if vfoundit :
                        print('companyCode defined')
                        if vCC != '2570':
                            print('wrong CC, updating')
                            ariaPutAcctUrl = ariaCoreUrl + '?client_no=' + clientID + '&auth_key=' + auth + '&rest_call=update_acct_complete&acct_no=' + str(acct) + '&supp_field_directives[0]=2&supp_field_names[0]=CompanyCode&supp_field_values[0]='+str(vCC)+'&output_format=json'

                            print(ariaPutAcctUrl)
                            response3 = requests.post(ariaPutAcctUrl) #update the CC on the account
                            i=datetime.datetime.now()

                            w='%s/%s/%s' %(i.month,i.day,i.year)

                            print(w)

                            writestring = str(acct)+','+str(vCC)+','+str(nCC)+','+str(w)+'\n'
                            print(writestring)
                            outfile.write(writestring) #log the account was updated
                    else:
                        print('Nope')
                        ariaPutAcctUrl = ariaCoreUrl + '?client_no=' + clientID + '&auth_key=' + auth + '&rest_call=update_acct_complete&acct_no=' + str(acct)+'&supp_field_directives[0]=1&supp_field_names[0]=CompanyCode&supp_field_values[0]='+str(vCC)+'&output_format=json'
                        print(ariaPutAcctUrl)
                        response3 = requests.post(ariaPutAcctUrl) #update the CC on the account
                        i = datetime.datetime.now()

                        w = '%s/%s/%s' % (i.month, i.day, i.year)

                        print(w)

                        writestring = str(acct) + ',None,'+str(nCC)+',' + str(w)+'\n'
                        print(writestring)
                        outfile.write(writestring) #log the account was updated

            # Increment the indexing variable| and continue the loop


            bloop = bloop + 1



inputfile = 'geoaccts.csv'
NewCompCode = 2570
callAria(inputfile,NewCompCode)


