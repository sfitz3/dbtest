import requests
import sys
import datetime
from pathlib import Path
import os.path




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

    ariaoutfile = 'ariaAccounts-all-Prod.txt'

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
    ariaoutfile = 'ariaAccounts-all-staging.txt'
#              ^Remove XXX if ready to update - extra safety measure to prevent accidental update
# Set Update Flags: True will enable; False Disable.  Revert will repopulate old LHGUID using same existing file. Should always retain orginal to get back to original values.

#filepath = filepath + ariaoutfile
#checking for the output file in the same path as the code.  If it exists| don't write the header| otherwise create and write header.
#using two methods to check for the file.
if os.path.isfile(ariaoutfile):
    print('path was found to file')

my_file = Path(ariaoutfile)
if my_file.is_file():
    print('it is here')
    # file exists
else:
    print('not found')
    set_title= open(ariaoutfile,'a+')
    set_title.write('status|acct_no|senior_acct_no|pay_method|created date|SBPN|ProductFam|PayMethod|Okta|MasterPlan|SuppPlan|BillAgree|company|firstname|lastname|email|country|materialID|materialDescription|GUID|PURCHASE_POWER|GEOCODE|Sales|Rep|CompanyCode|SalesOrg|DistributionChannel|Diision|BillingBPN|SAPsubscription|Name2|Name3|Guam_UserID|Guam_SubscriptionID|Tenant_ID|APIm_DeID|APIm_SubscriptionID|PCN|USPS_Serial_Number|EnterpriseFunded|EnterpriseA3|Enterprise|EnterpriseID|PrePay_Fund|Migrated_Account|SFDC_MCID|TaxClassCode|Mailcode'+ '\n')

    set_title.close()


