import datetime
import requests
import sys
from csv import reader
from datetime import date
from datetime import time




#Since this is a large extract, loop through calls using the account creation date
#Nested loops by year and month
isProduction = False

#Need to read a CSV file, lookup each account, then output the same data with "Country" added.


#set the attributes for production or staging Aria
if isProduction:
    # Point to Production

    ariaoutfile = 'ariaAccounts-with-paytype-Prod.txt'

    clientID= '5747004'
    auth= 'HBAETeMpu3Hn9nmQgD9dtnaMQtWqGfFG'
    #ariaCoreUrl= 'XXXhttps://secure.ariasystems.net/api/ws/api_ws_class_dispatcher.php'
    ariaObjectURL = 'https://secure.ariasystems.net/api/AriaQuery/objects.php'
    #ariaAdminURL = 'XXXhttps://admintools.ariasystems.net/index.php/Dispatcher/index'
    #              ^Remove XXX if ready to update - extra safety measure to prevent accidental update
    #Set Update Flags: True will enable; False Disable.  Revert will repopulate old LHGUID using same existing file. Should always retain orginal to get back to original values.

else:
    # Point to Staging
    clientID = '4934683'
    auth = 'DtcWUTxMYSySytSMtAerN3H67be5mH5n'
    #ariaCoreUrl = 'XXXhttps://secure.future.stage.ariasystems.net/api/ws/api_ws_class_dispatcher.php' #core URL
    ariaObjectURL = 'https://secure.future.stage.ariasystems.net/api/AriaQuery/objects.php'
    #ariaAdminURL = 'xxxhttps://admintools.future.stage.cph.ariasystems.net/AdminTools.php/Dispatcher'
    ariaoutfile = 'ariaAccounts-with-paytype-staging.txt'
#              ^Remove XXX if ready to update - extra safety measure to prevent accidental update
# Set Update Flags: True will enable; False Disable.  Revert will repopulate old LHGUID using same existing file. Should always retain orginal to get back to original values.



#core API
#ariaURL2 = ariaEndPoint + '?client_no=' + clientID + '&auth_key=' + auth + '&rest_call=update_acct_complete&acct_no=' + str(
#    ACCT_NO) + '&client_acct_id=' + GuamOkta + '&application_id=' + appName + '&application_date=' + processDate + '&output_format=json'


#object API
#Example query string: query_string=where status_cd = 1 and supp_field_name = Product_Family and supp_field_value = PBSP

#ariaGetAcctUrl= ariaObjectURL + '?client_no=' + clientID + '&auth_key=' + auth + '&rest_call=get_account_details&query_string=where last_name = Marley&output_format=json'


#ariaGetAcctUrl= ariaObjectURL + '?client_no=' + clientID + '&auth_key=' + auth + '&rest_call=get_account_details&query_string=where pay_method = 14&output_format=json'

#print(ariaGetAcctUrl)

def callAria (calldata):
    # Execute the API call
    response2 = requests.get(calldata)

    # copy the json response to a dictionary
    response_dict = response2.json()

    # copy the account detail records for the Get account Details API to a dictionary
    resp_dict = response_dict['account_details']
    # print(resp_dict)
    # Determine the number of accounts returned
    j = len(resp_dict)
    print('the length is: ' + str(j))

    # set a variable for using as an index in the for loop below for dictionary reference, and increment at the end
    b = 0

    # loop through the response records
    for i in resp_dict:
        print(i)
        # outfile.write(str(resp_dict[b]['acct_no'])+'|'+str(resp_dict[b]['senior_acct_no'])+'|'+str(resp_dict[b]['pay_method'])+'\n')
        print(str(resp_dict[b]['acct_no']) + '|' + str(resp_dict[b]['senior_acct_no']) + '|' + str(
            resp_dict[b]['pay_method']) + '\n')

        # Set dictionaries for the supplemental field list and the current billing info blocks
        z = resp_dict[b]['supp_field']
        y = resp_dict[b]['current_billing_info']
        print(str(b))

        # Start building the string to write to the file
        writestring = str(resp_dict[b]['acct_no']) + '|' + str(resp_dict[b]['senior_acct_no']) + '|' + str(
            resp_dict[b]['pay_method'])

        # Set index counter variables for the supplemental field and billing dictionaries
        c = len(z)
        d = len(y)

        # Default some variables for the output
        SBPN = 'None'
        ProductFam = 'None'
        materialID = 'None'
        materialDescription = 'None'
        Okta = 'None'
        firstname = 'None'
        lastname = 'None'
        email = 'None'
        company = 'None'
        country = 'US'

        # pull the bill agreement ID into a variable, clearer than doing inline during the string build
        BillAgree = y[d - 1]['billing_agreement_id']

        # Look for specifict supplemental fields, then store the values overwriting the variables above
        for k in range(c):
            if z[k]['supp_field_name'] == 'BPN':
                print('BPN: ' + str(z[k]['supp_field_value']))
                SBPN = str(z[k]['supp_field_value'])
            if z[k]['supp_field_name'] == 'Product_Family':
                print('Prod Family: ' + str(z[k]['supp_field_value']))
                ProductFam = str(z[k]['supp_field_value'])
            if z[k]['supp_field_name'] == 'Material_ID':
                print('Material_ID: ' + str(z[k]['supp_field_value']))
                materialID = str(z[k]['supp_field_value'])
            if z[k]['supp_field_name'] == 'Material_Description':
                print('Material_Description: ' + str(z[k]['supp_field_value']))
                materialDescription = str(z[k]['supp_field_value'])

                # print(str(resp_dict[b]['supp_field_name']))
        # When the items below are not of TYPE None, then store the value to the variable overwriting the default above
        if resp_dict[b]['client_acct_id'] != None:
            Okta = resp_dict[b]['client_acct_id']
        if resp_dict[b]['company_name'] != None:
            company = resp_dict[b]['company_name']
        if resp_dict[b]['first_name'] != None:
            firstname = resp_dict[b]['first_name']
        if resp_dict[b]['last_name'] != None:
            lastname = resp_dict[b]['last_name']

        # Finalize the output string
        writestring = writestring + '|' + SBPN + '|' + ProductFam + '|' + Okta + '|' + str(
            BillAgree) + '|' + company + '|' + firstname + '|' + lastname + '|' + country + '|' + materialID + '|' + materialDescription + '|' + '\n'
        print(writestring)

        # Only want V1 payment information, so check if the material id is set for a payment key '9x' or a Canadian account 'CA', and if so exclude.
        if materialID != '9x' or 'CA':
            outfile.write(writestring)

        # Increment the indexing variable, and continue the loop
        b = b + 1



