import pyproj


def inverse_num_in_range(num, minNum, maxNum):
    """
        Returns the inverse of a number in a range eg: 
            reverseNumRange(1, 0, 10) => 9
    """
    return (maxNum + minNum) - num


def get_map_string():
    """
        Loads the map from the txt file and returns the string with newLines
    """
    f = open("map.txt")
    return ''.join(f.readlines())


def get_map_string_with_border():
    """
        Loads the map from the txt file and returns the string with newLines and a border
    """
    f = open("map.txt")
    rows, cols = get_map_rows_cols()

    out = "+" + (cols * "-") + "+\n"
    for line in f.readlines():
        out += "|" + line.strip('\n') + "|\n"
    out += "+" + (cols * "-") + "+"

    return out

def get_map_rows_cols():
    """
        Returns the [rows, cols] height and width of the given map 
    """
    map_lines = get_map_string().split('\n')
    widths = []

    for line in map_lines:
        widths.append(len(line.strip('\n')))

    return [len(map_lines), max(widths)] 


def lat_lon_to_X_Y(lat, lon):
    """
        Takes a Lat, Lon pair and return the Mercador projection X, Y suitable for this map
        It ignores the very top and bottom of the map due to them being arctic regions and empty
        Lat range: 
    """
    # sets up the conversion
    crs_from = pyproj.Proj(init='epsg:4326') # standard lon, lat coords
    crs_to = pyproj.Proj(init='epsg:3857')  # Web mercator projection (same as google maps)

    x, y = pyproj.transform(crs_from, crs_to, lon, lat)
    
    # we standardise the coords in the given ranges here, so it becomes a percentage
    xRange = (-20037508.34, 20037508.34)
    yRange = (-20048966.10, 20048966.10)
    x_percent = (x - xRange[0]) / (xRange[1] - xRange[0])
    y_percent = (y - yRange[0]) / (yRange[1] - yRange[0])

    # we then take that percentage and apply it to the map width or height
    mapCols = 69
    mapRows = 41
    mapX = int(x_percent * mapCols)
    mapY = int(y_percent * mapRows)

    # we have to reverse the y 
    mapY = inverse_num_in_range(mapY, 0, mapRows)

    # ANything above or below our 
    topMargin = 10
    bottomMargin = 10
    if mapY - topMargin < 0 or mapY > mapRows-bottomMargin:
        raise ValueError('The Lat, Lon ({}, {}) was above or below our margins'.format(lat, lon))
    
    return mapX, mapY - topMargin

    # addLog("    ({:.2f} - {:.2f}) / ({:.2f} - {:.2f})".format(x, xRange[0], xRange[1], xRange[0]))
    # addLog("    ({:.2f}) / ({:.2f}) = {}".format(x - xRange[0], xRange[1] - xRange[0], x_percent))
    # addLog("    ({:.2f} - {:.2f}) / ({:.2f} - {:.2f})".format(y, yRange[0], yRange[1], yRange[0]))
    # addLog("    ({:.2f}) / ({:.2f}) = {}".format(y - yRange[0], xRange[1] - yRange[0], y_percent))
    # addLog("({:.1f} : {:.1f}) -> ({:.1f}, {:.1f})".format(lon, lat, x, y))
    # addLog("{}  ({:.2f}, {:.2f}) : ({:.2f} x {}, {:.2f} x {})  ->  ({}, {})".format(char, x, y, x_percent, mapRows, y_percent, mapCols, mapX, mapY))
    # addLog("")