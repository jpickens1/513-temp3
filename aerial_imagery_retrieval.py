from math import cos, pi, sin, log
import requests
import numpy
import cv2 as cv
import helper

MAX_LEVEL=23

## Load null image to be used for comparison
with open('null_image.npy', 'rb') as f1:
    NULL_IMAGE = numpy.load(f1)


## Input Class
class input_o:
    def __init__(self, left_latitude, left_longitude, right_latitude, right_longitude):
        self.left_latitude=left_latitude
        self.left_longitude=left_longitude
        self.right_latitude=right_latitude
        self.right_longitude=right_longitude
       


## Take user input
def input_main():
    print("Enter left top corner coordinates!\nLatitude: \t")
    latitude_1=float(input())
    print("Longitude: \t")
    longitude_1=float(input())
    print("\nEnter bottom right corner coordinates!\nLatitude: \t")
    latitude_2=float(input())
    print("Longitude: \t")
    longitude_2=float(input())
    return input_o(latitude_1, longitude_1, latitude_2, longitude_2)


## Check if the quad key generated from the given tile coordinates and level can be used to retrieve a valid image of the tile 
## Returns 0 if the retrieved image is null, and returns 1 if the returned image is not null.
def check_null_image(tile_left, tile_right, level):
    i=1
    for i_y in range(tile_left[1], tile_right[1]+1):
        for i_x in range(tile_left[0], tile_right[0]+1):
            quad_key=helper.get_quad_key((i_x, i_y), level)
            image_array=get_image("http://h0.ortho.tiles.virtualearth.net/tiles/h"+quad_key+".jpeg?g=131", "tile_"+str(i)+".jpeg")
            
            # Check if the returned image is a null image, return 0 if retrieved image is null, return 1 otherwise
            # A pre-saved null image will be used to see if the returned image is also null
            if (numpy.array_equal(image_array,NULL_IMAGE)):
                #print("Null image!") 
                return 0
            else:
                return 1
            

## Find the max level of detail for the input bounding box, start with level = 23
def find_max_level(lat1,lon1,lat2,lon2,level):

    # Start with the max level of 23, for each level, check if the return images are null, decrement the level if null images were returned
    while (level>0):
        # At each level, generate tile coordinates of the given lan/lon coordinates at each level
        tile1_x, tile1_y = helper.get_tile_from_latlon(lat1, lon1, level)
        tile2_x, tile2_y = helper.get_tile_from_latlon(lat2, lon2, level)

        # Check if the tile coordinates are correct, if the user inputs are wrong, correct them by swaps the inputs
        (tile_left,tile_right)=helper.correct_inputs((tile1_x,tile1_y),(tile2_x,tile2_y))
        
        # Call the check_null_image() function with the tile coordinates genearted at this level
        # If check_null_image() returns a 1, it indicates that the retrieved image at this level is valid, we've found the max level of detail of this bounding box
        if (check_null_image(tile_left,tile_right,level)==1):
            print ("Max Level Found: %s" % (level))
            return tile_left,tile_right,level
        
        level-=1

    print ("Error: No Max Level Found! \n")  
    sys.exit()


## Download a single image with the given quad key
def get_image(url, image_name):

    response=requests.get(url)

    # Write image to /tiles directory 
    with open("tiles/"+image_name, "wb") as f:
        f.write(response.content)

    image=numpy.asarray(bytearray(response.content), dtype="uint8")
    return cv.imdecode(image, cv.IMREAD_COLOR)



## Download a list of tiles in the bounding box, iterating the rows first then columns
## Returns a list of tiles for stithching
def download_images(tile_left, tile_right, level):

    i=1
    y_image_list=[]
    for i_y in range(tile_left[1], tile_right[1]+1):
        x_image_list=[]
        for i_x in range(tile_left[0], tile_right[0]+1):
            quad_key=helper.get_quad_key((i_x, i_y), level)
            
            image_array=get_image("http://h0.ortho.tiles.virtualearth.net/tiles/h"+quad_key+".jpeg?g=131", "tile_"+str(i)+".jpeg")
            x_image_list.append(image_array)
            i=i+1
            print('.', end='',flush=True)  #Displays progress of tile downloading process

        x_image_concatenated=numpy.concatenate(x_image_list,1)
        y_image_list.append(x_image_concatenated)

    return y_image_list




## Stitch the return tiles
def stitch_images(images):
    images=numpy.concatenate(images, 0)
    cv.imwrite("final_stitched_image.jpeg", images)


if __name__ == '__main__':
    input_object=input_main()
  
    # Find the max level of detail for the input bounding box
    tile_left, tile_right,level= find_max_level(input_object.left_latitude, input_object.left_longitude, input_object.right_latitude, input_object.right_longitude,MAX_LEVEL)


    # Download images at the max level
    print("Downloading the Tiles:  ")
    images=download_images(tile_left, tile_right, level)

    # Stitch images
    print("\nStitching the downloaded tiles! ")
    stitch_images(images)

    

