"""
Usage:
  python generate_tfrecord.py --csv_input=data/train_labels.csv \
			      --output_path=relative/path/ \
			      --train_ratio=float
                              --label_map=data/thingy.pbtxt
"""
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

import os
import io
import pandas as pd
import tensorflow as tf

from PIL import Image
import dataset_util
from collections import namedtuple, OrderedDict

import random
import math

flags = tf.app.flags
flags.DEFINE_string('train_ratio', '0.9', 'Ratio of Train to Test data')
flags.DEFINE_string('csv_input', '', 'Path to the CSV input')
flags.DEFINE_string('output_path', '', 'Path to output TFRecord')
flags.DEFINE_string('label_map', '', 'Path to pbtxt label map')
FLAGS = flags.FLAGS


def class_text_to_int(row_label):
    prevline = ""

    with open(FLAGS.label_map, "r") as file:
        for line in file:
            if row_label in line: return int(prevline.replace("  id:", ""))
            prevline = line


def split(df, group):
    data = namedtuple('data', ['filename', 'object'])
    gb = df.groupby(group)
    return [data(filename, gb.get_group(x)) for filename, x in zip(gb.groups.keys(), gb.groups)]


def create_tf_example(group, path):
    with tf.gfile.GFile(os.path.join(path, '{}'.format(group.filename)), 'rb') as fid:
        encoded_jpg = fid.read()
    encoded_jpg_io = io.BytesIO(encoded_jpg)
    image = Image.open(encoded_jpg_io)
    width, height = image.size

    filename = group.filename.encode('utf8')
    image_format = b'jpg'
    xmins = []
    xmaxs = []
    ymins = []
    ymaxs = []
    classes_text = []
    classes = []

    for index, row in group.object.iterrows():
        xmins.append(row['xmin'] / width)
        xmaxs.append(row['xmax'] / width)
        ymins.append(row['ymin'] / height)
        ymaxs.append(row['ymax'] / height)
        classes_text.append(row['class'].encode('utf8'))
        classes.append(class_text_to_int(row['class']))

    tf_example = tf.train.Example(features=tf.train.Features(feature={
        'image/height': dataset_util.int64_feature(height),
        'image/width': dataset_util.int64_feature(width),
        'image/filename': dataset_util.bytes_feature(filename),
        'image/source_id': dataset_util.bytes_feature(filename),
        'image/encoded': dataset_util.bytes_feature(encoded_jpg),
        'image/format': dataset_util.bytes_feature(image_format),
        'image/object/bbox/xmin': dataset_util.float_list_feature(xmins),
        'image/object/bbox/xmax': dataset_util.float_list_feature(xmaxs),
        'image/object/bbox/ymin': dataset_util.float_list_feature(ymins),
        'image/object/bbox/ymax': dataset_util.float_list_feature(ymaxs),
        'image/object/class/text': dataset_util.bytes_list_feature(classes_text),
        'image/object/class/label': dataset_util.int64_list_feature(classes)
    }))
    return tf_example


def main(_):
    path = os.path.join(os.getcwd(), 'images')
    examples = pd.read_csv(FLAGS.csv_input)
    grouped = split(examples, 'filename')

    ###Randomize images for test and train dataset###
    num_images = len(grouped)
    train_images = int(math.ceil(num_images * float(FLAGS.train_ratio)))
    print ('Writing', num_images, 'images:', train_images, 'train_images |', num_images-train_images, 'test images')
    random.shuffle(grouped)

    ###Create Train tfrecord###
    path_to_write = FLAGS.output_path #record for later use with test.record
    FLAGS.output_path = path_to_write + 'train.record' #flag must be a .record file otherwise error
    writer = tf.python_io.TFRecordWriter(FLAGS.output_path)

    for x in range(0, train_images):
        tf_example = create_tf_example(grouped[x], path)
        writer.write(tf_example.SerializeToString())

    writer.close()
    output_path = os.path.join(os.getcwd(), FLAGS.output_path)
    print('Successfully created the train TFRecord: {}'.format(output_path))


    ###Create Test tfrecord###
    FLAGS.output_path = path_to_write + 'test.record'
    writer = tf.python_io.TFRecordWriter(FLAGS.output_path)

    for x in range(train_images, num_images):
        tf_example = create_tf_example(grouped[x], path)
        writer.write(tf_example.SerializeToString())

    writer.close()
    output_path = os.path.join(os.getcwd(), FLAGS.output_path)
    print('Successfully created the test TFRecord: {}'.format(output_path))


if __name__ == '__main__':
    tf.app.run()
