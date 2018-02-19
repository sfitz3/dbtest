import requests
import sys
import datetime




i = 0
years = 1

#Since this is a large extract, loop through calls using the account creation date
#Nested loops by year and month
isProduction = False

#Need to read a CSV file, lookup each account, then output the same data with "Country" added.


#set the attributes for production or staging Aria
if isProduction:
    # Point to Production

    ariaoutfile = 'ariaAccounts-looper-Prod.txt'

    clientID= '5747004'
    auth= 'HBAETeMpu3Hn9nmQgD9dtnaMQtWqGfFG'
    ariaCoreUrl= 'XXXhttps://secure.ariasystems.net/api/ws/api_ws_class_dispatcher.php'
    #ariaObjectURL = 'https://secure.ariasystems.net/api/AriaQuery/objects.php'
    #ariaAdminURL = 'XXXhttps://admintools.ariasystems.net/index.php/Dispatcher/index'
    #              ^Remove XXX if ready to update - extra safety measure to prevent accidental update
    #Set Update Flags: True will enable; False Disable.  Revert will repopulate old LHGUID using same existing file. Should always retain orginal to get back to original values.

else:
    # Point to Staging
    clientID = '4934683'
    auth = 'DtcWUTxMYSySytSMtAerN3H67be5mH5n'
    ariaCoreUrl = 'https://secure.future.stage.ariasystems.net/api/ws/api_ws_class_dispatcher.php' #core URL
    #ariaObjectURL = 'xxxhttps://secure.future.stage.ariasystems.net/api/AriaQuery/objects.php'
    #ariaAdminURL = 'xxxhttps://admintools.future.stage.cph.ariasystems.net/AdminTools.php/Dispatcher'
    ariaoutfile = 'ariaAccounts-looper-staging.txt'
#              ^Remove XXX if ready to update - extra safety measure to prevent accidental update
# Set Update Flags: True will enable; False Disable.  Revert will repopulate old LHGUID using same existing file. Should always retain orginal to get back to original values.




#Execute the call to Aria to pull accounts based on a date range and write them to the file defined in ariaoutfile variable
def callAria (e_date):
    with open(ariaoutfile, 'a+') as outfile:

        # write the header line to the file
        #outfile.write('status|acct_no|senior_acct_no|pay_method|created date|BPN|Product_Family|Okta_ID|BillAgreementID|Company|Firstname|Lastname|Country|Material_ID|Material_Description\n')

        # set the URL with the date for the query
        ariaGetAcctUrl = ariaCoreUrl + '?client_no=' + clientID + '&auth_key=' + auth + '&rest_call=get_acct_details_all&acct_no=23024080&output_format=json'
        # Execute the API call
        print(ariaGetAcctUrl+'\n')
        response2 = requests.get(ariaGetAcctUrl)

        # copy the json response to a dictionary
        response_dict = response2.json()
        print(response_dict['notify_method'])

        # copy the account detail records for the Get account Details API to a dictionary
        #resp_dict = response_dict['account_details']
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
            writestring = str(resp_dict[b]['status_cd']) + '|' + str(resp_dict[b]['acct_no']) + '|' + str(resp_dict[b]['senior_acct_no']) + '|' + str(
                resp_dict[b]['pay_method'])+'|'+str(resp_dict[b]['created'])

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
            if SBPN != 'None':
                outfile.write(writestring)

            # Increment the indexing variable, and continue the loop
            b = b + 1

#Function to process the data range used in the Get Account Details call to Aria
def datelooper(i,years,startyear):
    callingdate=datetime.date(startyear,1,1)
    m=0
    #while m<(365*years):
    while m < (1 * 1):
        a_year=callingdate.timetuple().tm_year
        a_month=callingdate.timetuple().tm_mon
        a_day=callingdate.timetuple().tm_mday
        a_date=str(a_month)+'/'+str(a_day)+'/'+str(a_year)
        callAria(a_date)
        callingdate=callingdate+datetime.timedelta(days=1)
        m=m+1




#start the lookup process, 0 is counter start, number of years, starting year
datelooper(0,1,2017)
