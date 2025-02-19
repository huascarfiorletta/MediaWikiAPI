from mediawikiapi import MediaWikiAPI
from unittest.mock import MagicMock, patch, PropertyMock

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


def test_section_with_subsection():
    mediawikiapi = MediaWikiAPI()
    wiki_page = mediawikiapi.page('Kyoto')
    mock_content = """As the capital of Japan from 794 to 1868, Kyoto is sometimes called the thousand-year capital (
    千年の都).\nHistorically, foreign spellings for the city\'s name have included Kioto and Miaco or Meaco.\n\n\n
    == History ==\n\n\n=== Origins ===\n\nAmple archeological evidence suggests human settlement in the area of Kyoto 
    began as early as the Paleolithic period, although not much published material is retained about human activity 
    in the region before the 6th century, around which time the Shimogamo Shrine is believed to have been 
    established. Before Kyoto became the imperial capital, immigrants from mainland Asia contributed to the 
    development of the area.\nDuring the 8th century, when powerful Buddhist clergy became involved in the affairs of 
    the imperial government, Emperor Kanmu chose to relocate the capital in order to distance it from the clerical 
    establishment in Nara. His last choice for the site was the village of Uda, in the Kadono district of Yamashiro 
    Province.\nThe new city, Heian-kyō (平安京, "tranquility and peace capital"), modeled after Chinese Tang dynasty 
    capital Chang\'an, became the seat of Japan\'s imperial court in 794, beginning the Heian period of Japanese 
    history. Although military rulers established their governments either in Kyoto (Muromachi shogunate) or in other 
    cities such as Kamakura (Kamakura shogunate) and Edo (Tokugawa shogunate), Kyoto remained Japan\'s capital until 
    the transfer of the imperial court to Tokyo in 1869 at the time of the Imperial Restoration.Kyoto became a city 
    designated by government ordinance on September 1, 1956. In 1994, 17 historic monuments in Kyoto were inscribed 
    on the list as UNESCO World Heritage Sites. In 1997, Kyoto hosted the conference that resulted in the protocol on 
    greenhouse gas emissions (United Nations Framework Convention on Climate Change).\n\n\n== Geography ==\n\n\n=== 
    Terrain ===\nKyoto is located in a valley, part of the Yamashiro (or Kyoto) Basin, in the eastern part of the 
    mountainous region known as the Tamba highlands. The Yamashiro Basin is surrounded on three sides by mountains 
    known as Higashiyama, Kitayama and Nishiyama (literally "east mountain", "north mountain" and "west mountain" 
    respectively), with a maximum height of approximately 1,000 meters (3,281 ft) above sea level. This interior 
    positioning results in hot summers and cold winters. There are three rivers in the basin, the Uji River to the 
    south, the Katsura River to the west, and the Kamo River to the east. Kyoto City takes up"""
    with patch.object(type(wiki_page), 'content', new_callable=PropertyMock) as mock_content_property:
        mock_content_property.return_value = mock_content
        assert "== History ==" in mock_content
        section = wiki_page.section('History', with_subsections=True)
        assert len(section) > 50
        section = wiki_page.section('Geography', with_subsections=True)
        assert len(section) > 50
        section = wiki_page.section('NotThere', with_subsections=True)
        assert section is None