#Open the output file for writing based on variables in the production / staging check above
with open(ariaoutfile, 'w+') as outfile:

    #write the header line to the file
    outfile.write('acct_no|senior_acct_no|pay_method|BPN|Product_Family|Okta_ID|BillAgreementID|Company|Firstname|Lastname|Country|Material_ID|Material_Description\n')


        #set the URL with the date for the query
    ariaGetAcctUrl = ariaObjectURL + '?client_no=' + clientID + '&auth_key=' + auth + '&rest_call=get_account_details&query_string=where supp_field_name[0]=Product_Family and supp_field_name[0] = Horizon and pay_method = 14&output_format=json'
    callAria(ariaGetAcctUrl)
    ariaGetAcctUrl = ariaObjectURL + '?client_no=' + clientID + '&auth_key=' + auth + '&rest_call=get_account_details&query_string=where supp_field_name[0]=Product_Family and supp_field_name[0] = Horizon and pay_method = 29&output_format=json'
    callAria(ariaGetAcctUrl)


        #d = datetime.datetime.strptime(s, '%m/%d/%Y') + datetime.timedelta(days=1)
        #print(d.strftime('%m/%d/%Y'))


#print(response_dict.keys())
#print('\n')
#print (response_dict['account_details'][0])


#if response_dict['total_records'] > 0:
 #   print('records were found: '+str(response_dict['total_records']))
#    with open("ariaAccountDetails.txt", 'w+') as outfile:
 #       for i in response_dict:
            #acct_no,senior_acct_no,user_id,password,status_cd,plan_no,first_name,mi,last_name,address_1,address_2,city,locality,postal_code,country,phone_npa,phone_nxx,phone_suffic,phone_extension,intl_phone,alt_email,client_acct_id,promo_cd,resp_level_cd,pay_method,created,last_updated,client_1,company_name,billing_first_name,billing_middle_initial,billing_last_name,billing_address1,billing_address2,billing_city,billing_state,billing_locality,billing_zip,billing_country,billing_phone_npa,billing_phone_nxx,billing_phone_suffix,billing_phone_extension,billing_intl_phone,billing_email,billing_pay_method,billing_cc_expire_mm,billing_cc_expire_yyyy,billing_bank_routing_num,billing_agreement_id,plan_name,state_prov,country_english,promo_name,no_provision_ind,bill_action_cd,status_name,acct_balance,supp_field,bill_day,supp_plan,invoice_posting_method_cd,acct_start_date,pay_method_name,External_Payment = i
  #          print(response_dict[i])

 #           """accountnum=response_dict['acct_no'].title()
 #           senioracct=response_dict['senior_acct_no']
 #           supplementalplan=response_dict['supp_plan']
  #          paymenttype=response_dict['payment_method']"""
            #outfile.write(str(acct_no)+'|'+str(senior_acct_no)+'|'+str(supp_plan)+'|'+str(payment_method))

#else:
#    print(len(response_dict))



appName = 'GetAccountDetails Query'
# processDate='2017/02/09'
processDate = date.today()
print('The process date is: ' + str(processDate))

