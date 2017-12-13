###fma hardware accelerators###
pip install --ignore-installed ~/tensorflow_builds/tensorflow.fma/tensorflow-1.4.1-cp36-cp36m-linux_x86_64.whl
python train.py --logtostderr \
                --train_dir=/home/clearlab/gits/IoTPark/training/train_dir/rcnn_resnet_ww48_fma \
                --pipeline_config_path=/home/clearlab/gits/IoTPark/training/feature_extractors/faster_rcnn_resnet101_coco_2017_11_08/faster_rcnn_resnet101_coco_2017_11_08.config
pip uninstall -y tensorflow tensorflow-tensorboard

###sse hardware accelerators###
pip install --ignore-installed ~/tensorflow_builds/tensorflow.sse/tensorflow-1.4.1-cp36-cp36m-linux_x86_64.whl
python train.py --logtostderr \
                --train_dir=/home/clearlab/gits/IoTPark/training/train_dir/rcnn_resnet_ww48_sse \
                --pipeline_config_path=/home/clearlab/gits/IoTPark/training/feature_extractors/faster_rcnn_resnet101_coco_2017_11_08/faster_rcnn_resnet101_coco_2017_11_08.config
pip uninstall -y tensorflow tensorflow-tensorboard