#Execute the call to Aria to pull accounts based on a date range and write them to the file defined in ariaoutfile variable
def callAria (e_date1,e_date2):
    with open(ariaoutfile, 'a+') as outfile:

        # write the header line to the file
        #outfile.write('status|acct_no|senior_acct_no|pay_method|created date|BPN|Product_Family|Okta_ID|BillAgreementID|Company|Firstname|Lastname|Country|Material_ID|Material_Description\n')

        # set the URL with the date for the query
        #ariaGetAcctUrl = ariaObjectURL + '?client_no=' + clientID + '&auth_key=' + auth + '&rest_call=get_account_details&query_string=where created between '+ s_builddate +' and ' +e_builddate+' and status_cd=1 or status_cd=-1&output_format=json'
        ariaGetAcctUrl = ariaObjectURL + '?client_no=' + clientID + '&auth_key=' + auth + '&rest_call=get_account_details&query_string=where created >'+str(e_date1)+' and created <'+str(e_date2)+' and status_cd > -2&limit=20000&output_format=json'
        #ariaGetAcctUrl = ariaObjectURL + '?client_no=' + clientID + '&auth_key=' + auth + '&rest_call=get_account_details&query_string=where  &limit=1500&output_format=json'

        # Execute the API call
        print(ariaGetAcctUrl+'\n')
        response2 = requests.get(ariaGetAcctUrl)

        # copy the json response to a dictionary
        response_dict = response2.json()

        # copy the account detail records for the Get account Details API to a dictionary
        resp_dict = response_dict['account_details']
        # print(resp_dict)
        # Determine the number of accounts returned
        j = len(resp_dict)
        print('the length is: ' + str(j))

        # set a variable for using as an index in the for loop below for dictionary reference| and increment at the end
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
            f = resp_dict[b]['supp_plan']
            print(str(b))
            print(f)

            # Start building the string to write to the file
            writestring = str(resp_dict[b]['status_cd']) + '|' + str(resp_dict[b]['acct_no']) + '|' + str(resp_dict[b]['senior_acct_no']) + '|' + str(
                resp_dict[b]['pay_method'])+'|'+str(resp_dict[b]['created'])

            # Set index counter variables for the supplemental field and billing dictionaries
            c = len(z)
            d = len(y)
            if resp_dict[b]['supp_plan'] != None:
                g = len(f)
            else:
                g = -1

            # Default some variables for the output
            vSBPN = 'None'
            vProductFam = 'None'
            vmaterialID = 'None'
            vmaterialDescription = 'None'
            Okta = 'None'
            firstname = 'None'
            lastname = 'None'
            email = 'None'
            company = 'None'
            country = 'US'
            vED_EMAILS = 'None'
            vED_CONTACTS = 'None'
            vED_PLAN_TYPE = 'None'
            vCULTURE = 'None'
            vCOUPON_CODE = 'None'
            vCAN = 'None'
            vGUID = 'None'
            vPURCHASE_POWER = 'None'
            vCOUPON_CODE_APPLIED = 'None'
            vCancellation = 'None'
            vsystem = 'None'
            vaccess = 'None'
            vSC_Total_Campaigns = 'None'
            vSC_Active_Campaigns = 'None'
            vSC_Total_Edits = 'None'
            vSC_Plan_type = 'None'
            vGEOCODE = 'None'
            vpromocode4pbsconn = 'None'
            vpromocode4pbscode = 'None'
            vpromo4pbbundle = 'None'
            vSales = 'None'
            vRep = 'None'
            vpromocode4pbsmobile = 'None'
            vsm_plan_type = 'None'
            vsm_active_pages = 'None'
            vsm_total_drafts = 'None'
            vsm_active_sites = 'None'
            vaffiliate_membership_number = 'None'
            vCODES_COUPON_CODE = 'None'
            vMOBILES_COUPON_CODE = 'None'
            vinventorypromocode4pbsconn = 'None'
            vinventorypromocode4pbscode = 'None'
            vinventorypromocode4pbsmobile = 'None'
            vCompanyCode = 'None'
            vSalesOrg = 'None'
            vDistributionChannel = 'None'
            vDivision = 'None'
            vBillingBPN = 'None'
            vSAPsubscription = 'None'
            vName2 = 'None'
            vName3 = 'None'
            vGuam_UserID = 'None'
            vGuam_SubscriptionID = 'None'
            vTenant_ID = 'None'
            vAPIm_DevID = 'None'
            vAPIm_SubscriptionID = 'None'
            vPCN = 'None'
            vUSPS_Serial_Number = 'None'
            vEnterpriseFunded = 'None'
            vEnterpriseA3 = 'None'
            vMaterial_ID = 'None'
            vEnterprise = 'None'
            vEnterpriseID = 'None'
            vPrePay_Fund = 'None'
            vMigrated_Account = 'None'
            vPaymentKey = 'None'
            vSFDC_MCID = 'None'
            vTaxClassCode = 'None'
            vMailcode = 'None'
            vsupp_plan0 = 'None'
            vsupp_plan1 = 'None'
            vsupp_plan2 = 'None'
            vsupp_plan3 = 'None'
            vsupp_plan4 = 'None'
            vsupp_plan5 = 'None'
            vsupp_plan6 = 'None'
            vsupp_plan7 = 'None'
            vsupp_plan8 = 'None'
            vsupp_plan9 = 'None'
            vsupp_plan10 = 'None'
            vpay_method = 'None'
            # pull the bill agreement ID into a variable| clearer than doing inline during the string build
            BillAgree = y[d - 1]['billing_agreement_id']

            if g > -1:
                for l in range(g):
                    if l == 0:
                        vsupp_plan0=str(f[l]['supp_plan_no'])
                    if l == 1:
                        vsupp_plan1 = str(f[l]['supp_plan_no'])
                    if l == 2:
                        vsupp_plan2 = str(f[l]['supp_plan_no'])
                    if l == 3:
                        vsupp_plan3 = str(f[l]['supp_plan_no'])
                    if l == 4:
                        vsupp_plan4 = str(f[l]['supp_plan_no'])
                    if l == 5:
                        vsupp_plan5 = str(f[l]['supp_plan_no'])
                    if l == 6:
                        vsupp_plan6 = str(f[l]['supp_plan_no'])
                    if l == 7:
                        vsupp_plan7 = str(f[l]['supp_plan_no'])
                    if l == 8:
                        vsupp_plan8 = str(f[l]['supp_plan_no'])
                    if l == 9:
                        vsupp_plan9 = str(f[l]['supp_plan_no'])
                    if l == 10:
                        vsupp_plan10 = str(f[l]['supp_plan_no'])

            # Look for specific supplemental fields| then store the values overwriting the variables above
            for k in range(c):
                if z[k]['supp_field_name'] == 'BPN':
                    print('BPN: ' + str(z[k]['supp_field_value']))
                    vSBPN = str(z[k]['supp_field_value'])
                if z[k]['supp_field_name'] == 'Product_Family':
                    print('Prod Family: ' + str(z[k]['supp_field_value']))
                    vProductFam = str(z[k]['supp_field_value'])
                if z[k]['supp_field_name'] == 'Material_ID':
                    print('Material_ID: ' + str(z[k]['supp_field_value']))
                    vmaterialID = str(z[k]['supp_field_value'])
                if z[k]['supp_field_name'] == 'Material_Description':
                    print('Material_Description: ' + str(z[k]['supp_field_value']))
                    vmaterialDescription = str(z[k]['supp_field_value'])
                if z[k]['supp_field_name'] == 'GUID':
                    print('GUID: ' + str(z[k]['supp_field_value']))
                    vGUID = str(z[k]['supp_field_value'])
                if z[k]['supp_field_name'] == 'Purchase_Power':
                    print('Purchase Power: ' + str(z[k]['supp_field_value']))
                    vPURCHASE_POWER = str(z[k]['supp_field_value'])
                if z[k]['supp_field_name'] == 'GEOCODE':
                    print('GEOCODE: ' + str(z[k]['supp_field_value']))
                    vGEOCODE = str(z[k]['supp_field_value'])
                if z[k]['supp_field_name'] == 'Sales':
                    print('Sales: ' + str(z[k]['supp_field_value']))
                    vSales = str(z[k]['supp_field_value'])
                if z[k]['supp_field_name'] == 'Rep':
                    print('Rep: ' + str(z[k]['supp_field_value']))
                    vRep = str(z[k]['supp_field_value'])
                if z[k]['supp_field_name'] == 'CompanyCode':
                    print('Company Code: ' + str(z[k]['supp_field_value']))
                    vCompanyCode = str(z[k]['supp_field_value'])
                if z[k]['supp_field_name'] == 'SalesOrg':
                    print('SalesOrg: ' + str(z[k]['supp_field_value']))
                    vSalesOrg = str(z[k]['supp_field_value'])
                if z[k]['supp_field_name'] == 'DistributionChannel':
                    print('Distribution Channel: ' + str(z[k]['supp_field_value']))
                    vDistributionChannel = str(z[k]['supp_field_value'])
                if z[k]['supp_field_name'] == 'Division':
                    print('Division: ' + str(z[k]['supp_field_value']))
                    vDivision = str(z[k]['supp_field_value'])
                if z[k]['supp_field_name'] == 'BillingBPN':
                    print('BillingBPN: ' + str(z[k]['supp_field_value']))
                    vBillingBPN = str(z[k]['supp_field_value'])
                if z[k]['supp_field_name'] == 'SAPsubscription':
                    print('SAP Subscription: ' + str(z[k]['supp_field_value']))
                    vSAPsubscription = str(z[k]['supp_field_value'])
                if z[k]['supp_field_name'] == 'Name2':
                    print('Name2: ' + str(z[k]['supp_field_value']))
                    vName2 = str(z[k]['supp_field_value'])
                if z[k]['supp_field_name'] == 'Name3':
                    print('Name3: ' + str(z[k]['supp_field_value']))
                    vName3 = str(z[k]['supp_field_value'])
                if z[k]['supp_field_name'] == 'Guam_UserID':
                    print('vGuam_UserID: ' + str(z[k]['supp_field_value']))
                    vGuam_UserID = str(z[k]['supp_field_value'])
                if z[k]['supp_field_name'] == 'Guam_SubscriptionID':
                    print('vGuam_SubscriptionID: ' + str(z[k]['supp_field_value']))
                    vGuam_SubscriptionID = str(z[k]['supp_field_value'])
                if z[k]['supp_field_name'] == 'Tenant_ID':
                    print('vTenant_ID: ' + str(z[k]['supp_field_value']))
                    vTenant_ID = str(z[k]['supp_field_value'])
                if z[k]['supp_field_name'] == 'APIm_DevID':
                    print('vAPIm_DevID: ' + str(z[k]['supp_field_value']))
                    vAPIm_DevID = str(z[k]['supp_field_value'])
                if z[k]['supp_field_name'] == 'APIm_SubscriptionID':
                    print('vAPIm_SubscriptionID: ' + str(z[k]['supp_field_value']))
                    vAPIm_SubscriptionID = str(z[k]['supp_field_value'])
                if z[k]['supp_field_name'] == 'PCN':
                    print('vPCN: ' + str(z[k]['supp_field_value']))
                    vPCN = str(z[k]['supp_field_value'])
                if z[k]['supp_field_name'] == 'USPS_Serial_Number':
                    print('vUSPS_Serial_Number: ' + str(z[k]['supp_field_value']))
                    vUSPS_Serial_Number = str(z[k]['supp_field_value'])
                if z[k]['supp_field_name'] == 'EnterpriseFunded':
                    print('vEnterpriseFunded: ' + str(z[k]['supp_field_value']))
                    vEnterpriseFunded = str(z[k]['supp_field_value'])
                if z[k]['supp_field_name'] == 'EnterpriseA3':
                    print('vEnterpriseA3: ' + str(z[k]['supp_field_value']))
                    vEnterpriseA3 = str(z[k]['supp_field_value'])
                if z[k]['supp_field_name'] == 'Material_ID':
                    print('vMaterial_ID: ' + str(z[k]['supp_field_value']))
                    vMaterial_ID = str(z[k]['supp_field_value'])
                if z[k]['supp_field_name'] == 'Enterprise':
                    print('vEnterprise: ' + str(z[k]['supp_field_value']))
                    vEnterprise = str(z[k]['supp_field_value'])
                if z[k]['supp_field_name'] == 'vEnterpriseID':
                    print('vEnterpriseID: ' + str(z[k]['supp_field_value']))
                    vEnterpriseID = str(z[k]['supp_field_value'])
                if z[k]['supp_field_name'] == 'PrePay_Fund':
                    print('vPrePay_Fund: ' + str(z[k]['supp_field_value']))
                    vPrePay_Fund = str(z[k]['supp_field_value'])
                if z[k]['supp_field_name'] == 'Migrated_Account':
                    print('vMigrated_Account: ' + str(z[k]['supp_field_value']))
                    vMigrated_Account = str(z[k]['supp_field_value'])
                if z[k]['supp_field_name'] == 'PaymentKey':
                    print('vPaymentKey: ' + str(z[k]['supp_field_value']))
                    vPaymentKey = str(z[k]['supp_field_value'])
                if z[k]['supp_field_name'] == 'SFDC_MCID':
                    print('vSFDC_MCID: ' + str(z[k]['supp_field_value']))
                    vSFDC_MCID = str(z[k]['supp_field_value'])
                if z[k]['supp_field_name'] == 'TaxClassCode':
                    print('vTaxClassCode: ' + str(z[k]['supp_field_value']))
                    vTaxClassCode = str(z[k]['supp_field_value'])
                if z[k]['supp_field_name'] == 'vMailcode':
                    print('vMailcode: ' + str(z[k]['supp_field_value']))
                    vMailcode = str(z[k]['supp_field_value'])


            # print(str(resp_dict[b]['supp_field_name']))
            # When the items below are not of TYPE None| then store the value to the variable overwriting the default above
            if resp_dict[b]['client_acct_id'] != None:
                Okta = resp_dict[b]['client_acct_id']
            if resp_dict[b]['company_name'] != None:
                company = resp_dict[b]['company_name']
            if resp_dict[b]['first_name'] != None:
                firstname = resp_dict[b]['first_name']
            if resp_dict[b]['last_name'] != None:
                lastname = resp_dict[b]['last_name']
            if resp_dict[b]['alt_email'] != None:
                email = resp_dict[b]['alt_email']
            masterplan = resp_dict[b]['plan_no']
            if resp_dict[b]['supp_plan'] != None:
                vsupp_plan = resp_dict[b]['supp_plan']
            if resp_dict[b]['pay_method'] != None:
                vpay_method = resp_dict[b]['pay_method']

            # Finalize the output string
            writestring = writestring + '|' + vSBPN + '|' + vProductFam + '|' + str(vpay_method)+ '|' + Okta + '|' + str(masterplan)
            if g > -1:
                for l in range(g):
                    if vsupp_plan0 != 'None':
                        print(str(vsupp_plan0))
                        writestring = writestring + '|'+ str(vsupp_plan0)
                    if vsupp_plan1 != 'None':
                        writestring = writestring + '|'+ str(vsupp_plan1)
                    if vsupp_plan2 != 'None':
                        writestring = writestring + '|'+ str(vsupp_plan2)
                    if vsupp_plan3 != 'None':
                        writestring = writestring + '|'+ str(vsupp_plan3)
                    if vsupp_plan4 != 'None':
                        writestring = writestring + '|'+ str(vsupp_plan4)
                    if vsupp_plan5 != 'None':
                        writestring = writestring + '|'+ str(vsupp_plan5)
                    if vsupp_plan6 != 'None':
                        writestring = writestring + '|'+ str(vsupp_plan6)
                    if vsupp_plan7 != 'None':
                        writestring = writestring + '|'+ str(vsupp_plan7)
                    if vsupp_plan8 != 'None':
                        writestring = writestring + '|'+ str(vsupp_plan8)
                    if vsupp_plan9 != 'None':
                        writestring = writestring + '|'+ str(vsupp_plan9)
                    if vsupp_plan10 != 'None':
                        writestring = writestring + '|'+ str(vsupp_plan10)

            writestring = writestring + '|' + str(BillAgree) + '|' + company + '|' + firstname + '|' + lastname + '|' +email+'|'+ country + '|' + vmaterialID + '|' + vmaterialDescription + '|' + vGUID + '|' + vPURCHASE_POWER + '|' + vGEOCODE + '|' + vSales + '|' + vRep + '|' + vCompanyCode + '|' + vSalesOrg + '|' + vDistributionChannel + '|' + vDivision + '|' + vBillingBPN + '|' + vSAPsubscription + '|' + vName2 + '|' + vName3 + '|' + vGuam_UserID + '|' + vGuam_SubscriptionID + '|' + vTenant_ID + '|' + vAPIm_DevID + '|' + vAPIm_SubscriptionID + '|' + vPCN + '|' + vUSPS_Serial_Number + '|' + vEnterpriseFunded + '|' + vEnterpriseA3 + '|' + vEnterprise + '|' + vEnterpriseID + '|' + vPrePay_Fund + '|' + vMigrated_Account + '|' + vSFDC_MCID + '|' + vTaxClassCode + '|' + vMailcode + '|' + '\n'
            print(writestring)

            # Only want V1 payment information| so check if the material id is set for a payment key '9x' or a Canadian account 'CA'| and if so exclude.
            #if vSBPN != 'None':
            #if resp_dict[b]['status_cd'] > -2:
            outfile.write(writestring)

            # Increment the indexing variable| and continue the loop
            b = b + 1

