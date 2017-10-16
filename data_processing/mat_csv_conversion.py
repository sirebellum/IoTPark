import scipy.io as sio

import os
import glob
import pandas as pd
import xml.etree.ElementTree as ET
from PIL import Image

def mat_to_csv(mat_list, mat_struct, lower, upper):

    for i in range(lower, upper):
        for j in range (0, int(mat_struct[0,i][0].size/4)-1):
            filename = mat_struct[0,i][1][0]+'.jpg'
            xmin = mat_struct[0,i][0][j][0]
            ymin = mat_struct[0,i][0][j][1]
            xmax = mat_struct[0,i][0][j][2]
            ymax = mat_struct[0,i][0][j][3]
            
            im = Image.open('images/'+filename)
            width = im.size[0]
            height = im.size[1]
            
            value = (filename,
                     width,
                     height,
                     'car',
                     xmin,
                     ymin,
                     xmax,
                     ymax
                     )
            mat_list.append(value)


def main():

    mat_list = []
    column_name = ['filename', 'width', 'height', 'class', 'xmin', 'ymin', 'xmax', 'ymax']

    
    ### Pull data from trainset_annos.mat ###
    set = 'train' #train or test set
    mat_contents = sio.loadmat('annotations/'+set+'set_annos.mat')
    mat_struct = mat_contents[set] #retrieve contents from struct name $set
    mat_to_csv(mat_list, mat_struct, 0, mat_struct.size-1) #Appends rows onto list structure

    set = 'test' #train or test set
    mat_contents = sio.loadmat('annotations/'+set+'set_annos.mat')
    mat_struct = mat_contents[set] #retrieve contents from struct name $set
    mat_to_csv(mat_list, mat_struct, 0, 29) #Appends rows onto list structure
    
    mat_df = pd.DataFrame(mat_list, columns=column_name)
    
    set = 'train' #train or test set
    
    mat_df.to_csv('annotations/car_labels_'+set+'.csv', index=None) #Write list to actual csv file
    
    ### Pull data from testset_annos.mat ###
    mat_list = [] #Clear data from trainset
    
    set = 'test' #train or test set
    mat_contents = sio.loadmat('annotations/'+set+'set_annos.mat')
    mat_struct = mat_contents[set] #retrieve contents from struct named $set
    mat_to_csv(mat_list, mat_struct, 30, mat_struct.size-1)

    mat_df = pd.DataFrame(mat_list, columns=column_name)
    mat_df.to_csv('annotations/car_labels_'+set+'.csv', index=None)

    print('Successfully converted xml to csv.')
    
    #print (mat_struct[0,0][0]) #format: mat_struct[0, image_entry][0 = corners/1 = file name][car_entry][xy coordinates]


main()