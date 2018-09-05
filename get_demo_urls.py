import requests
import time

import os

API_KEY = open(".faceit_key", "r").read().strip()

NA_FPL = "748cf78c-be73-4eb9-b131-21552f2f8b75"
EU_FPL = "74caad23-077b-4ef3-8b1d-c6a2254dfa75"

# `hub` is a string containing the hub id. `first_match` is the offset into the
# matches provided by Faceit. `num_matches` is the number of matches to query.
# Outputs a list of json objects containing information on the most recent
# matches played in that hub. Defaults to first 20 matches.
def get_matches(hub, first_match=0, num_matches=20):
    REQUEST_STEP = 20

    matches_api_url = "https://open.faceit.com/data/v4/hubs/{hub}/matches" \
        .format(hub=hub)


    auth_header = "Bearer {}".format(API_KEY)
    accept_header = "application/json"

    headers = {"Authorization": auth_header, "Accept": accept_header}

    matches = list()
    for start in range(first_match, num_matches, REQUEST_STEP):
        params = {"type":"past", "offset":start, "limit":REQUEST_STEP}
        resp = requests.get(matches_api_url, params=params, headers=headers)

        print("Response getting matches: {}".format(resp.status_code))
        matches+= resp.json()['items']
        time.sleep(1)

    return matches

# Given a list of match json objects, filter out incomplete ones.
def filter_incomplete_matches(matches):
    output = list()
    for match in matches:
        if match['status'] == 'FINISHED':
            output.append(match)

    return output

# Given a list of match json objects, return the demo urls
def get_demo_urls(matches):
    demo_urls = list()
    for match in matches:
        demo_urls.append(match['demo_url'][0])

    return demo_urls

if __name__ == '__main__':
    # make data/ and data/demos/ dirs if they don't exist
    os.makedirs("data/demos/", exist_ok=True)

    # because we filter out matches that did not get played, this is actually
    # an upper bound on the number of demos
    NUM_DEMOS = 250

    na_matches = get_matches(NA_FPL, num_matches=NUM_DEMOS)
    na_fpl_urls = get_demo_urls(filter_incomplete_matches(na_matches))

    with open("data/na_fpl_demo_urls.txt", "a") as f:
        f.write('\n'.join(na_fpl_urls))

    eu_matches = get_matches(EU_FPL, num_matches=NUM_DEMOS)
    eu_fpl_urls = get_demo_urls(filter_incomplete_matches(eu_matches))

    with open("data/eu_fpl_demo_urls.txt", "a") as f:
        f.write('\n'.join(eu_fpl_urls))