#Function to process the data range used in the Get Account Details call to Aria
#Input starting month| days to process| and year to begin

def datelooper(month,daytostart,daystoprocess,startyear):
    callingdate=datetime.date(startyear,month,daytostart)
    callingdate2 = callingdate + datetime.timedelta(days=1)
    if callingdate2.day is 1:
        print('yes')
    else:
        print('no')

    m=0
    #while m<(365*years):
    #while m < (1 * 1):
    while m < daystoprocess:
        a_year=callingdate.timetuple().tm_year
        a_year2=callingdate2.timetuple().tm_year
        a_month=callingdate.timetuple().tm_mon
        a_month2=callingdate2.timetuple().tm_mon
        a_day=callingdate.timetuple().tm_mday
        a_day2=callingdate2.timetuple().tm_mday
        a_date1=str(a_year)+'-'+str(a_month)+'-'+str(a_day)
        a_date2=str(a_year2)+'-'+str(a_month2)+'-'+str(a_day2)
        print(a_date1, a_date2)
        callAria(a_date1,a_date2)
        callingdate=callingdate+datetime.timedelta(days=1)
        callingdate2 = callingdate + datetime.timedelta(days=1)

        m=m+1




#start the lookup process
#parameters are month to start the search| day of the month to start| number of days to process| starting year
lmonth = 6
lstartday = 16
ldaystoprocess = 15
lyear = 2017

datelooper(lmonth,lstartday,ldaystoprocess,lyear)
