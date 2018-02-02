echo "Creating 8gb Swapfile for compiling... it can be deleted after script is finished"
sudo ./create_Swapfile.sh

echo "Installing Bazel (and prereqs)..."
sleep 2

# Bazel prereqs
sudo apt-get install build-essential openjdk-8-jdk python zip

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


# Python prereqs
sudo apt-get install python3
sudo apt-get install python3-pip python3-numpy python3-six python3-wheel

# Tensorflow prereqs
sudo apt-get install coreutils swig
sudo apt-get install libxml2-dev libxslt-dev libffi-dev gcc musl-dev libgcc1 libssl-dev curl
sudo apt-get install libjpeg-dev zlib1g-dev libfreetype6-dev liblcms2-dev libopenjpeg-dev libtiff5-dev tk-dev tcl-dev

cd ..

# Install Tensorflow
git clone https://github.com/tensorflow/tensorflow
cd tensorflow
git checkout r1.5
bazel clean
./configure

bazel build -c opt --verbose_failures -k //tensorflow/tools/pip_package:build_pip_package
bazel-bin/tensorflow/tools/pip_package/build_pip_package /tmp/tensorflow_pkg

pip install --upgrade --ignore-installed /tmp/tensorflow_pkg/tensorflow*

echo "Installation complete! Feel free to delete bazel/, tensorflow/, and swapfile"
