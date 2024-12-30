import json
import unittest
from unittest.mock import patch

from mediawikiapi import MediaWikiAPI, GeosearchResult


class TestGeosearchResult(unittest.TestCase):
    """Test the functionality of GeosearchResult"""

    api = MediaWikiAPI()

    def test_page_to_geosearchresult(self):
        wikipedia_page = self.api.page("Mosque–Cathedral_of_Córdoba")
        geo_search_result = GeosearchResult.from_wikipedia_page(wikipedia_page.__dict__)
        self.assertEqual(geo_search_result.title, wikipedia_page.title)
        self.assertEqual(geo_search_result.description, wikipedia_page.pageprops['wikibase-shortdesc'])
        self.assertTrue(geo_search_result.thumbnail)
        self.assertTrue(geo_search_result.article_url)
        self.assertEqual(geo_search_result.latitude, wikipedia_page.latitude)
        self.assertEqual(geo_search_result.longitude, wikipedia_page.longitude)

    def test_get_article_url(self):
        # Test with a valid relative URL
        relative_url = "read_place/Example"
        full_url = "https://en.wikipedia.org/wiki/Example"
        assert GeosearchResult.get_article_url(full_url) == relative_url

        # Test with an already full URL
        relative_url = "read_place/Example"
        full_url = "wikipedia.org/wiki/Example"
        assert GeosearchResult.get_article_url(full_url) == relative_url

        # Test with an empty string
        empty_url = ""
        assert GeosearchResult.get_article_url(empty_url) == ""

        # Test with None
        none_url = None
        assert GeosearchResult.get_article_url(none_url) == ""
