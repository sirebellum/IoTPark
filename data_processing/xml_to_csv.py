import scipy.io as sio

import os
import glob
import pandas as pd
import xml.etree.ElementTree as ET
from PIL import Image

def num_files(path):
    return len(os.listdir(path))

def parse_xml(anno_list, filename):

    im = Image.open(filename+'.jpg')
    tree = ET.parse(filename+'.xml')
    root = tree.getroot()

    width = im.size[0]
    height = im.size[1]

    for child in root:
        if child.get('occupied') == '1':
            xmin = child[1][0].get('x') #xy coordinates of included annotations are weirdly formated
            xmax = child[1][0].get('x')

            x1 = child[1][1].get('x')
            x2 = child[1][2].get('x')
            x3 = child[1][3].get('x')

            if x1 < xmin: xmin = x1 #this code serves to record only the min and max of xy
            if x1 > xmax: xmax = x1
            if x2 < xmin: xmin = x2
            if x2 > xmax: xmax = x2
            if x3 < xmin: xmin = x3
            if x3 > xmax: xmax = x3

            ymin = child[1][0].get('y') #xy coordinates of included annotations are weirdly formated
            ymax = child[1][0].get('y')

            y1 = child[1][1].get('y')
            y2 = child[1][2].get('y')
            y3 = child[1][3].get('y')

            if y1 < ymin: ymin = y1 #this code serves to record only the min and max of xy
            if y1 > ymax: ymax = y1
            if y2 < ymin: ymin = y2
            if y2 > ymax: ymax = y2
            if y3 < ymin: ymin = y3
            if y3 > ymax: ymax = y3

            value = (filename.replace('images_new/', '')+'.jpg',
                     width,
                     height,
                     'car',
                     xmin,
                     ymin,
                     xmax,
                     ymax
                     )
            anno_list.append(value)

def main():

    anno_list = []
    column_name = ['filename', 'width', 'height', 'class', 'xmin', 'ymin', 'xmax', 'ymax']

    x = 0
    for infile in glob.glob("images_new/*.jpg"):
        file, ext = os.path.splitext(infile)
        parse_xml(anno_list, file)
        x = x + 1
        if x == 11000:
            anno_df = pd.DataFrame(anno_list, columns=column_name)
            anno_df.to_csv('car_labels_train.csv', index=None) #Write list to actual csv file
            anno_list = []

    anno_df = pd.DataFrame(anno_list, columns=column_name)
    anno_df.to_csv('car_labels_test.csv', index=None) #Write list to actual csv file

main()
