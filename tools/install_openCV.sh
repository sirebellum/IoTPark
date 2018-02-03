cores=$1
if [ -z $1 ]
then
    echo "Please specify a core count to use for make -j# ie. ./install_openCV.sh 4"
    exit
fi

# Install prereqs
sudo yum install build-essential cmake pkg-config
sudo yum install libjpeg-devel libtiff5-devel libjasper-devel libpng12-devel
sudo yum install libavcodec-devel libavformat-devel libswscale-devel libv4l-devel
sudo yum install libxvidcore-devel libx264-devel
sudo yum install libgtk2.0-devel
sudo yum install libatlas-base-devel gfortran
sudo yum install gstreamer1-plugins-bad-free-devel.x86_64

sudo yum install epel-release
sudo yum install python36
curl -O https://bootstrap.pypa.io/get-pip.py
sudo /usr/bin/python36 get-pip.py

sudo rpm --import http://li.nux.ro/download/nux/RPM-GPG-KEY-nux.ro
sudo rpm -Uvh http://li.nux.ro/download/nux/dextop/el7/x86_64/nux-dextop-release-0-5.el7.nux.noarch.rpm


# Unified directory for building
mkdir open_cv
cd open_cv

# Download source
wget https://codeload.github.com/opencv/opencv/zip/3.4.0 -O opencv-3.4.0.zip
wget https://codeload.github.com/opencv/opencv_contrib/zip/3.4.0 -O opencv_contrib-3.4.0.zip

# unzip
unzip opencv-3.4.0.zip
unzip opencv_contrib-3.4.0.zip

# python prereqs
sudo pip install numpy

# cmake
cd opencv-3.4.0
mkdir build
cd build
cmake -D CMAKE_BUILD_TYPE=RELEASE \
      -D CMAKE_INSTALL_PREFIX=/usr/local \
      -D INSTALL_PYTHON_EXAMPLES=ON \
      -D OPENCV_EXTRA_MODULES_PATH=../../opencv_contrib-3.4.0/modules \
      -D WITH_FFMPEG=1 \
      -D BUILD_EXAMPLES=ON  ..

echo "Does the cmake output look good? y/n"
read input
if [ $input != "y" ]
then
    exit
fi

make -j$cores
echo "Does the make output look good? y/n"
read input2
if [ $input2 != "y" ]
then
    exit
fi
sudo make install
sudo ldconfig

echo "Installation complete! Feel free to delete open_cv/"
