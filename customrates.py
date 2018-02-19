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
ariaAPI = '&rest_call=get_acct_plans_all&acct_no='
ariaAPI2 = '&rest_call=modify_supp_plan&acct_no='

#filepath = 'Desktop/Python2/'

#Since this is a large extract| loop through calls using the account creation date
#Nested loops by year and month
isProduction = False

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

else:
    # Point to Staging
    clientID = '4934683'
    auth = 'DtcWUTxMYSySytSMtAerN3H67be5mH5n'
    ariaCoreUrl = 'https://secure.future.stage.ariasystems.net/api/ws/api_ws_class_dispatcher.php' #core URL
    #ariaObjectURL = 'XXXhttps://secure.future.stage.ariasystems.net/api/AriaQuery/objects.php'
    #ariaAdminURL = 'xxxhttps://admintools.future.stage.cph.ariasystems.net/AdminTools.php/Dispatcher'
    ariaoutfile = 'ariaCustRatesAccount--staging.txt' #setting the file variable to store the output of the API call
    changefile = 'newrates.txt'
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
def callAria (acctID):
#This function calls the get_acct_plans Aria API to retrieve all the plan and rate data on the account
#It parses the output and builds a text file with the data necessary to build a load file for the modify plan rates call
    with open(ariaoutfile, 'w') as outfile:

        writestring = 'Acct|clientPID|CustRatePlan|RateSchedNum|RateSrvNo|Recurring|Usage|SeqNo|fromU|toU|rtPerU' + '\n'
        outfile.write(writestring)

        # set the URL with the account number for the lookup
        ariaGetAcctUrl = ariaCoreUrl + '?client_no=' + clientID + '&auth_key=' + auth + ariaAPI +str(acctID)+'&output_format=json'

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

        # Defaultsomevariablesfortheoutput
        #vacctPlanArrayLnth = j
       # vPlanNum = 'None'
       # vPlanName = 'None'
       # vlastBillDate = 'None'
       # vnextBillDate = 'None'
       # vbillThruDate = 'None'
       # vPlanSrvCount = 'None'
        #vclientSrvID = 'None'
       # vusageType = 'None'
        #vusageTypeName = 'None'
       # vrateSchedName = 'None'
        #visDefaultSched = 'None'
       # vplanSrvRatesCount = 'None'


        vAccount = acctID
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

        # loop through the response records
        for i in resp_dict:


            # outfile.write(str(resp_dict[b]['acct_no'])+'|'+str(resp_dict[b]['senior_acct_no'])+'|'+str(resp_dict[b]['pay_method'])+'\n')
            #print(str(acctID) + '|' + str(resp_dict[b]['plan_no']) + '|' + str(resp_dict[b]['plan_name']) + '\n')

            # Set dictionaries for the supplemental field list and the current billing info blocks



            #print(str(c)+'/n')
            #print(str(d)+'/n')


           # vPlanNum = resp_dict[b]['plan_no']
           # vPlanName = resp_dict[b]['plan_name']

           # vlastBillDate = resp_dict[b]['last_bill_date']
            #vnextBillDate = resp_dict[b]['next_bill_date']
            #vbillThruDate = resp_dict[b]['bill_thru_date']
           # visDefaultSched = resp_dict[b]['rate_sched_is_default_ind']

            vrateSchedNum = resp_dict[b]['rate_schedule_no']
            vclientPlanID = resp_dict[b]['client_plan_id']
            vsuppPlanIndicator = resp_dict[b]['supp_plan_ind']
            vsuppPlanStatus = resp_dict[b]['supp_plan_status_cd']
            vclientRateSchedID = resp_dict[b]['client_rate_schedule_id']

           # vrateSchedName = resp_dict[b]['rate_schedule_name']
           # visDefaultSched = resp_dict[b]['rate_sched_is_default_ind']

            #print(vclientPlanID)
            if b == 0:
                masterrateschedule = resp_dict[b]['rate_schedule_no']


            if vsuppPlanStatus == 1:
                z = resp_dict[b]['plan_services']
                c = len(z)
                print(resp_dict[b])

                for k in range (c):
                    vIsRecurring = z[k]['is_recurring_ind']
                    vIsUsage = z[k]['is_usage_based_ind']
                    vSrvNo = z[k]['service_no']
                    #if vIsUsage > 0:
                     #   vusageType = z[k]['usage_type']
                     #   vusageTypeName = z[k]['usage_type_name']
                    #vclientSrvID = z[k]['client_service_id']
                    y = z[k]['plan_service_rates']
                    d = len(y)
                    vplanSrvRatesCount = d
                    vIsRecurring = z[k]['is_recurring_ind']
                    vIsUsage = z[k]['is_usage_based_ind']
                    #if vIsUsage > 0:
                       # vusageType = z[k]['usage_type']
                       # vusageTypeName = z[k]['usage_type_name']
                    #vclientSrvID = z[k]['client_service_id']

                    for m in range (d):
                        vtoUnit = 'None'
                        vrateSeqNo = y[m]['rate_seq_no']
                        vfromUnit = y[m]['from_unit']
                        if y[m]['to_unit'] != None:
                            vtoUnit = y[m]['to_unit']
                        vratePerUnit = y[m]['rate_per_unit']


                        #vclientRateSchedID = y[m]['client_rate_schedule_id']

                        #build the string and write to file
                        if vsuppPlanIndicator == 1 and vsuppPlanStatus == 1:
                            #print(str(resp_dict[b]['plan_no']))
                            #print(str(resp_dict[b]['plan_date']))
                            #print(str(resp_dict[b]['bill_day']))

                            writestring = str(vAccount) + '|'  + str(vclientPlanID) + '|'+str(masterrateschedule)+'|' + str(vrateSchedNum) +'|' + str(vSrvNo) + '|' + str(vIsRecurring) + '|' + str(vIsUsage) + '|'  + str(vrateSeqNo) + '|' + str(vfromUnit) + '|' + str(vtoUnit) + '|' + str(vratePerUnit) + '\n'

                            #print(writestring)
                            outfile.write(writestring)

                #print(str(b))




            # Increment the indexing variable| and continue the loop
            b = b + 1


