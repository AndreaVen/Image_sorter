

from Image_sorter_class import *
import argparse
import sys

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-cl','--class_list', nargs='+', help='<List of classes', required=True)
    parser.add_argument('-p','--path', type=str, required=False,help='path of the images, default is ./images')
    args = parser.parse_args()
    image_folder=args.path
    if image_folder==None:
        image_folder=os.path.join(os.getcwd(),"images")
    folder_names=[i for i in args.class_list]
viewer= image_viewer(image_folder,folder_names)
viewer .start_gui()
viewer.smista()


        

