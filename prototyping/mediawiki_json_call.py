import json
import time

from mediawikiapi import MediaWikiAPI
from tests.test_customizations import ROME, STOCKHOLM, NYC

"""
Run experimental calls to mediawiki API so as to inspect the contents returned and the latency of the call
https://www.mediawiki.org/wiki/Extension:GeoData
https://www.mediawiki.org/wiki/API:Query
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

    # https://en.wikipedia.org/w/api.php?action=query&generator=geosearch&prop=coordinates%7Cpageimages&ggscoord=37.7891838%7C-122.4033522
    search_params = {
        "action": "query",
        "generator": "geosearch",
        "ggsradius": 10000,
        "ggscoord": "{0}|{1}".format(NYC[0], NYC[1]),
        "ggssort": "relevance",
        "prop": "pageviews",
        "ggslimit": 50,
    }

    # https://en.wikipedia.org/w/api.php?action=query&generator=geosearch&prop=linkshere&ggscoord=37.7891838%7C-122.4033522&lhprop=pageid
    # takes too long list of incoming links is huge and has a very high number of continues
    search_params = {
        "action": "query",
        "generator": "geosearch",
        "ggsradius": 10000,
        "ggscoord": "{0}|{1}".format(NYC[0], NYC[1]),
        "ggssort": "relevance",
        "prop": "linkshere",  # info, length
        "ggslimit": 10,
        "lhprop": "pageid",  # linkshere
        "lhlimit": 100,  # linkshere max number
    }

    # filter categories using clcategories
    # https://en.wikipedia.org/w/api.php?format=xml&action=query&cllimit=500&prop=categories&titles=Empire_State_Building
    # https://en.wikipedia.org/w/api.php?format=xml&action=query&cllimit=500&prop=categories&titles=New_York_University&cldir=ascending
    # https://en.wikipedia.org/w/api.php?format=xml&action=query&cllimit=500&prop=categories&titles=New_York_University&clcategories=Category:Greenwich%20Village

    search_params = {
        "action": "query",
        "generator": "geosearch",
        "ggsradius": 10000,
        "ggscoord": "{0}|{1}".format(NYC[0], NYC[1]),
        "ggssort": "relevance",
        "prop": "info|categories",  # info, length
        "ggslimit": 50,
        "clcategories": "Category:Culture|Category:Greenwich Village",
        # https://www.mediawiki.org/w/api.php?action=help&modules=query%2Bcategories
    }

    # https://en.wikipedia.org/w/api.php?format=xml&action=query&cllimit=500&prop=langlinks&titles=Empire_State_Building&lllimit=10
    # Elapsed time: 83.440358877182 seconds
    search_params = {
        "action": "query",
        "generator": "geosearch",
        "ggsradius": 10000,
        "ggscoord": "{0}|{1}".format(NYC[0], NYC[1]),
        "ggssort": "relevance",
        "prop": "info|description|extracts|langlinks",  # info, length
        "ggslimit": 50,
        "explaintext": True,  # extracts https://www.mediawiki.org/w/api.php?action=help&modules=query%2Bextracts
        "exintro": True,  # extracts
        "exchars": 256,  # extracts
        "lllimit": 10,  # langlinks https://www.mediawiki.org/w/api.php?action=help&modules=query%2Blanglinks
    }

    # Elapsed time: 1.3639109134674072 seconds
    search_params = {
        "action": "query",
        "generator": "geosearch",
        "ggsradius": 10000,
        "ggscoord": "{0}|{1}".format(NYC[0], NYC[1]),
        "ggssort": "relevance",
        "prop": "info|description|extracts",  # info, length
        "ggslimit": 200,
        "explaintext": True,  # extracts https://www.mediawiki.org/w/api.php?action=help&modules=query%2Bextracts
        "exintro": True,  # extracts (greatly speeds up)
        "exchars": 1200,  # extracts
    }

    search_params = {
        "action": "query",
        "prop": "coordinates|pageimages|description|info|pageviews|extracts",
        "inprop": "url",
        "pithumbsize": 144,
        "generator": "geosearch",
        "ggsradius": 10000,
        "ggslimit": 200,
        "colimit": 200,
        "ggscoord": "{0}|{1}".format(NYC[0], NYC[1]),
        "explaintext": True,  # extracts https://www.mediawiki.org/w/api.php?action=help&modules=query%2Bextracts
        "exintro": True,  # extracts (greatly speeds up)
        "exchars": 1200,  # extracts
    }

    start_time = time.time()
    raw_results = mwa.session.request(search_params, mwa.config)
    print(json.dumps(raw_results, indent=4))
    print(f"Elapsed time: {time.time() - start_time} seconds")