def modRates():
#This function uses a delimited text file to read in the lines and build data dictionaries for each array type needed when making the
#modify_supp_plan API call to Aria to change custom rates.

        newrates1 = open(changefile, 'r')
       #fout.write(writeout)
        chkclientPID = 'None'
        bloop = -1

        custom_rate_plan_no = []
        custom_rate_service_no = []
        custom_rate_seq_no = []
        custom_rate_from_unit = []
        custom_rate_to_unit = []
        custom_rate_per_unit = []
        custom_rate_sched_id = []

        ariaChangePlanRates = ariaCoreUrl + '?client_no=' + clientID + '&auth_key=' + auth + ariaAPI2

        for line in reader(newrates1, delimiter ='|'):
            #print(line)
            Acct,clientPID,clientrateshedid,RateSchedNum,RateSrvNo,Recurring,Usage,SeqNo,fromU,toU,rtPerU=line
            if bloop > -1:
                ariaChangePlanRatesUrl=ariaChangePlanRates+str(Acct)+'&assignment_directive=2&client_plan_id='+str(clientPID)+'&alt_rate_schedule_no='+str(RateSchedNum)+'&num_plan_units=1&do_write=true'

                #custom_rate_sched_id.append(clientrateshedid)
                custom_rate_plan_no.append(clientrateshedid)
                custom_rate_service_no.append(RateSrvNo)
                custom_rate_seq_no.append(SeqNo)
                custom_rate_from_unit.append(fromU)
                custom_rate_to_unit.append(toU)
                custom_rate_per_unit.append(rtPerU)

            bloop = bloop + 1

        print('length of list custom rate plan no is '+str(len(custom_rate_plan_no)))
        rateslist = ''

        getlist=0
        #rateslist =rateslist+'&custom_rate_plan_no'
        for g in custom_rate_plan_no:
            rateslist=rateslist+'&custom_rate_plan_no['+str(getlist)+']='+str(custom_rate_plan_no[getlist])
            getlist=getlist+1
        getlist=0
        #rateslist=rateslist+'&custom_rate_service_no'
        for h in custom_rate_service_no:
            rateslist=rateslist+'&custom_rate_service_no['+str(getlist)+']='+str(custom_rate_service_no[getlist])
            getlist=getlist+1
        getlist = 0
        #rateslist=rateslist+'&custom_rate_seq_no'
        for h in custom_rate_seq_no:
            rateslist = rateslist + '&custom_rate_seq_no[' + str(getlist) + ']='+str(custom_rate_seq_no[getlist])
            getlist = getlist + 1
        getlist = 0
        #rateslist=rateslist+'&custom_rate_from_unit'
        for h in custom_rate_from_unit:
            rateslist = rateslist + '&custom_rate_from_unit[' + str(getlist) + ']=' + str(custom_rate_from_unit[getlist])
            getlist = getlist + 1
        getlist = 0

        for h in custom_rate_to_unit:
            print(str(custom_rate_to_unit[getlist]))
            if custom_rate_to_unit[getlist] != 'None':
                rateslist = rateslist + '&custom_rate_to_unit[' + str(getlist) + ']=' + str(custom_rate_to_unit[getlist])
            getlist = getlist + 1
        getlist = 0
        #rateslist=rateslist+'&custom_rate_per_unit'
        for h in custom_rate_per_unit:
            rateslist = rateslist + '&custom_rate_per_unit[' + str(getlist) + ']=' + str(custom_rate_per_unit[getlist])
            getlist = getlist + 1

        changeURL = ariaChangePlanRatesUrl+rateslist
       # print(ariaChangePlanRatesUrl+'\n')
        #print(rateslist+'\n')
        print(changeURL)
        response3 = requests.post(changeURL)

        print(response3)
# to capture the sent rates
        #with open(ariaoutfileratesup, 'w') as outfile2:
             #outfile2.write('Acct|clientPID|RateSchedNum|RateSrvNo|Recurring|Usage|SeqNo|fromU|toU|rtPerU|' + '\n')  #start the lookup process
#parameters are the account to retrieve  ** if you need date manipulation look at "looptest.py" for examples

lacct = "23024106"


#callAria(lacct)

modRates()
