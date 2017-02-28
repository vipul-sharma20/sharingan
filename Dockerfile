FROM python:3.6

MAINTAINER Vipul <vipul.sharma20@gmail.com>

RUN apt-get -y update
RUN apt-get -y install wget unzip \
                       build-essential cmake git pkg-config libatlas-base-dev gfortran \
                       libjasper-dev libgtk2.0-dev libavcodec-dev libavformat-dev \
                       libswscale-dev libjpeg-dev libpng-dev libtiff-dev
libjasper-dev libv4l-dev
RUN apt-get -y install tesseract-ocr

RUN wget https://bootstrap.pypa.io/get-pip.py && python get-pip.py
ADD requirements.txt .
RUN pip3 install -r requirements.txt

RUN wget https://github.com/Itseez/opencv/archive/3.2.0.zip && unzip 3.2.0.zip \
    && mv opencv-3.2.0 /opencv

RUN mkdir /opencv/release
WORKDIR /opencv/release

RUN cmake -DBUILD_TIFF=ON \
		-DBUILD_opencv_java=OFF \
		-DWITH_CUDA=OFF \
		-DENABLE_AVX=ON \
		-DWITH_OPENGL=ON \
		-DWITH_OPENCL=ON \
		-DWITH_IPP=OFF \
		-DWITH_TBB=ON \
		-DWITH_EIGEN=ON \
		-DWITH_V4L=ON \
		-DWITH_VTK=OFF \
		-DBUILD_TESTS=OFF \
		-DBUILD_PERF_TESTS=OFF \
		-DCMAKE_BUILD_TYPE=RELEASE \
		-DBUILD_opencv_python2=OFF \
		-DCMAKE_INSTALL_PREFIX=$(python3.6 -c "import sys; print(sys.prefix)") \
		-DPYTHON3_EXECUTABLE=$(which python3.6) \
		-DPYTHON3_INCLUDE_DIR=$(python3.6 -c "from distutils.sysconfig import get_python_inc; print(get_python_inc())") \
		-DPYTHON3_PACKAGES_PATH=$(python3.6 -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())") ..

RUN make -j4
RUN make install

CMD ["bash"]
