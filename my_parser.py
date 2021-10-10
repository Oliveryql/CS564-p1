
"""
FILE: skeleton_parser.py
------------------
Author: Firas Abuzaid (fabuzaid@stanford.edu)
Author: Perth Charernwattanagul (puch@stanford.edu)
Modified: 04/21/2014

Skeleton parser for CS564 programming project 1. Has useful imports and
functions for parsing, including:

1) Directory handling -- the parser takes a list of eBay json files
and opens each file inside of a loop. You just need to fill in the rest.
2) Dollar value conversions -- the json files store dollar value amounts in
a string like $3,453.23 -- we provide a function to convert it to a string
like XXXXX.xx.
3) Date/time conversions -- the json files store dates/ times in the form
Mon-DD-YY HH:MM:SS -- we wrote a function (transformDttm) that converts to the
for YYYY-MM-DD HH:MM:SS, which will sort chronologically in SQL.

Your job is to implement the parseJson function, which is invoked on each file by
the main function. We create the initial Python dictionary object of items for
you; the rest is up to you!
Happy parsing!
"""

import sys
from json import loads
from re import sub

columnSeparator = "|"

# Dictionary of months used for date transformation
MONTHS = {'Jan':'01','Feb':'02','Mar':'03','Apr':'04','May':'05','Jun':'06',\
        'Jul':'07','Aug':'08','Sep':'09','Oct':'10','Nov':'11','Dec':'12'}

"""
Returns true if a file ends in .json
"""
def isJson(f):
    return len(f) > 5 and f[-5:] == '.json'

"""
Converts month to a number, e.g. 'Dec' to '12'
"""
def transformMonth(mon):
    if mon in MONTHS:
        return MONTHS[mon]
    else:
        return mon

"""
Transforms a timestamp from Mon-DD-YY HH:MM:SS to YYYY-MM-DD HH:MM:SS
"""
def transformDttm(dttm):
    dttm = dttm.strip().split(' ')
    dt = dttm[0].split('-')
    date = '20' + dt[2] + '-'
    date += transformMonth(dt[0]) + '-' + dt[1]
    return date + ' ' + dttm[1]

"""
Transform a dollar value amount from a string like $3,453.23 to XXXXX.xx
"""

def transformDollar(money):
    if money == None or len(money) == 0:
        return money
    return sub(r'[^\d.]', '', money)

def transformStr(st):
    # return NULL string for SQL as per spec
    if st is None:
        return "NULL"
    
    escaped_str = st.replace('"','""')
    return '"{}"'.format(escaped_str)

"""
Parses a single json file. Currently, there's a loop that iterates over each
item in the data set. Your job is to extend this functionality to create all
of the necessary SQL tables for your database.
"""
def parseJson(json_file):
    with open(json_file, 'r') as f:
        items = loads(f.read())['Items'] # creates a Python dictionary of Items for the supplied json file
        for item in items:
            """
            TODO: traverse the items dictionary to extract information from the
            given `json_file' and generate the necessary .dat files to generate
            the SQL tables based on your relation design
            """
            # ATTENTION: NEED TO FIX DUPLICATE ENTRIES

            with open("item.dat",'a') as f1:
                # item table
                f1.write(item['ItemID'] + '|')
                if item['Name'] is None:
                    f1.write("NULL"+ '|')
                else:
                    f1.write(transformStr(item['Name']) + '|')
                if item['Currently'] is None:
                    f1.write("NULL"+ '|')
                else:
                    f1.write(transformDollar(item['Currently']) + '|')
                if 'Buy_Price' in item: # this attribute could be missing
                    f1.write(transformDollar(item['Buy_Price']) + '|')
                else:
                    f1.write("NULL" + '|')
                if item['First_Bid'] is None:
                    f1.write("NULL"+ '|')   
                else:           
                    f1.write(transformDollar(item['First_Bid']) + '|')
                if item['Number_of_Bids'] is None:
                    f1.write("NULL"+ '|')
                else:
                    f1.write(item['Number_of_Bids'] + '|')
                if item['Started'] is None:
                    f1.write("NULL"+ '|')
                else:
                    f1.write(transformDttm(item['Started']) + '|')
                if item['Ends'] is None:
                    f1.write("NULL"+ '|')
                else:                
                    f1.write(transformDttm(item['Ends']) + '|')
                if item['Seller'] is None:
                    f1.write("NULL"+ '|')
                else:
                    f1.write(item['Seller']['UserID']+'|')
                if item['Description'] is None:
                    f1.write("NULL"+ '\n')
                else:
                    f1.write(transformStr(item['Description']) + '\n')
                f1.close()
                # category table
            with open("category.dat",'a') as f2:
                for cat in item['Category']:
                    f2.write(item['ItemID'] + '|')
                    f2.write(cat + '\n')
                f2.close()
                # auction table
            with open("auction.dat",'a') as f3:
                if item['Bids'] is not None:
                    for bid in item['Bids']:
                        f3.write(item['ItemID'] + '|')
                        f3.write(bid['Bid']['Bidder']['UserID'] + '|')
                        f3.write(transformDttm(bid['Bid']['Time']) + '|')
                        f3.write(transformDollar(bid['Bid']['Amount']) + '\n')
                f3.close()
                # user table
            with open("user.dat",'a') as f4:
                # extract seller info first
                f4.write(item['Seller']['UserID']+'|')
                f4.write(transformStr(item['Location'])+'|')
                f4.write(transformStr(item['Country'])+'|')
                f4.write(item['Seller']['Rating']+'\n')
                # extract bidder info next
                if item['Bids'] is not None:
                    for bid in item['Bids']:
                        f4.write(bid['Bid']['Bidder']['UserID'] + '|')
                        if 'Location' in bid['Bid']['Bidder']:
                            f4.write(transformStr(bid['Bid']['Bidder']['Location']) + '|')
                        else: 
                            f4.write("NULL" + '|')
                        if 'Country' in bid['Bid']['Bidder']:
                            f4.write(transformStr(bid['Bid']['Bidder']['Country']) + '|')
                        else:
                            f4.write("NULL" + '|')
                        f4.write(bid['Bid']['Bidder']['Rating'] + '\n')
                f4.close()
            pass

"""
Loops through each json files provided on the command line and passes each file
to the parser
"""
def main(argv):
    if len(argv) < 2:
        print >> sys.stderr, 'Usage: python skeleton_json_parser.py <path to json files>'
        sys.exit(1)
    # loops over all .json files in the argument
    for f in argv[1:]:
        if isJson(f):
            parseJson(f)
            print ("Success parsing " + f)

if __name__ == '__main__':
    main(sys.argv)
