Street Parking Dataset
======================

Description
-----------

Although the recently proposed KITTI dataset [1] and Pascal VOC dataset [2] are very challenging and widely used, the camera viewpoints are relatively restricted due to the camera platform (e.g., no bird view), and there is a less number of cars in each image than the ones in parking lot images. Our self-collected parking lot dataset provides more features on these two aspects.This dataset has more diversity in terms of viewpoints and
occlusions. It contains 65 training images and 63 testing images, with 3346 cars (including left-right mirrored ones) for training and 2015 cars for testing.For more features of our dataset, please refer to [3]. Most of the images are collected by searching the internet.


Annotation
----------

Train and test annotations are available inside the trainset_annos.mat and testset_annos.mat, respectively. There are basically two fields in each image annotation: "BB" for all the single car bounding boxes, and "im" for the corresponding image name. For each bounding box, we annotate the top left corner and bottom right corner in image coordinate.


Citing
------

If you make use of this dataset, please cite our iccv paper [1] in any publication.


Contact
-------

Please feel free to contact the first author or corresponding author for any questions.

Bo Li <boli86@bit.edu.cn>
or
Tianfu Wu <tfwu@stat.ucla.edu>


References:
-----------

[1] Geiger, A., Lenz, P., Urtasun, R.: Are we ready for autonomous driving? the kitti vision benchmark suite. In: CVPR (2012)

[2] Everingham, M., Van Gool, L., Williams, C., Winn, J., Zisserman, A.: The pascal visual object classes (voc) challenge. IJCV (2010)

[3] Li, B., Wu T.
