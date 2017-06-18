#!/usr/bin/env python

# # Pulling raw data from OpenCorporates
# 
# This notebook's purpose is only to pull raw data from OpenCorporates and store it in JSON format. Please don't commit the resulting file to GitHub! This is just for convenience, so that we don't have to re-download every time, but I think it would be better if only the data that we decide to include in the final dataset is made public.
# 
# The API key is to be stored in an environmental variable, OC_APIKEY. It will be used here for the query.

# Command line tool version of the notebook

import os
import sys
import json
import requests
import numpy as np
import pandas as pd


# First step is loading the .csv and gathering all unique company names
tw_orgorg = pd.read_csv('https://query.data.world/s/94g9v4tj3pzz3ir495y8s3esl')
tw_perorg = pd.read_csv('https://query.data.world/s/50ivsaqkos6vzdf4m51ntq7qc')

# Now gather all the company names
org1 = tw_orgorg['Organization A'].unique()
org2 = tw_orgorg['Organization B'].unique()
org3 = tw_perorg['Organization'].unique()


all_org = sorted(list(set(org1).union(set(org2).union(set(org3)))))

query_header = 'https://api.opencorporates.com/v0.4/companies/search'
org_oc_data = {}
failed_i = []

print "Pulling organization data from OpenCorporates..."
for i, org in enumerate(all_org):
    sys.stdout.write("\r{0:4d}/{1}".format(i+1, len(all_org)))
    ou_q = '+'.join([w.lower() for w in org.split()])
    # Prepare an URL request
    try:
        r = requests.get(query_header, params={'q': ou_q, 'api_token': os.environ['OC_APIKEY']})
        resp = json.loads(r.text)
    except Exception as e:
        # Something went wrong?
        print "\nERROR: {0}\n".format(e)
        failed_i.append(i)
        continue
    # If we did it...
    org_oc_data[org] = resp['results']['companies']


# And finally save it all
json.dump(org_oc_data, open('org_OCdata.json', 'w'))

# Also dump a log of failed ones:
errlog = open('failed.log', 'w')
errlog.write('\n'.join([all_org[i] for i in failed_i]))
errlog.close()
