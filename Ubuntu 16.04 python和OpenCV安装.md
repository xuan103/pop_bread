使用 Docker 快速创建 OpenCV 实验环境
<br/>
1. 构建镜像
首先创建Dockerfile

# Use Ubuntu:16.04 image as parent image
FROM ubuntu:16.04

ENV AUTHOR aggresss
ENV DEBIAN_FRONTEND noninteractive

# Modify apt-get to aliyun mirror
WORKDIR /
RUN sed -i 's/archive.ubuntu/mirrors.aliyun/g' /etc/apt/sources.list

# Install necessary library
RUN apt-get update
RUN apt-get -y install apt-utils
RUN apt-get -y install git
RUN apt-get -y install python python-dev python-pip
RUN apt-get -y install lib32z1 libglib2.0-dev libsm6 libxrender1 libxext6 libice6 libxt6 libfontconfig1 libcups2 

# Clone the docker-opencv-python repository
RUN git clone https://github.com/aggresss/docker-opencv-python.git /docker-opencv-python

# Modify pip mirror
WORKDIR /docker-opencv-python
RUN mkdir -p /root/.pip
RUN cp -f pip.conf /root/.pip/

# Install necessary python-library
RUN pip install --upgrade pip
RUN pip install numpy scipy matplotlib pillow
RUN pip install opencv-python
RUN pip install ipython==5.5.0
RUN pip install jupyter

# Modify Jupter run arguments
WORKDIR /docker-opencv-python
RUN mkdir -p /root/.jupyter
RUN cp -f jupyter_config.py /root/.jupyter/
RUN mkdir -p /root/volume

# Make startup run file
WORKDIR /docker-opencv-python
RUN cp -f run.sh /
RUN chmod +x /run.sh
CMD /run.sh

然后执行下面命令构建镜像

docker build -t aggresss/opencv-python .

在10Mbps的网络下大约需要10分钟，构建好镜像后使用 docker images 命令看到构建好的镜像。

2. 运行容器
创建一个目录用于挂载容器的数据

mkdir -p  /data/volume/opencv_python

然后使用下面命令来运行容器

docker run -d \
-p 18881:8888 \
-v /data/volume/opencv_python:/root/volume \
--privileged=true \
--name opencv-python \
aggresss/opencv-python

容器运行后就可以在浏览器中输入 http://ip:18881 来访问Jupyter 服务了，默认密码是: 12345678

也可以使用 docker-compose 的方式启动容器，编写docker-compose.yml 文件如下

version: '2'
services:
  opencv-python:
    image: aggresss/opencv-python
    privileged: true
    command: /run.sh
    ports:
      - "18881:8888"
    volumes:
      - /data/volume/opencv_python:/root/volume

然后使用下面命令运行容器

docker-compose up -d 

3. 共享镜像
  上面所有提到的文件可以在 https://github.com/aggresss/docker-opencv-python 下载，镜像构建好后为了方便分享可以上传到dockerhub上面，或者私有的registry里面。到 www.dockerhub.com 上面注册一个帐号并创建一个与需要上传的镜像同名的repo， 然后在本地使用登录命令

docker login

再使用下面命令将镜像上传

docker push aggresss/opencv-python 

dockerhub同时支持使用github上面的dockerfile自动构建镜像的方式，可以查看dockerhub的文档去了解。

参考文档：
https://docs.docker.com/
https://github.com/aggresss/docker-opencv-python
————————————————
版权声明：本文为CSDN博主「aggresss」的原创文章，遵循 CC 4.0 BY-SA 版权协议，转载请附上原文出处链接及本声明。
原文链接：https://blog.csdn.net/aggresss/article/details/79381030
