import requests
import datetime
import sys
from datetime import date
from datetime import time
# from datetime import datetime
from csv import reader
from pathlib import Path
import os.path

isProduction = True #Need to Add a loop for year and month to build the output file, otherwise the query for payment method takes too long and times out

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
ariaGetAcctUrl= ariaCoreUrl + '?client_no=' + clientID + '&auth_key=' + auth + '&rest_call=get_acct_invoice_history&acct_no='
#UKariaGetAcctUrl=ariaCoreURL + '?client_no=' + UKclientID + '&auth_key=' + UKauth + '&rest_call=get_acct_details_all&acct_no='
#AUariaGetAcctUrl=ariaCoreURL + '?client_no=' + AUclientID + '&auth_key=' + AUauth + '&rest_call=get_acct_details_all&acct_no='


#ariaGetAcctUrl= ariaObjectURL + '?client_no=' + clientID + '&auth_key=' + auth + '&rest_call=get_account_details&query_string=where pay_method = 14 or pay_method = 29&output_format=json'

#ariaGetAcctUrl= ariaObjectURL + '?client_no=' + clientID + '&auth_key=' + auth + '&rest_call=get_account_details&query_string=where pay_method = 14&output_format=json'

if os.path.isfile(ariaoutfile):
    print('path was found to file')

my_file = Path(ariaoutfile)
if my_file.is_file():
    print('it is here')
    # file exists
else:
    print('not found')
    set_title= open(ariaoutfile,'a+')
    set_title.write('accountType|accountNumber|seniorAccountNumber|invoice_no|bill_date|debit|credit'+ '\n')
    set_title.close()

#print(ariaGetAcctUrl)
#Execute the API call

#response2=requests.get(ariaGetAcctUrl)
#response_dict= response2.json()

#print(response_dict.keys())

#writeout='name,uuid,aria_us_id,aria_uk_id,aria_can_id,aria_au_id,country\n'
#fout.write(writeout)

#UKariaGetAcctUrl = UKariaGetAcctUrl+str(46302395)+'&output_format=json'
#response2 = requests.get(UKariaGetAcctUrl)
#response_dict = response2.json()
#print(response_dict['country'])
accountType = 'None'
accountNumber = 'None'
seniorAccountNumber = 'None'
invoice_no = 'None'
bill_date = 'None'
getbilldate = 'None'
debitamt = 'None'
creditamt = 'None'

with open(ariaoutfile, 'a+') as outfile:
    for line in reader(f2,delimiter='|'):
        accountType, accountNumber, seniorAccountNumber = line
        usurl = ''
        print(accountType,accountNumber,seniorAccountNumber)

        if accountType == 'A3':
          getbilldate = '2017-06-05'

        elif accountType == 'A2':
          getbilldate = '2017-04-08'

        usurl = ariaGetAcctUrl + str(accountNumber) + '&start_bill_date=' + getbilldate + '&output_format=json'
        print(usurl)
        #print ('passed A2 check')
        if accountType == 'A2' or accountType == 'A3':
            if accountNumber != 'NULL':

                #print('US ID: '+str(aria_us_id))
                response2 = requests.get(usurl)
                response_dict = response2.json()
                print(response_dict)
                resp_dict = response_dict['invoice_history']
                # print(resp_dict)
                # Determine the number of accounts returned
                if resp_dict != None:
                    j = len(resp_dict)
                    print('the length is: ' + str(j))

                    # set a variable for using as an index in the for loop below for dictionary reference| and increment at the end
                    b = 0

                    # loop through the response records
                    for i in resp_dict:
                        invoice_no = resp_dict[b]['invoice_no']
                        bill_date = resp_dict[b]['bill_date']
                        debitamt = resp_dict[b]['debit']
                        creditamt = resp_dict[b]['credit']
                        #if response_dict['country'] != None:
                            # country = response_dict['country']
                        outfile.write(str(accountType)+'|'+str(accountNumber)+'|'+str(seniorAccountNumber)+'|'+str(invoice_no)+'|'+str(bill_date)+'|'+str(debitamt)+'|'+str(creditamt)+'\n')
                        print(str(accountType)+','+str(accountNumber)+','+str(seniorAccountNumber)+','+str(invoice_no)+'\n')
                        b=b+1


f2.close()

