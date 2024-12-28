from mediawikiapi import MediaWikiAPI
from unittest.mock import MagicMock

from mediawikiapi import MediaWikiAPI


def get_mock_wiki_page(title, coordinates=None):
    mock_page = MagicMock()
    mock_page.title = title
    mock_page.coordinates = coordinates
    return mock_page


def test_get_wiki_page_saint_nicolas_church():
    mediawikiapi = MediaWikiAPI()
    wiki_page = mediawikiapi.page('Saint Nicolas Church')
    assert wiki_page.title
