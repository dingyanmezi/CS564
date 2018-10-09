#!/bin/bash
python parser.py ebay_data/items-*.json

sort  users.dat | uniq > users_uniq.dat
sort  bids.dat | uniq > bids_uniq.dat
sort  category.dat | uniq > category_uniq.dat