"""
response2=requests.get(ariaGetAcctUrl)

#copy the json response to a dictionary
response_dict= response2.json()

#copy the account detail records for the Get account Details API to a dictionary
resp_dict=response_dict['account_details']

#Determine the number of accounts returned
j=len(resp_dict)
print('the length is: '+str(j))

#Open the output file for writing based on variables in the production / staging check above
with open(ariaoutfile, 'w+') as outfile:

    #write the header line to the file
    outfile.write('acct_no|senior_acct_no|pay_method|BPN|Product_Family|Okta_ID|BillAgreementID|Company|Firstname|Lastname|Country|Material_ID|Material_Description\n')

    #set a variable for using as an index in the for loop below for dictionary reference, and increment at the end
    b=0

    #loop through the response records
    for i in resp_dict:
        print(i)
        #outfile.write(str(resp_dict[b]['acct_no'])+'|'+str(resp_dict[b]['senior_acct_no'])+'|'+str(resp_dict[b]['pay_method'])+'\n')
        print(str(resp_dict[b]['acct_no'])+'|'+str(resp_dict[b]['senior_acct_no'])+'|'+str(resp_dict[b]['pay_method'])+'\n')

        #Set dictionaries for the supplemental field list and the current billing info blocks
        z = resp_dict[b]['supp_field']
        y = resp_dict[b]['current_billing_info']
        print(str(b))

        #Start building the string to write to the file
        writestring=str(resp_dict[b]['acct_no'])+'|'+str(resp_dict[b]['senior_acct_no'])+'|'+str(resp_dict[b]['pay_method'])

        #Set index counter variables for the supplemental field and billing dictionaries
        c=len(z)
        d=len(y)

        #Default some variables for the output
        SBPN='None'
        ProductFam='None'
        materialID='None'
        materialDescription='None'
        Okta='None'
        firstname='None'
        lastname='None'
        email='None'
        company='None'
        country='US'

        #pull the bill agreement ID into a variable, clearer than doing inline during the string build
        BillAgree=y[d-1]['billing_agreement_id']

        #Look for specifict supplemental fields, then store the values overwriting the variables above
        for k in range(c):
            if z[k]['supp_field_name'] == 'BPN':
                print('BPN: '+str(z[k]['supp_field_value']))
                SBPN = str(z[k]['supp_field_value'])
            if z[k]['supp_field_name'] == 'Product_Family':
                print('Prod Family: '+str(z[k]['supp_field_value']))
                ProductFam = str(z[k]['supp_field_value'])
            if z[k]['supp_field_name'] == 'Material_ID':
                print('Material_ID: ' + str(z[k]['supp_field_value']))
                materialID = str(z[k]['supp_field_value'])
            if z[k]['supp_field_name'] == 'Material_Description':
                print('Material_Description: ' + str(z[k]['supp_field_value']))
                materialDescription = str(z[k]['supp_field_value'])

            # print(str(resp_dict[b]['supp_field_name']))
        #When the items below are not of TYPE None, then store the value to the variable overwriting the default above
        if resp_dict[b]['client_acct_id'] != None:
            Okta=resp_dict[b]['client_acct_id']
        if resp_dict[b]['company_name'] != None:
            company=resp_dict[b]['company_name']
        if resp_dict[b]['first_name'] != None:
            firstname=resp_dict[b]['first_name']
        if resp_dict[b]['last_name'] != None:
            lastname=resp_dict[b]['last_name']

        #Finalize the output string
        writestring=writestring+'|'+SBPN+'|'+ProductFam+'|'+Okta+'|'+str(BillAgree)+'|'+company+'|'+firstname+'|'+lastname+'|'+country+'|'+materialID+'|'+materialDescription+'|'+'\n'
        print(writestring)

        #Only want V1 payment information, so check if the material id is set for a payment key '9x' or a Canadian account 'CA', and if so exclude.
        if materialID != '9x' or 'CA':
            outfile.write(writestring)

        #Increment the indexing variable, and continue the loop
        b = b + 1


#print(response_dict.keys())
#print('\n')
#print (response_dict['account_details'][0])


#if response_dict['total_records'] > 0:
 #   print('records were found: '+str(response_dict['total_records']))
#    with open("ariaAccountDetails.txt", 'w+') as outfile:
 #       for i in response_dict:
            #acct_no,senior_acct_no,user_id,password,status_cd,plan_no,first_name,mi,last_name,address_1,address_2,city,locality,postal_code,country,phone_npa,phone_nxx,phone_suffic,phone_extension,intl_phone,alt_email,client_acct_id,promo_cd,resp_level_cd,pay_method,created,last_updated,client_1,company_name,billing_first_name,billing_middle_initial,billing_last_name,billing_address1,billing_address2,billing_city,billing_state,billing_locality,billing_zip,billing_country,billing_phone_npa,billing_phone_nxx,billing_phone_suffix,billing_phone_extension,billing_intl_phone,billing_email,billing_pay_method,billing_cc_expire_mm,billing_cc_expire_yyyy,billing_bank_routing_num,billing_agreement_id,plan_name,state_prov,country_english,promo_name,no_provision_ind,bill_action_cd,status_name,acct_balance,supp_field,bill_day,supp_plan,invoice_posting_method_cd,acct_start_date,pay_method_name,External_Payment = i
  #          print(response_dict[i])
"""
 #           """accountnum=response_dict['acct_no'].title()
 #           senioracct=response_dict['senior_acct_no']
 #           supplementalplan=response_dict['supp_plan']
  #          paymenttype=response_dict['payment_method']"""
            #outfile.write(str(acct_no)+'|'+str(senior_acct_no)+'|'+str(supp_plan)+'|'+str(payment_method))

#else:
#    print(len(response_dict))

"""
updateAria = False
# updateAria=True (BECAREFUL using True)
revert = False
# revert=True (BECAREFUL  using True)
"""

appName = 'GetAccountDetails Query'
# processDate='2017/02/09'
processDate = date.today()
print('The process date is: ' + str(processDate))

"""
if revert:
    appName = appName + 'Revert'
    print(appName)

appStartTime = datetime.datetime.now()
print()
print("Update Aria Okta and LH IDs Started: ", appStartTime)
print()

N=10
with open("allAcctAnalysis.txt") as myfile:
    head = [next(myfile) for x in range(N)]
print (head)"""