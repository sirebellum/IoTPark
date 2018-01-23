# Import TensorRT Modules
import tensorrt as trt
import uff
import os
from tensorrt.parsers import uffparser
G_LOGGER = trt.infer.ConsoleLogger(trt.infer.LogSeverity.INFO)

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("frozen_model", help="Specify model ie. rcnn_resnet_ww48c")
args = parser.parse_args()

CWD_PATH = os.getcwd()
PATH_TO_CKPT = os.path.join(CWD_PATH, args.frozen_model, 'frozen_inference_graph.pb')

# Load your newly created Tensorflow frozen model and convert it to UFF
uff_model = uff.from_tensorflow_frozen_model(PATH_TO_CKPT, ["detection_scores"])
#detection_boxes,detection_scores,detection_classes,num_detections