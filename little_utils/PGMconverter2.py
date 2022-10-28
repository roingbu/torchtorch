import os
from PIL import Image


file_src_path = "./pgm/"	# store jpg images
file_des_path = "./jpg/"	# storing pgm format 


def jpg2pgm(file_src_path, file_des_path):
    images = os.listdir(file_src_path)

    for image in images:
        current_image = image[:-3] + "jpg"  # pgm2jpg:convert pgm to jpg
        print("Writing jpg image to pgm file: %s" % current_image)
        Image.open(file_src_path+image).save(file_des_path+current_image)


if __name__ == "__main__":
    jpg2pgm(file_src_path, file_des_path)
