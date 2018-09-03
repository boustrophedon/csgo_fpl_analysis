import requests

API_KEY = open(".faceit_key", "r").read().strip()

NA_FPL = "748cf78c-be73-4eb9-b131-21552f2f8b75"
EU_FPL = "74caad23-077b-4ef3-8b1d-c6a2254dfa75"

# `hub` is a string containing the hub id.
# Outputs a list of json objects containing information on the most recent
# matches played in that hub. Defaults to 200 matches.
def get_matches(hub, num_matches=200):
    matches_api_url = "https://open.faceit.com/data/v4/hubs/{hub}/matches" \
        .format(hub=hub)

    params = {"type":"past", "offset":"0", "limit":num_matches}

    auth_header = "Bearer {}".format(API_KEY)
    accept_header = "application/json"

    headers = {"Authorization": auth_header, "Accept": accept_header}

    resp = requests.get(matches_api_url, params=params, headers=headers)

    print("Response getting matches: {}".format(resp.status_code))

    return resp.json()['items']

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
    na_fpl_urls = get_demo_urls(filter_incomplete_matches(get_matches(NA_FPL)))

    with open("na_fpl_demos.txt", "a") as f:
        f.write('\n'.join(na_fpl_urls))

    eu_fpl_urls = get_demo_urls(filter_incomplete_matches(get_matches(eu_FPL)))

    with open("eu_fpl_demos.txt", "a") as f:
        f.write('\n'.join(eu_fpl_urls))
