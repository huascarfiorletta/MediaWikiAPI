import random

ROME = (41.902011993223006, 12.493929510107037)
NYC = (40.80773442954472, -73.96254051668487)
STOCKHOLM = (59.32558360695936, 18.070745550255786)


def get_random_location_in_europe():
    latitude = random.uniform(46.70394858309998, 50.93926644158736)
    longitude = random.uniform(2.8681031672756516, 16.24945016645088)
    return latitude, longitude