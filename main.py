#!/usr/bin/env python
import json
import yaml
import client as client
import time

DELAY=5

def get_skip_list():
    with open('./secrets/skiplist.yml') as data:
        yml = yaml.safe_load(data)
        return yml

with open('./data/config.yml', 'r') as data:
    yml = yaml.safe_load(data)
    skip_list = get_skip_list()
    for name, group in yml.items():

        if name in skip_list:
            print ('Skipping group: [{}]'.format(name))
            continue

        print('Creating group: [{}]'.format(name))
        pendo_group = client.create_group_idempotent(name, client.get_color(name, group))

        if 'pages' in group:
            for page_name, page in group['pages'].items():
                print('- Creating page: [{}] {}'.format(page_name, page))
                client.create_page_in_group(pendo_group, page_name, page)
                time.sleep(DELAY)

        if 'features' in group:
            for feature_name, feature in group['features'].items():
                print('- Creating feature: [{}] {}'.format(feature_name, feature))
                client.create_feature_in_group(pendo_group, feature_name, feature)
                time.sleep(DELAY)
