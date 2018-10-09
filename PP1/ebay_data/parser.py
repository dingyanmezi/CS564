
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
MONTHS = {'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04', 'May': '05', 'Jun': '06',
          'Jul': '07', 'Aug': '08', 'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12'}

Itemdat = open('items.dat', 'w')
Userdat = open('users.dat', 'w')
Bidsdat = open('bids.dat', 'w')
ItemCategorydat = open('category.dat', 'w')

"""
Returns true if a file ends in .json
"""


def isJson(f):
    return len(f) > 5 and f[-5:] == '.json'

def addQuote(xian):
    shu = 0
    finalxian = ''
    zifumen = []
    indexmen = []
    for babe in xian:
        zifumen.insert(shu, babe)
        if babe == '"':
            indexmen.append(shu)
        shu = shu + 1
    shu2 = len(indexmen)-1
    while shu2 >= 0:
        zifumen.insert(indexmen[shu2], '"')
        shu2 = shu2 - 1
    for babe2 in zifumen:
        finalxian = finalxian + babe2
    return finalxian
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
    if dttm == 'NULL':
        return dttm
    else:
        dttm = dttm.strip().split(' ')
        dt = dttm[0].split('-')
        date = '20' + dt[2] + '-'
        date += transformMonth(dt[0]) + '-' + dt[1]
        return date + ' ' + dttm[1]


"""
Transform a dollar value amount from a string like $3,453.23 to XXXXX.xx
"""


def transformDollar(money):
    if money == None or len(money) == 0 or money == 'NULL' or money == '0':
        return money
    return sub(r'[^\d.]', '', money)


"""
Parses a single json file. Currently, there's a loop that iterates over each
item in the data set. Your job is to extend this functionality to create all
of the necessary SQL tables for your database.
"""


def parseJson(json_file):
    # CREATE THE DESTINATION FILES
    quote = '"'
    
    with open(json_file, 'r') as f:
        items = loads(f.read())['Items']  # creates a Python dictionary of Items for the supplied json file

        for item in items:
            """
            TODO: traverse the items dictionary to extract information from the
            given `json_file' and generate the necessary .dat files to generate
            the SQL tables based on your relation design
            """
            # SET UP THE KEYS FOR FUTURE USE
            #print item
            #break
            keys = ['ItemID', 'Name', 'Currently', 'Buy_Price', 'First_Bid', 'Number_of_Bids',
                    'Description', 'Started', 'Ends', 'Rating', 'Country', 'Location',
                    'Category', 'Bids', 'Seller']

            # TURN THE VALUE OF 'NONE' INTO 'NULL'
            for key in keys:
                if item.get(key) is None:
                    item[key] = 'NULL'

            # FOUR BLCOKS BELOW FORMATTING THE STRING THAT WILL BE WIRTTE INTO RESPECTIVE .DAT FILE

            # THIS IS FOR TABLE ITEM
            yihang_item = '' + item.get('ItemID', 'NULL') + columnSeparator + quote + addQuote(item.get('Name', 'NULL')) + quote + columnSeparator + quote +\
                transformDollar(item.get('Currently', 'NULL')) + quote + columnSeparator + quote +\
                transformDollar(item.get('Buy_Price', '0')) + quote + columnSeparator + quote +\
                transformDollar(item.get('First_Bid', 'NULL')) + quote +\
                columnSeparator + item.get('Number_of_Bids', 'NULL') + columnSeparator + quote +\
                addQuote(item.get('Description', 'NULL')) + quote + columnSeparator + quote +\
                transformDttm(item.get('Started', 'NULL')) + quote + columnSeparator + quote +\
                transformDttm(item.get('Ends', 'NULL')) + quote + columnSeparator
            maijiainfo = item.get('Seller')
            yihang_item += quote + maijiainfo.get('UserID', 'NULL') + quote

            # THIS IS FOR TABLE USER
            
            SellerID_field = maijiainfo.get('UserID', 'NULL')
            location_field_text = '' + item.get('Location', 'NULL')
            country_field_text = '' + item.get('Country', 'NULL')
            rating_field = maijiainfo.get('Rating', 'NULL')
            yihang_user = '' + quote + addQuote(SellerID_field) + quote + columnSeparator + quote + addQuote(location_field_text) + quote + columnSeparator + quote +\
            			addQuote(country_field_text) + quote + columnSeparator + rating_field
                

            # THIS IS FOR TABLE BID
            yihang_bid = '' + item.get('ItemID', 'NULL') + columnSeparator
            bids_field = item.get('Bids', 'NULL')    
            BidderID_field = ''
            time_field = ''
            amount_field = ''
            if bids_field == 'NULL':
                BidderID_field = 'NULL'
                time_field = 'NULL'
                amount_field = 'NULL'
                yihang_bid += BidderID_field + columnSeparator + time_field + columnSeparator + amount_field
                Bidsdat.write(yihang_bid + '\n')
            else:
                for babe2 in bids_field:
                    BidderID_field_2 = babe2.get('Bid', 'NULL').get('Bidder', 'NULL').get('UserID', 'NULL')
                    time_field_2 = transformDttm(babe2.get('Bid', 'NULL').get('Time', 'NULL'))
                    amount_field_2 = transformDollar(babe2.get('Bid', 'NULL').get('Amount', 'NULL'))

                    rating_field_2 = babe2.get('Bid', 'NULL').get('Bidder', 'NULL').get('Rating', 'NULL')
                    location_field_2 = babe2.get('Bid', 'NULL').get('Bidder', 'NULL').get('Location', 'NULL')
                    country_field_2 = babe2.get('Bid', 'NULL').get('Bidder', 'NULL').get('Country', 'NULL')

                    yihang_bid_2 = '' + item.get('ItemID', 'NULL') + columnSeparator + quote + BidderID_field_2 +\
                                        quote + columnSeparator + quote + time_field_2 + quote + columnSeparator +\
                                        quote + amount_field_2 + quote
                    Bidsdat.write(yihang_bid_2 + '\n')
                    # This is for the bidder as a user to be added into the Users table. 
                    # I write it here cuz I am gonna use var declared in this BID section and I dont want to change the decalred var. 
                    yihang_user_2 = '' + quote + addQuote(BidderID_field_2) + quote + columnSeparator + quote + addQuote(location_field_2) + quote + columnSeparator + quote +\
                        addQuote(country_field_2) + quote + columnSeparator + rating_field_2
                    Userdat.write(yihang_user_2 + '\n')

            # THIS IS FOR TABLE CATEGORY
            
            zhongleimen = item.get('Category', 'NULL')
            for yigezhonglei in zhongleimen:
                yihang_category = '' + item.get('ItemID', 'NULL') + columnSeparator + quote + yigezhonglei + quote
                ItemCategorydat.write(yihang_category + '\n')
            # WRITE TO THE FILE
            Itemdat.write(yihang_item + '\n')
            Userdat.write(yihang_user + '\n')
            
            

    # CLOSE FILES

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
            print "Success parsing " + f


if __name__ == '__main__':
    main(sys.argv)

Itemdat.close()
Userdat.close()
Bidsdat.close()
ItemCategorydat.close()