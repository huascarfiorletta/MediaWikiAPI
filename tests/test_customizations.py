from unittest import TestCase

from mediawikiapi import MediaWikiAPI, GeosearchResult
from prototyping.location_coordinates import ROME, STOCKHOLM, NYC

mediawikiapi = MediaWikiAPI()


class Test(TestCase):

    def test_wiki_geo_query(self):
        number_of_results = 20
        places: list[GeosearchResult] = mediawikiapi.geosearch_pages(STOCKHOLM[0],
                                                                     STOCKHOLM[1], radius=10000, results=number_of_results)
        assert len(places) == number_of_results
        # ensure all places have coordinates
        for place in places:
            assert place.title
            assert place.article_url
            assert place.avg_page_views
            assert place.latitude
            assert place.longitude
            assert place.extract
        # at least one thumbnail
        thumbnails = [place.thumbnail for place in places]
        assert len(thumbnails) > 0
        # at least one description
        descriptions = [place.description for place in places]
        assert len(descriptions) > 0
    
    def test_wiki_page_from_title(self):
        titles = ["Little Rock", "Rome"]
        for title in titles:
            wp = mediawikiapi.page(title)
            try:
                assert wp
                assert wp.title
                assert wp.thumbnail
                assert wp.url
                assert wp.latitude
                assert wp.longitude
                assert wp.categories
                assert wp.images
            except AssertionError:
                print(f"Page '{title}'")
                raise
