from math import cos, pi, sin, log


## Clip the input number to a max or min value
def clip(number, min_value, max_value):
    return min(max(number, min_value), max_value)

## Get map size from level
def get_map_size(level):
    return int(256*2**level)

## Get pixel coordinates
def get_pixel_xy(latitude, longitude, level):
    latitude=clip(latitude, -85.05113, 85.05113)
    longitude=clip(longitude, -180, 180)
    #print('lat',latitude)
    #print('lon',longitude)

    x=(longitude+180)/360
    sin_lat=sin(latitude * pi/180)
    y=0.5-log((1+sin_lat)/(1-sin_lat))/(4*pi)
    map_size=get_map_size(level)

    pixel_x=int(clip(x * map_size + 0.5, 0, map_size-1))
    pixel_y=int(clip(y * map_size + 0.5, 0, map_size-1))

    return (pixel_x,pixel_y)


## Get tile position
def get_tile_position(pixels):
    tile_x=int(pixels[0]/256)
    tile_y=int(pixels[1]/256)


    return (tile_x, tile_y)

def get_tile_from_latlon(lat,lon,level):
    pixels = get_pixel_xy(lat,lon,level)
    tile_x, tile_y = get_tile_position(pixels)

    return (tile_x, tile_y)

## Get quad key string
def get_quad_keyq(tiles, level):

    quad_key=""

    while level>0:
        mask=1<<(level-1)
        d=0
        if((tiles[0] & mask)!=0):
            d+=1
        if((tiles[1] & mask)!= 0):
            d+=2

        quad_key = quad_key + str(d)
        level-=1

    return quad_key
def get_quad_key(tiles, level):
    """
    :param tileX: 
    :param tileY: 
    :param level: 
    :return: quad key
    """
    quad_key = str()
    for i in range(level, 0, -1):
        d = '0'
        m = (1<<(i-1)) & 0xffffffff
        if (tiles[0] & m) != 0:   d = chr(ord(d) + 1)

        if (tiles[1] & m) != 0:
            d = chr(ord(d) + 1)
            d = chr(ord(d) + 1)
        quad_key += d
    return quad_key

def correct_inputs(x, y):
    right_1=max(x[1],y[1])
    right_0=max(x[0],y[0])
    left_0=min(x[0],y[0])
    left_1 = min(x[1], y[1])

    x=(left_0, left_1)
    y=(right_0, right_1)

    return (x, y)

      
        