#Ubuntu 16.04 python和OpenCV安装

1. 首先更新相关的package：

    $ apt-get update

    $ apt-get install build-essential cmake git libgtk2.0-dev pkg-config libavcodec-dev libavforma


编译OpenCV需要用到下面的一些package：

GCC
CMake
GTK+2.x or higher
pkg-config
ffmpeg or libav development packages: libavcodec-dev, libavformat-dev, libswscale-dev



2. 下载python：
Ubuntu默认带了各个版本的python，如果没有的话，可以很方便的安装：

    $ apt-get install python3.5-dev
    
    
3. 下载OpenCV的源码
OpenCV官网上有linux版本的源码包可以下载，不过最好是从git上下载，这样可以保证下载得到的是最新的代码：

    $ wget -O opencv.zip https://github.com/Itseez/opencv/archive/3.2.0.zip

    $ unzip opencv.zip
    
    
4. 编译安装
进入到OpenCV的文件夹中，创建一个build目录，进行编译：

cd opencv-3.2.0
mkdir build
cd build
cmake -D CMAKE_BUILD_TYPE=RELEASE -D CMAKE_INSTALL_PREFIX=/usr/local ..
make -j4
sudo make install
5. 测试是否安装成功
python
>>>import cv2
>>>cv2.__version__ 
'3.2.0'
————————————————
版权声明：本文为CSDN博主「cyn618」的原创文章，遵循 CC 4.0 BY-SA 版权协议，转载请附上原文出处链接及本声明。
原文链接：https://blog.csdn.net/cyn618/article/details/64494434

ImportError: No module named pip
python -m ensurepip
apt-get install python3.5

For older versions of Ubuntu
Install Easy Install
$ sudo apt-get install python-setuptools python-dev build-essential 
Install pip
$ sudo easy_install pip 
Install virtualenv
$ sudo pip install --upgrade virtualenv 
安裝mysql 
apt-get install mysql-server


For Python 3

sudo apt-get install python3-pip
————————————————


Makefile:86: recipe for target 'obj/image_opencv.o' failed

pip install matplotlib



