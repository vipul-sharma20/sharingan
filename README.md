Sharingan
=========

[![Build Status](https://travis-ci.org/vipul-sharma20/sharingan.svg?branch=master)](https://travis-ci.org/vipul-sharma20/sharingan)
[![Docker Automated build](https://img.shields.io/docker/automated/vipul20/sharingan.svg)]()

Sharingan is a tool built on Python 3.6 using OpenCV 3.2 to extract news
content as text from newspaper’s photo and perform news context extraction.

For more details and explanation, please refer the blog post here: [http://vipul.xyz/2017/03/sharingan-newspaper-text-and-context.html](http://www.vipul.xyz/2017/03/sharingan-newspaper-text-and-context.html)

How it works?
=============

News Extraction
---------------

<p align="center">
    <b>Capture Image</b>
</p>

![Alt](https://i.imgur.com/6DklnQt.jpg)

<p align="center">
    <b>Canny Edge Detection</b>
</p>

![Alt](https://i.imgur.com/voDsUEg.jpg)

<p align="center">
    <b>Dilation</b>
</p>

![Alt](https://i.imgur.com/zMq2vgH.jpg)

<p align="center">
    <b>Contour Detection</b>
</p>

![Alt](https://i.imgur.com/zbh5UAV.jpg)

<p align="center">
    <b>Contour Approximation and Bound Box</b>
</p>

![Alt](https://i.imgur.com/LSR98LW.jpg)

Manual Mode
-----------

![Alt](https://cdn-images-1.medium.com/max/1600/1*6KKm4wGknXonl54dUD6tjQ.gif "drag")

![Alt](https://cdn-images-1.medium.com/max/1600/1*_pOvzvVLvHvcgrpxQL9XeA.gif "thresh")

Context Extraction
------------------

The segmentation done above gives the following result after context extraction:

        [‘residential terraces’, ‘busy markets’, ‘Puppies’, ‘inhumane conditions’, ‘popular e-commerce sites’, ‘Sriramapuram’, ‘Russell Market’, ‘issue licences’,
        ‘meeting conditions’, ‘positive impact’, ‘pet owners’, ‘R. Shantha Kumar’, ‘welfare ofﬁcer’, ‘Animal Welfare Board’, ‘India’]
        [‘Kittie’]
        [‘Compassion Unlimited’]
        [‘public spaces’, ‘Animal’, ‘rights activists’, ‘civic body’, ‘Bengaluru’],
        [‘BENGALURU’, ‘Bruhat Bengaluru Mahanagar Palike’, ‘Dane’, ‘English Mastiff’, ‘Bulldog’, ‘Boxer’, ‘Rottweiler’, ‘Bernard’, ‘Shepherd’, ‘Retriever’,
        ‘draft guidelines’, ‘sterilisation’, ‘pet dogs ’, ‘Owners’]


Installation
============

Installing OpenCV 3.2 from source Python 3.6
--------------------------------------------

* `wget https://github.com/Itseez/opencv/archive/3.2.0.zip`
* `unzip 3.2.0.zip`
* `cd opencv-3.2.0`
* `mkdir release && cd release`

        cmake -DBUILD_TIFF=ON \
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

* You will be similar to this: [output](https://gist.github.com/vipul-sharma20/d57a779619f22b2254b66c89c957faf2)
* `make -j4`
* make install

Setting up Sharingan
--------------------

* `git clone git@github.com:vipul-sharma20/sharingan.git`
* `pip install -r requirements.txt`

**IMPORTANT:** You will require some corpora and trained models
for the code to run. You can refer to: [http://www.nltk.org/data.html](http://www.nltk.org/data.html)

* Interactive Method:

        In [1]: import nltk

        In [2]: nltk.download()

Docker
======

Try out the code on Jupyter Notebook

* `docker build -t sharingan-docker .`
* `docker run -p 8888:8888 -it sharingan-docker`

Thanks to
=========

I am no wizard. Big thanks to people who came up with these solutions and posts:

* [https://erget.wordpress.com/](https://erget.wordpress.com/2014/03/13/building-an-interactive-gui-with-opencv/)
* [https://www.scivision.co/](https://www.scivision.co/anaconda-python-opencv3/)
* [https://enumap.wordpress.com/](https://enumap.wordpress.com/2012/11/23/python-opencv-resize-image/)
* [http://stackoverflow.com/questions/15341538/](http://stackoverflow.com/questions/15341538/numpy-opencv-2-how-do-i-crop-non-rectangular-region)
* [http://stackoverflow.com/questions/30310430/](http://stackoverflow.com/questions/30310430/opencv-draw-a-rectangle-in-a-picture-were-never-shown)
* [http://www.pyimagesearch.com/](http://www.pyimagesearch.com/2015/02/09/removing-contours-image-using-python-opencv/)
* [http://to.predict.ch/](http://to.predict.ch/hacking/2017/02/12/opencv-with-docker.html)

The Name?
=========

See here: [Sharingan](naruto.wikia.com/wiki/Sharingan)

LICENSE
=======

This project is licensed under MIT License:

Copyright (c) 2017-2018: Vipul Sharma

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

This project uses following external libraries, which have their own licenses:

* NLTK (https://github.com/nltk/nltk/blob/develop/LICENSE.txt) [Apache]
* OpenCV (https://github.com/opencv/opencv/blob/master/LICENSE) [BSD]
* NumPy (https://github.com/numpy/numpy/blob/master/LICENSE.txt)

