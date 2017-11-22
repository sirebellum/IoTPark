#Convert from csv to labelImg compatible xml for bounding box editing

import csv

def do_stuff(csvfile):
	readCSV = csv.reader(csvfile, delimiter=',')
	
	line = 0
	
	for row in readCSV:
		if line == 0: pfilename = "filename" #if doesn't execute further down for first line in csv
		
		filename = row[0]
		
		if filename != pfilename:
			
			if line != 0:
				xmlfile.write("</annotation>")
				xmlfile.close()
			
			line = line + 1
		
			width = row[1]
			height = row[2]
			
			xmlfile = open(filename.replace(".jpg", "")+".xml" ,"w+")
			xmlfile.write("<annotation><folder>images_new</folder><filename>"+filename+"</filename><path>/mnt/c/Users/temp/gits/images_new/"+filename+"</path><source><database>Unknown</database></source><size><width>"+width+"</width><height>"+height+"</height><depth>3</depth></size><segmented>0</segmented>"+"\n")
		
		xmin = row[4]
		ymin = row[5]
		xmax = row[6]
		ymax = row[7]
		
		if line != 0: xmlfile.write("<object><name>car</name><pose>Unspecified</pose><truncated>0</truncated><difficult>0</difficult><bndbox><xmin>"+xmin+"</xmin><ymin>"+ymin+"</ymin><xmax>"+xmax+"</xmax><ymax>"+ymax+"</ymax></bndbox></object>"+"\n")
		
		pfilename = filename



with open('dirty_car_labels_test.csv') as testfile:
	do_stuff(testfile)
	
with open('dirty_car_labels_train.csv') as trainfile:
	do_stuff(trainfile)