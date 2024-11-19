from unittest import TestCase

from mediawikiapi import MediaWikiAPI, GeosearchResult

STOCKHOLM = (59.32558360695936, 18.070745550255786)
ROME = (41.902011993223006, 12.493929510107037)
NYC = (40.80773442954472, -73.96254051668487)

mediawikiapi = MediaWikiAPI()


class Test(TestCase):

    def test_wiki_geo_query(self):
        number_of_results = 50
        places: list[GeosearchResult] = mediawikiapi.geosearch_pages(ROME[0],
                                                                     ROME[1], radius=10000, results=number_of_results)
        assert len(places) == number_of_results
        # ensure all places have coordinates
        for place in places:
            assert place.latitude
            assert place.longitude
            assert place.page_views

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

    def test_pageviews(self):
        number_of_results = 50
        pages_without_pageviews = []
        for city in [ROME, STOCKHOLM, NYC]:
            pages: list[GeosearchResult] = mediawikiapi.geosearch_pages(city[0],
                                                                        city[1], radius=10000,
                                                                        results=number_of_results)
            assert len(pages) == number_of_results
            cnt_pages_without_pageviews = 0
            for current_page in pages:
                if current_page.page_views is None:
                    cnt_pages_without_pageviews += 1
                    pages_without_pageviews.append(current_page.title)
            try:
                assert cnt_pages_without_pageviews == 0
            except AssertionError:
                print(f"{cnt_pages_without_pageviews} pages out of {number_of_results} have no page views.")
                print(pages_without_pageviews)
                raise