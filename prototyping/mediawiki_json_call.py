import json

from mediawikiapi import MediaWikiAPI
from tests.test_customizations import ROME, STOCKHOLM, NYC

"""
https://www.mediawiki.org/wiki/Extension:GeoData
https://en.wikipedia.org/w/api.php?action=query&list=geosearch&gsradius=10000&gscoord=37.786971%7C-122.399677
"""

if __name__ == '__main__':
    mwa = MediaWikiAPI()

    # https://www.mediawiki.org/wiki/Extension:GeoData
    # returns a list and cannot be expanded with prop
    search_params = {
        "action": "query",
        "list": "geosearch",
        "gsradius": 10000,
        "gscoord": "{0}|{1}".format(ROME[0], ROME[1]),
        # "prop": "description|categories",
    }

    search_params = {
        "action": "query",
        "generator": "geosearch",
        "ggsradius": 10000,
        "ggscoord": "{0}|{1}".format(NYC[0], NYC[1]),
        "ggssort": "relevance",
        "prop": "pageviews",
        "ggslimit": 50,
    }


    raw_results = mwa.session.request(search_params, mwa.config)
    print(json.dumps(raw_results, indent=4))
