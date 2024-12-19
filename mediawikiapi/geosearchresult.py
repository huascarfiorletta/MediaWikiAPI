import datetime

import dateutil


class GeosearchResult(object):
    """
    Contains data from a Geosearch query page.
    """
    title: str
    description: str
    thumbnail: str
    article_url: str
    avg_page_views: float
    latitude: float
    longitude: float
    extract: str
    index: int
    length: int
    touched: datetime

    def __init__(self, page_dict: dict[str, any]):
        self.title = page_dict['title']
        self.description = page_dict['description'] if "description" in page_dict else ''
        self.thumbnail = page_dict['thumbnail']['source'] if "thumbnail" in page_dict else ''
        self.article_url = "read_place/" + page_dict['fullurl'].split("/")[-1] if "fullurl" in page_dict else ''
        self.avg_page_views = -1
        if "pageviews" in page_dict:
            self.avg_page_views = 0
            pageviews_counts = list(page_dict['pageviews'].values())
            for views_count in pageviews_counts:
                if views_count is not None:
                    self.avg_page_views = self.avg_page_views + views_count
            self.avg_page_views = self.avg_page_views / len(pageviews_counts)
        self.latitude = page_dict['coordinates'][0]['lat'] if "coordinates" in page_dict else None
        self.longitude = page_dict['coordinates'][0]['lon'] if "coordinates" in page_dict else None
        self.extract = page_dict['extract'] if "extract" in page_dict else None
        self.index = page_dict['index'] if "index" in page_dict else None
        self.length = page_dict['length'] if "length" in page_dict else None
        self.touched = dateutil.parser.isoparse(page_dict['touched']) if "touched" in page_dict else None


    def __str__(self):
        return f"Title: {self.title} - Description: {self.description}"
