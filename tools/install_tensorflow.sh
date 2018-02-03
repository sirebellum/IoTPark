echo "Installing Bazel (and prereqs)..."
sleep 1

# Bazel prereqs
sudo yum install build-essential sudo yum install java-1.8.0-openjdk-devel-1:1.8.0.151-5.b12.el7_4.x86_64 java-1.8.0-openjdk-headless-1:1.8.0.151-5.b12.el7_4.x86_64 zip

# Bazel installation
wget https://github.com/bazelbuild/bazel/releases/download/0.9.0/bazel-0.9.0-dist.zip
mkdir bazel
mv bazel-0.9.0-dist.zip bazel
cd bazel
unzip bazel-0.9.0-dist.zip

./compile.sh

echo "Does the bazel build output look good? y/n"
read input
if [ $input != "y" ]
then
    exit
fi

sudo cp output/bazel /usr/bin/

yum install gcc gcc-c++ make openssl-devel

# Python prereqs
sudo yum install python3
sudo yum install python3-pip python3-numpy python3-six python3-wheel

# Tensorflow prereqs
sudo yum install coreutils swig
sudo yum install libxml2-devel libxslt-devel libffi-devel gcc musl-devel libgcc1 libssl-devel curl
sudo yum install libjpeg-devel zlib1g-devel libfreetype6-devel liblcms2-devel libopenjpeg-devel libtiff5-devel tk-devel tcl-devel

cd ..

# Install Tensorflow
git clone https://github.com/tensorflow/tensorflow
cd tensorflow
git checkout r1.5
bazel clean
./configure

bazel build -c opt --copt=-mavx --copt=-mavx2 --copt=-mfma --copt=-msse4.1 --copt=-msse4.2 --verbose_failures -k //tensorflow/tools/pip_package:build_pip_package
bazel-bin/tensorflow/tools/pip_package/build_pip_package /tmp/tensorflow_pkg

pip install --upgrade --ignore-installed /tmp/tensorflow_pkg/tensorflow*

echo "Installation complete! Feel free to delete bazel/, tensorflow/, and swapfile"
