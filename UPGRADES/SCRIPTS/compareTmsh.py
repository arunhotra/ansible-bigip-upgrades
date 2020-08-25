#!/usr/bin/env python3

import os
import json
import sys
from collections import OrderedDict


os.chdir("..")
os.chdir("./TMP")

compare_status = {}

with open('active_standby_ha_pairs.json', 'r') as bigips_file:
    bigips = json.load(
        bigips_file, object_pairs_hook=OrderedDict)


for ha_pair in bigips.keys():
    status_file_1 = ha_pair + '_status.json'
    status_file_2 = bigips[ha_pair] + '_status.json'

    with open(status_file_1, 'r') as active_file:
        status_file_1_json = json.load(
            active_file, object_pairs_hook=OrderedDict)

    with open(status_file_2, 'r') as standby_file:
        status_file_2_json = json.load(
            standby_file, object_pairs_hook=OrderedDict)

    status = (status_file_1_json == status_file_2_json)
    compare_status[ha_pair + '-' + bigips[ha_pair]] = status

with open('compare_status.json', 'w') as outfile:
    json.dump(compare_status, outfile)
