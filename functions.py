import time
import cv2
import os
import numpy as np
import tensorflow as tf

from classes import Car

font = cv2.FONT_HERSHEY_SIMPLEX

def track_cars(boxes, scores, cars, width, height, fps):
    
    ###CHECK FOR EXISTING CARS###
    x = 0
    saved = False #Keep track of if a box is new
    for box in boxes[0]:
        if scores[0][x] >= 0.5: #Only if confidence score above threshold
            upper_x = box[1]*width
            upper_y = box[0]*height
            lower_x = box[3]*width
            lower_y = box[2]*height
            
            for car in cars:
                if car.distance(upper_x, upper_y, lower_x, lower_y) <= car.delta_pos:
                    car.update(upper_x, upper_y, lower_x, lower_y, fps)
                    saved = True #Don't double up on detections
            
            if not saved:
                cars.append(Car(upper_x, upper_y, lower_x, lower_y)) #Uppercase Car is a class

        x = x + 1 #Index for scores
        saved = False


def persistence(cars, width, height):

    num_cars = 0 #Reset for counting cars in a frame
    ###Persistence calculations###    
    for car in cars:
        if car.persistence < 0:
            car.kill()

        else:
            car.update_persistence(width, height)
            num_cars = num_cars + 1
            car.detected = 0 #reset for next run
    
    return num_cars
    

def draw_boxes(cars, frame):

    for car in cars:
        frame2 = cv2.circle(frame, \
                           (int(car.x), int(car.y)), \
                           5, \
                           (0, 255, 255*(not car.detected)), \
                           -1)
        frame2 = cv2.putText(frame2, \
                            str(round(car.id, 2)), \
                            (int(car.x)+5, int(car.y)), \
                            font, \
                            0.4, \
                            (0, 0, 255), \
                            1, \
                            cv2.LINE_AA)
                        
    return frame2