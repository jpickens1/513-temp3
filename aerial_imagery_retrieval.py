from math import cos, pi, sin, log
import requests
import numpy
import cv2 as cv
import helper

MAX_LEVEL=23

# Load null image to be used for comparison
with open('null_image.npy', 'rb') as f1:
    NULL_IMAGE = numpy.load(f1)


# Input Class
class input_o:
    def __init__(self, left_latitude, left_longitude, right_latitude, right_longitude):
        self.left_latitude=left_latitude
        self.left_longitude=left_longitude
        self.right_latitude=right_latitude
        self.right_longitude=right_longitude
       


# Take input
def input_main():
    #print("Enter Ground resolution! Between 1 and 23! ")
    #level=int(input())
    print("Enter left top corner coordinates!\nLatitude: \t")
    latitude_1=float(input())
    print("Longitude: \t")
    longitude_1=float(input())
    print("\nEnter bottom right corner coordinates!\nLatitude: \t")
    latitude_2=float(input())
    print("Longitude: \t")
    longitude_2=float(input())
    return input_o(latitude_1, longitude_1, latitude_2, longitude_2)




# Get a image with quad key
def get_image(url, image_name):

    response=requests.get(url)

    # Write image to /tiles directory 
    with open("tiles/"+image_name, "wb") as f:
        f.write(response.content)

    image=numpy.asarray(bytearray(response.content), dtype="uint8")
    
    return cv.imdecode(image, cv.IMREAD_COLOR)




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
            print('.', end='',flush=True)


        x_image_concatenated=numpy.concatenate(x_image_list,1)
        y_image_list.append(x_image_concatenated)

    return y_image_list

def check_null_image(tile_left, tile_right, level):
    i=1
    for i_y in range(tile_left[1], tile_right[1]+1):
        for i_x in range(tile_left[0], tile_right[0]+1):
            quad_key=helper.get_quad_key((i_x, i_y), level)
            #print("quadkey: ",quad_key)
            image_array=get_image("http://h0.ortho.tiles.virtualearth.net/tiles/h"+quad_key+".jpeg?g=131", "tile_"+str(i)+".jpeg")
            
            # Check if the returned image is a null image, return 0 if retrieved image is null, return 1 otherwise
            if (numpy.array_equal(image_array,NULL_IMAGE)):
                #print("Null image!") 
                return 0
            else:
                return 1
            

## Find the max level of detail for the input bounding box
def find_max_level(lat1,lon1,lat2,lon2,level):
    # Start with the max level of 23, for each level, check if the return images are null, decrement the level if null images were returned
    while (level>0):
        tile1_x, tile1_y = helper.get_tile_from_latlon(lat1, lon1, level)
        tile2_x, tile2_y = helper.get_tile_from_latlon(lat2, lon2, level)
        (tile_left,tile_right)=helper.correct_inputs((tile1_x,tile1_y),(tile2_x,tile2_y))
        
        #print("testing level:",level)
        
        # if check_null_image() returns a 1, it indicates that the retrieved image at this level is valid, we are good to proceed
        if (check_null_image(tile_left,tile_right,level)==1):
            print ("Max Level Found: %s" % (level))
            return tile_left,tile_right,level
        
        level-=1

    print ("Error: No Max Level Found! \n")  
    sys.exit()


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

    

