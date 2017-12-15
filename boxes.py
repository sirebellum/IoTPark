import time
import cv2
import os
import numpy as np
import tensorflow as tf

from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as vis_util

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("frozen_model", help="Specify model ie. rcnn_resnet_ww48c")
args = parser.parse_args()

CWD_PATH = os.getcwd()
PATH_TO_CKPT = os.path.join(CWD_PATH, 'training/frozen', args.frozen_model, 'frozen_inference_graph.pb')
PATH_TO_LABELS = os.path.join(CWD_PATH, 'data_processing', 'data', 'object-detection.pbtxt')

NUM_CLASSES = 1

# Loading label map
label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
category_index = label_map_util.create_category_index(categories)

def detect_objects(image_np, sess, detection_graph):
    # Expand dimensions since the model expects images to have shape: [1, None, None, 3]
    image_np_expanded = np.expand_dims(image_np, axis=0)
    image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')

    # Each box represents a part of the image where a particular object was detected.
    boxes = detection_graph.get_tensor_by_name('detection_boxes:0')

    # Each score represent how level of confidence for each of the objects.
    # Score is shown on the result image, together with the class label.
    scores = detection_graph.get_tensor_by_name('detection_scores:0')
    classes = detection_graph.get_tensor_by_name('detection_classes:0')
    num_detections = detection_graph.get_tensor_by_name('num_detections:0')

    # Actual detection.
    (boxes, scores, classes, num_detections) = sess.run(
        [boxes, scores, classes, num_detections],
        feed_dict={image_tensor: image_np_expanded})

    # Visualization of the results of a detection.
    vis_util.visualize_boxes_and_labels_on_image_array(
        image_np,
        np.squeeze(boxes),
        np.squeeze(classes).astype(np.int32),
        np.squeeze(scores),
        category_index,
        use_normalized_coordinates=True,
        line_thickness=5,
        max_boxes_to_draw=1000)

    return image_np, boxes, scores


###MAIN###

video_capture = cv2.VideoCapture('input.avi')
width = video_capture.get(3)  # float
height = video_capture.get(4) # float

#frame = cv2.imread('image.jpg')
#height, width, channels = frame.shape

detection_graph = tf.Graph()
with detection_graph.as_default():
    od_graph_def = tf.GraphDef()
    with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
        serialized_graph = fid.read()
        od_graph_def.ParseFromString(serialized_graph)
        tf.import_graph_def(od_graph_def, name='')

    sess = tf.Session(graph=detection_graph)

while True:

	num_cars = 0
	beginning = time.time()

	_, frame = video_capture.read()
	frame2, boxes, scores = detect_objects(frame, sess, detection_graph)
	#boxes = [upper-y, upper-x, lower-y, lower-x] : float of image resolution

	for x in range(0, len(boxes[0])):
		if scores[0][x] >= 0.5: #Only print if confidence score above threshold
			num_cars = num_cars + 1
			print(int((boxes[0][x][1]*width+boxes[0][x][0]*height)/2),
			      int((boxes[0][x][3]*width+boxes[0][x][2]*height)/2))

	fps = 1/(time.time()-beginning)
	print(num_cars, "cars present.")
	print("FPS:", fps)