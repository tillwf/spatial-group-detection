from math import radians, cos, sin, asin, sqrt


def haversine(X, Y):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    """
    lat1, lon1 = X
    lat2, lon2 = Y

    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    # Radius of earth in kilometers. Use 3956 for miles
    r = 6371
    return c * r


def haversine_acc(X, Y):

    lat1, lon1, ac1 = X
    lat2, lon2, ac2 = Y

    ac1 = ac1 * 0.001
    ac2 = ac2 * 0.001

    distance = haversine((lat1, lon1), (lat2, lon2))

    min_distance = max(0, distance - ac2 - ac1)
    max_distance = distance + ac1 + ac2

    return (max_distance + min_distance) / 2
