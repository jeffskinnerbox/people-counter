<!--
Maintainer:   jeffskinnerbox@yahoo.com / www.jeffskinnerbox.me
Version:      0.4.1
-->

# People Counting Build Process
This document provides step-by-step procedures to build the people-counter
software application.
There is also a list of hardware compoents.
The hardware build should can be done by following the instructions
that come with the hardware when purchased.

Two version of this application have been built:

* BlueRpi - does **not** include the [Optimizing OpenCV on the Raspberry Pi](https://www.pyimagesearch.com/2017/10/09/optimizing-opencv-on-the-raspberry-pi/)
procedures and uses a ???Mb ??? PiCamera with software version 1.13
* YellowRpi - does include the [Optimizing OpenCV on the Raspberry Pi](https://www.pyimagesearch.com/2017/10/09/optimizing-opencv-on-the-raspberry-pi/)
procedures and uses a ???Mb ??? PiCamera with software version 1.13

**This is a work in progress**

* rpi-loader - https://github.com/jeffskinnerbox/rpi-loader
    * fix the scripts concern the use of sudo
    * write scripts for the loading of OpenCV, Jupyter, etc.
* OpenCV
    * include procedures from [Optimizing OpenCV on the Raspberry Pi](https://www.pyimagesearch.com/2017/10/09/optimizing-opencv-on-the-raspberry-pi/)
* Jupyter
* ts_dweepy - make sure to setup with setup.py, etc.
* people-counter - the MassMutual camera based people counter
* [Installing Keras with TensorFlow backend](https://www.pyimagesearch.com/2016/11/14/installing-keras-with-tensorflow-backend/)
* [Install dlib on the Raspberry Pi](https://www.pyimagesearch.com/2017/05/01/install-dlib-raspberry-pi/)


Videos, Pictures, Data -

A version of this document will be posted here - https://oneconfluence.verizon.com/display/TF2017/2017/10/10/HowTo%3A+Set-up+Jupyter+and+OpenCV

################################################################################

-----
## Bill of Materials
The materials required to build the hardware environment is as follows:

| Name      | Description                                                       | Price | Source            |
|:---------:|:-----------------------------------------------------------------:|:-----:|:-----------------:|
| Processor | Raspberry PI 3 Model B 1.2GHz 64-bit quad-core ARMv8 CPU, 1GB RAM | $35   | [Amazon](https://www.amazon.com/Raspberry-Model-1-2GHz-64-bit-quad-core/dp/B01CD5VC92/) |
| SD Card | Sandisk Ultra MICROSDHC 32GB 80MB/S Flash Memory Card | $17 | [Amazon](https://www.amazon.com/gp/product/B0148S2WUU) |
| Camera Clamp Mount | i.Trek ME-DC1+ME-CLP 12-Inch Clamp Mount for Compact Digital Camera | $19 | [Amazon](https://www.amazon.com/gp/product/B008OLGKLU) |
| Camera | Raspberry Pi Camera Module V2 - 8 Megapixel,1080p | $27 | [Amazon](https://www.amazon.com/gp/product/B01ER2SKFS) |
| Camera Case | Raspberry Pi Camera Case for V2 8 Megapixel | $10 | [Amazon](https://www.amazon.com/gp/product/B00IJZJKK4) |
| Power SUpply | CanaKit 5V 2.5A Raspberry Pi 3 Power Supply / Adapter / Charger | $10 | [Amazon](https://www.amazon.com/CanaKit-Raspberry-Supply-Adapter-Charger/dp/B00MARDJZ4) |
| WiFi Dongle | Edimax EW-7811Un 150Mbps 11n Wi-Fi USB Adapter | $8 | [Amazon](https://www.amazon.com/gp/product/B003MTTJOY) |
| Mobile Hot Spot | Jetpack 4G LTE Mobile Hotspot—AC791L | $100 | [Verizon](https://www.verizonwireless.com/internet-devices/verizon-jetpack-4g-lte-mobile-hotspot-ac791l/) |
| Case    | Aluminum case, Customize for Raspberry Pi 3/ Raspberry Pi 2 / Raspberry Pi B+ | $15 | [Amazon](https://www.amazon.com/gp/product/B0722L338Q) |
| Case    | Night Vision PIR Camer Box Bundle B+/2/3 | $20 | [MODMYPI](https://www.modmypi.com/raspberry-pi/cases-183/raspberry-pi-b-plus2-and-3-cases-1122/modmypi-pir-night-vision-camera-box-bundle-b-plus23) |


################################################################################

-----
## Building the OS Environment - DONE
I have written a detailed [step-by-step guide][03]
(you'll also find it [here][04])
on how to set up your Raspberry Pi as a "headless" computer.
This includes configuring the RPi for my local network, updating firmware,
loading all my favorite development tools and utilities.
This guide has been of great value to me to help repeatedly and consistently establish my devices.
But the work is all manual requiring dozens of command line entries.
This utility takes the drudgery out of setting up a new Raspberry Pi by automating this manual tasks.

Clearly, not all everything can be scripted.
You still have to download the latest version of Raspbian,
burn it to a SD Card, and things like that.
My objective is to ultimate create some utilities that will make this easier,
but that will wait until another version of this script.

Some of the ideas for this script were taken from the following:
"[Scripts to update the Raspberry Pi and Debian-based Linux Distros][05]".

### Step 0: Use 32G SD-Card or Larger
The tools you are about to install take up a great deal of space,
and since this is for video applications,
anything you record will consume siginificant disk space.
The OpenCV and the OpenCV Contribution packages alone are very large (430M + 120M).

A standard Raspberry Pi install will likely use over 4GB of the available space,
and then you add your personal tools and more space is used up.
I have found that attempting to load OpenCV and the OpenCV Contribution package
will require 10GB of disk space.
If your considering using Jupyter and some of the popular Python libraries,
your looking at 11 to 12GB of SD-Card storage being consumed.
My advice is to consider using a 32G SD-Card.

### Step 1: Download Raspberry Pi Image - DONE
Before you can load a copy of the latest Raspberry Pi image onto your micro SD Card,
you must first download the official Raspberry Pi operating system, [Raspbian][12]
(in my case, the version is [Stretch][11]).
You can get that download [here][13].

The Raspbian download site also lists a check sum for the download file.
(In my case, I down loaded the Raspbian file to `/home/jeff/Downloads/`.)
Check whether the file has been changed from its original state
by checking its digital signature (SHA1 hash value).

```bash
# validate file is uncorrupted via check of digital signature
$ sha1sum /home/jeff/Downloads/2017-08-16-raspbian-stretch.zip
da329713833e0785ffd94796304b7348803381db  /home/jeff/Downloads/2017-08-16-raspbian-stretch.zip
```

>**NOTE:** Latest versons of Raspian may be using SHA-256,
so replace `sha1sum` with `sha256sum` in the above command.

Next you need to unzip the file to retrieve the Linux image file:

```bash
$ unzip 2017-08-16-raspbian-stretch.zip
Archive:  2017-08-16-raspbian-stretch.zip
  inflating: 2017-08-16-raspbian-stretch.img
```

### Step 2: Write Raspberry Pi Image to SD Card - DONE
Next using Linux, you have copied the Raspbian image onto the SD card mounted to your system.
I'll be using the [Rocketek 11-in-1 4 Slots USB 3.0 Memory Card Reader][14] to create my SD Card.
Make sure to [choose a reputable SD Card][15] from [here][13], don't go cheap.

When using your card reader,
you'll need to know the device name of the reader.
The easiest way to find this is just unplug your card reader from the USB port,
run `df -h`, then plug it back in, and run `df -h` again.

```bash
# with the SD card reader unplugged
$ df -h
Filesystem      Size  Used Avail Use% Mounted on
udev            3.9G   12K  3.9G   1% /dev
tmpfs           783M  1.7M  781M   1% /run
/dev/sda3       110G   14G   90G  14% /
none            4.0K     0  4.0K   0% /sys/fs/cgroup
none            5.0M     0  5.0M   0% /run/lock
none            3.9G   90M  3.8G   3% /run/shm
none            100M   80K  100M   1% /run/user
/dev/sda1       461M  132M  306M  31% /boot
/dev/md0        917G  224G  647G  26% /home
/dev/sdb        3.6T  2.5T  950G  73% /mnt/backup

# with the SD card reader plugged in USB
$ df -h
Filesystem      Size  Used Avail Use% Mounted on
udev            3.9G   12K  3.9G   1% /dev
tmpfs           783M  1.8M  781M   1% /run
/dev/sda3       110G   14G   90G  14% /
none            4.0K     0  4.0K   0% /sys/fs/cgroup
none            5.0M     0  5.0M   0% /run/lock
none            3.9G   90M  3.8G   3% /run/shm
none            100M   80K  100M   1% /run/user
/dev/sda1       461M  132M  306M  31% /boot
/dev/md0        917G  224G  647G  26% /home
/dev/sdb        3.6T  2.5T  950G  73% /mnt/backup
/dev/sdj1        15G   32K   15G   1% /media/jeff/3CB1-D9D9
```

Note that in my example above, the new device is `/dev/sdj1`.
The last part (the number 1) is the partition number
but we want to write to the whole SD card, not just one partition.
Therefore you need to remove that part when creating the image.
With this information, and know the location of the Raspbian image and
where we need to write the Raspbian image to the SD Card
(see more detail instructions [here][16]).

```bash
# go to directory with the RPi image
cd /home/jeff/Downloads/Raspbian

# unmount the sd card reader
sudo umount /dev/sdj1

# write the image to the sd card reader
sudo dd bs=4M if=2017-08-16-raspbian-stretch.img of=/dev/sdj

# ensure the write cache is flushed
sudo sync

# check the integrity of the sd card image
sudo dd bs=4M if=/dev/sdj of=copy-from-sd-card.img
sudo truncate --reference 2017-08-16-raspbian-stretch.img copy-from-sd-card.img
diff -s 2017-08-16-raspbian-stretch.img copy-from-sd-card.img

# unmount the sd card reader
sudo umount /dev/sdj
```

Don’t remove SD card from the reader on your computer.
We’re going to set up the WiFi interface next.

>**NOTE:** You could immediately put the SD Card in the RPi and boot it up,
but you will have no WiFi access and you'll need to use the Ethernet interface,
or if there is no Ethernet interface,
you'll need to use a console cable to make the file modification
outline in the next step.
[Adafruit has good description on how to use a console cable]17]
and the how to [enable the UART for the console][18].

### Step 3: Install rpi-loader Script - DONE
To minimize the amount of keyboard entry and eliminate "fat finger" errors,
we use several Bash Shell scripts for building the Raspberry Pi
operating environment, required software packages,
and the people counting application.
Those scripts need to be downloaded and install on both a local
Linux machine, which I'll call `desktop`, and the Raspberry Pi.

The first install is on `desktop` as follows:

```bash
# change direct to where the rpi-loader will be installed
cd ~/src

# clone the rpi-loader software
git clone https://github.com/jeffskinnerbox/rpi-loader.git
```

Now you must do the final set of the install by running the `install.sh` script.
Run it and just answer the questions when prompted.

```bash
# enter the rpi-loader directory
cd rpi-loader

# complete the install
./install.sh
```

### Step 4: Run the part-1.sh Script - DONE
We now execute the first and only script to run on the local system
(aka `desktop`) while the against the SD Card.
This sets up the hostname and networking features for the Raspberry Pi.

```bash
# update the sd-card with networking information
sudo ~/src/rpi-loader/part-1.sh
```

This completes the operations that will be performed on the SD-Card
while on `desktop`.
Next will place the SD-Card in the Raspberry Pi
and complete all the remaining loading from there.

### Step 5: Start Up the Raspberry Pi - DONE
Place the SD-Card into the Raspberry Pi, power it up,
and login via ssh via WiFi or via Ethernet.
The hostname will be what you provided during the running of the `part-1.sh` script.
You will login as the `pi` user and password will be `raspberry`.

### Step 6: Clone the rpi-loader Tool - DONE
The `rpi-loader` will be heavely used on the Raspberry Pi for installing software,
but you now need to install it first.

```bash
# change direct to where the rpi-loader will be installed
cd ~
mkdir src
cd src

# clone the rpi-loader software
git clone https://github.com/jeffskinnerbox/rpi-loader.git
```

Now you must do the final set of the install by running the `install.sh` script.
Run it and just answer the questions when prompted.

```bash
# enter the rpi-loader directory
cd rpi-loader

# complete the install
./install.sh
```

### Step 7: Run the part-2.sh Script - DONE
Now your going to run `raspi-config` as a non-interactive command line tool
setting multiple low level options on the Raspberry Pi.

```bash
# run raspi-config tool and ste the time zone
sudo ~/src/rpi-loader/part-2.sh

# reboot the raspberry pi
sudo shutdown -r now
```

>**NOTE:** This script runs `raspi-config` as a non-interactive command line tool.
See "[Instructions of command-line in Raspi-config][01]"
and you notice that the command takes the form
`sudo raspi-config nonint <option> [<parameter>]`.
Key to understanding how to use this command are the `#define`
statments found within "[How could one automate the raspbian raspi-config setup?][02]".
**This capabilitiy is not documented, and as such,
could change without notice.**

### Step 8: Run the part-3.sh Script - DONE
Now we will update the Linux package list and the currently installed packages.

```bash
# update currently install linux packages
sudo ~/src/rpi-loader/part-3.sh

# if packages were installed, reboot the raspberry pi
sudo shutdown -r now
```

### Step 9: Run the part-4.sh Script - DONE
Now we'll update the Raspberry Pi firmware.

```bash
# update raspberry pi firmware
sudo ~/src/rpi-loader/part-4.sh

# if if new firmware was installed, reboot the raspberry pi
sudo shutdown -r now
```

### Step 10: Run the part-5.sh Script - DONE
Now we'll install multiple Linux packages that will likely see the greatest use.

```bash
# load linux packages
sudo ~/src/rpi-loader/part-5.sh
```

### Step 11: Run the part-5A.sh Script - DONE
Install your personal tools for your Linux environment.

>**NOTE:** We are not using `sudo` to run this script.
The tools your installing here should be owned by `pi` and not `root`.

```bash
# install your tools
~/src/rpi-loader/part-5A.sh

# copy scripts for python virual env
sudo cp ~/.bash/virtualenvwrapper.sh ~/.bash/virtualenvwrapper_lazy.sh /usr/local/bin

# make your bash tools active now
source ~/.bashrc
```

This completes the building of the Raspberry Pi's foundational operating environment.
We can now layer on additional tools for our applications.

################################################################################

-----
## Building the OpenCV Environment - DONE
This solution requires [OpenCV][33] to be used with the Raspberry Pi Camera.
First of all, hopefully its one of the [RPi Board Cameras][44].
While you could use a cheaper [USB-Webcam on the RPi][38],
you'll get none of the benefits of the Raspberry Pi's native GPU or [Graphics Processing Unit][45].

My major source of inspiration for the steps below are from:
"[Optimizing OpenCV on the Raspberry Pi][06]".

### Step 1: Install OpenCV Dependencies - DONE
The first thing we should do is update and upgrade any existing packages,
followed by updating the Raspberry Pi firmware.

```bash
# update the raspberry pi platform
sudo apt-get update && sudo apt-get upgrade
sudo rpi-update

# if the firmware is updated, you need to reboot
sudo shutdown -r now
```

Now let install OpenCV dependency packages.

```bash
# install opencv dependency packages
sudo ~/src/rpi-loader/part-6.sh
```

### Step 4: Install and Compile OpenCV Source Code - DONE
We are now ready to compile and install OpenCV.
We will grab the [latest version of OpenCV][41] from GitHub and install it.
Make sure your `opencv` and `opencv_contrib` versions match up,
otherwise you will run into errors during compilation.

The script used below contains `make` [recommended flags][06]
intended to optimize the performance of OpenCV on the Raspberry Pi.
Specifically, flags to make us of Arm CPU features [NEON][07] and [VFPV3][08].
There is an expected 30% to 45% boost in performance.

>**NOTE:** We are not using `sudo` to run this script.
The tools your installing here should be owned by `pi` and not `root`.

```bash
# install and compile opencv source code
~/src/rpi-loader/part-7.sh
```

This script will run an exceptionally long time;
as long as four hours.
(This could run faster if you increase the swap space
and use `make -j` but this does have draw backs.
Read more about this [here][06].)

Next we'll move the OpenCV libraries and executables to their proper location.

```bash
# enter directory where opencv was built
cd ~/src/opencv-3.3.0/build/

# install opencv executables and libraries
sudo make install

# creates the necessary links and cache to the most recent shared libraries
sudo ldconfig
```

Provided the above steps finished without error,
OpenCV should now be installed in `/usr/local/lib/python3.5/site-pacakges`
or `/usr/local/lib/python3.5/dist-packages/`.
You should verify this:

```bash
# verify the opencv install
$ ls -l /usr/local/lib/python3.5/dist-packages/
total 3876
-rw-r--r-- 1 root staff 3968464 Sep  5 17:11 cv2.cpython-35m-arm-linux-gnueabihf.so
```

For some reason (bug in the CMake script?),
the OpenCV 3 file for Python 3+ binding has the extention `.so`
and named `cv2.cpython-35m-arm-linux-gnueabihf.so` (or some variant of)
rather than simply `cv2.so` like  it should.
This needs to be fixed:

```bash
# enter the target directory
cd /usr/local/lib/python3.5/dist-packages/

# rename the file
sudo mv cv2.cpython-35m-arm-linux-gnueabihf.so cv2.so
```

### Step 5: Test OpenCV 3 Install - DONE
To validate the install of OpenCV and its binding with Python3,
open up a new terminal, execute the `source` and `workon` commands,
and then attempt to import the Python + OpenCV bindings:

```bash
[cv_env] $ ~/src/cv_env $ python3
Python 3.5.3 (default, Jan 19 2017, 14:11:04)
[GCC 6.3.0 20170124] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import cv2
>>> cv2.__version__
'3.3.0'
>>>
```

Appears that OpenCV 3.3.0 has been successfully installed
on Raspberry Pi 3 + Python 3.5 environment.

Once your absolutely sure OpenCV has been successfully installed,
you can remove both the `~/src/opencv-3.3.0` and `~/src/opencv_contrib-3.3.0`
directories to free up a bunch of space on your disk.

## Step 6: Test the Camera and Install Required Python Module - DONE
Before we go any further,
we need to make sure the camera on the Raspberry Pi works.
The install instructions for the camera can bout found [here][47].
To test out the camera, just use some of the simple tools
that come with the RPi:

```bash
# test the raspberry pi camer to make sure it works
raspistill -o ~/tmp/output.jpg

# view the image captured
display ~/tmp/output.jpg
```

With the last command, you should see a picture displayed.

So we know now the Raspberry Pi camera is working properly,
but how do we interface with the Raspberry Pi camera module using Python?
To do this, we'll use [Python's picamera][48].
To do the install,
and execute the following commands:

```bash
# install picamera modual with the array sub-module
# (this may run long as python creates wheels for all packages)
pip3 install "picamera[array]"
```
The standard picamera module provides methods to interface with the camera,
but we need the array sub-module so that we can utilize OpenCV.
With our Python bindings,
OpenCV represents images as [NumPy][49] arrays
and the array sub-module enables this.

To test if the Python `picamera` module is up and working with OpenCV,
run place the code below in the file `~/tmp/test_image.py`
and execute it with `python3 ~/tmp/test_image.py`:

```python
# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
rawCapture = PiRGBArray(camera)

# allow the camera to warmup
time.sleep(0.5)

# grab an image from the camera
camera.capture(rawCapture, format="bgr")
image = rawCapture.array

# display the image on screen and wait for a keypress to kill this process
cv2.imshow("Image", image)
cv2.waitKey(0)
```

You can also test the video capabilities via the script below
(execute with `python3 ~/tmp/test_video.py`):

```python
# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))

# allow the camera to warmup
time.sleep(0.5)

# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
	# grab the raw NumPy array representing the image, then initialize the timestamp
	# and occupied/unoccupied text
	image = frame.array

	# show the frame
	cv2.imshow("Frame", image)
	key = cv2.waitKey(1) & 0xFF

	# clear the stream in preparation for the next frame
	rawCapture.truncate(0)

	# if the `q` key was pressed, break from the loop
	if key == ord("q"):
		break
```

### Step 7: Uploading Test Data
OpenCV is all about processing visual images,
so your going to need test data,
potential a great deal of it, in the form of pictures and videos.
Some sources to consider are:

* Search Google for images or videos to download
* You can use the utility [`youtube-dl`][46] (may want to use the `-k` option)
to download videos from Youtube, or from nearly any website.
* [USC-SIPI image database](http://sipi.usc.edu/database/)

You can use SSH to move data from your local desktop to the Raspberry Pi.
I did this with the following commands:

```bash
# make directory for data to be uploaded (Videos and Pictures directory should already exist)
cd ~
mkdir Data

# to copy a file from your local computer to the raspberry pi, you use the following
# scp <file> <username>@<IP address or hostname>:<Destination>

# load images, video and data to the raspberry pi
scp ~/Pictures/* pi@BlueRPi:~/Pictures
scp ~/Videos/* pi@BlueRPi:~/Videos
scp ~/Data/* pi@BlueRPi:~/Data
```
################################################################################

-----
## Building the People-Counter Application
Now its time to install the People-Counter applicatiion.

Dweepy is a simple Python library for [dweet.io][23]
and modeled after the [BugLabs Javascript library][21].
The developers of Dweepy claim they have fully test it
and aims to have 100% coverage of the dweet.io API.

What we'll install here is the equivalent of Dweepy but supporting
[Verizon's ThingSpace version of dweet][22] instead of [Bub Labs dweet.io][20].
Effectively, the Dweepy library was modified to no longer point to `https://dweet.io`
and instead point to `https://thingspace.io`.

### Step 1: Install TS_Dweepy Code - DONE
The software for [`ts_dweepy` is on GitHub][09]
and this downloads it, builds the Python libarary,
installs it , and cleans up afer itslef.

>**NOTE:** We are not using `sudo` to run this script.
The tools your installing here should be owned by `pi` and not `root`.

```bash
# install ts_dweepy
~/src/rpi-loader/part-8.py
```

### Step 2: Install People-Counter

```bash
# enter directory where people-counter will be stored
cd ~/src

# install people-counter
git clone https://github.com/jeffskinnerbox/people-counter.git
```

### Step 3: Test People-Counter

################################################################################


# Node Binding Using node-opencv
[node-opencv][42] is OpenCV's bindings for Node.js.


* https://github.com/drejkim/pyenv-opencv/blob/master/detection.py
* [node-opencv GitHub](https://github.com/peterbraden/node-opencv)
* [node-opencv documentation](http://peterbraden.github.io/node-opencv/)
* [Real-time face detection using OpenCV, Node.js, and WebSockets](http://drejkim.com/blog/2014/12/02/real-time-face-detection-using-opencv-nodejs-and-websockets/)
* [face-detection-node-opencv GitHub](https://github.com/drejkim/face-detection-node-opencv)

################################################################################

# Installing OpenCV and Jupyter on Ubuntu
I also want OpenCV on my Linux desktop which is running Ubuntu 17.04.
I used the installation procedure below, which was derived from
[this website](http://milq.github.io/install-opencv-ubuntu-debian/).


################################################################################

-----
## Building the Jupyter Notebook Environment
Pewrsonally, I want a interactive and feature rich environment for doing my OpenCV work,
and I found that in [Jupyter Notebook][55] does the trick.
Just like the OpenCV package, giving a proper introduction to Jupyter Notebook
could fill multiple books, web pages, news articles, and in fact does!
Jupyter is an evolution of [Interactive Python (IPython) and its notebook][56],
but now [language agnostic and much more][54]
If you want to get a sense of the power and versatility of Jupyter Notebook,
check out the links below:

* [A gallery of interesting Jupyter Notebooks](https://github.com/jupyter/jupyter/wiki/A-gallery-of-interesting-Jupyter-Notebooks)
* [Jupyter nbviewer](http://nbviewer.jupyter.org/)
* [IPython Notebook best practices for data science](https://www.youtube.com/watch?v=JI1HWUAyJHE)

If you wish to covert the Jupyter Notebooks to another format for publishing
(ex. HTML, PDF, Markdown, and more),
they can be created by using the [nbconvert][52] utility.
Another nice fact is that Jupyter Notebook files
(i.e. `*.ipynb`) will render automatically on GitHub/Gist ([example][53])
giving you a public way to share or .

### Step 1: Install Jupyter and Supporting Packages
Installing Jupyter Notebook on your computer is documented [here][50].
For new users, they highly recommend installing it via [Anaconda][51],
but I used the following procedure:

```bash
# update your pip utility
pip3 install --upgrade pip

# install jupyter
sudo pip3 install jupyter

# install some of the commonly used python packages
sudo pip3 install matplotlib seaborn pandas imutils
sudo pip3 install scipy scikit-learn              # scikit-learn didn't build for some reason
```

### Step 2: Test Jupyter
Your ready now to start the Jupyter Notebook.
This can be done via several ways.
The easiest is to just enter `jupyter notebook`
in a terminal window on the Raspberry Pi
and the default browser on teh Rasperry Pi will open with jupyter (`http://localhost:8888`).
I prefer to put the burden of running the browser on my local computer.
You can do this via running Jupyter as a server.

With this, you Jupyter environment isn't on your local computer,
but instead on a remote compute (Raspberry Pi) accessible over TCP/IP.
You want to open and manipulate an Jupyter Notebook running on the remote computer.
This can be done by opening an SSH tunnel.
This tunnel will forward the port used by the remotely running Jupyter Notebook server instance
to a port on your local machine,
where it can be accessed in a browser just like a locally running Jupyter Notebook instance.

On the remote machine, start the Jupyter Notebooks server:

```bash
# on the pberry pi (emote machine), start the jupyter notebooks server
jupyter notebook --no-browser --port=8889
```

On the local machine, start an SSH tunnel:

```bash
# on you desktop linux (local machine), start an SSH tunnel
# run in background: ssh -f -N -L localhost:8888:localhost:8889 remote_user@remote_host
# run in foreground: ssh -N -L localhost:8888:localhost:8889 remote_user@remote_host
ssh -N pi@BlueRPi -L localhost:8888:localhost:8889
```

Now enter `localhost:8888` in your favorite browser on your desktop linux (local machine)
to use the Raspberry Pi (remote machine) Jupyter Notebook.
You should see Jupyter popup in your browser.

To test Jupyter, enter the code from the script created earlier, `~/tmp/test_video.py`.
You should get a popup window with the Raspberry Pi camera streaming live video.



* [Remote Access to IPython Notebooks via SSH](https://coderwall.com/p/ohk6cg/remote-access-to-ipython-notebooks-via-ssh)
* [Use Jupyter notebook remotely](http://amber-md.github.io/pytraj/latest/tutorials/remote_jupyter_notebook)
* [Running a notebook server](https://jupyter-notebook.readthedocs.io/en/stable/public_server.html)
* [Jupyter Notebook on remote server](https://coderwall.com/p/y1rwfw/jupyter-notebook-on-remote-server)

################################################################################
################################################################################

* [Install guide: Raspberry Pi 3 + Raspbian Jessie + OpenCV 3](http://www.pyimagesearch.com/2016/04/18/install-guide-raspberry-pi-3-raspbian-jessie-opencv-3/)
* [OpenCV and Pi Camera Board](https://thinkrpi.wordpress.com/2013/05/22/opencv-and-camera-board-csi/)
* [OpenFace - Free and open source face recognition with deep neural networks](https://cmusatyalab.github.io/openface/)
* [Face Detection Using OpenCV With Raspberry Pi](https://www.hackster.io/deligence-technologies/face-detection-using-opencv-with-raspberry-pi-93a8fe)
* [Face Recognition: Kairos vs Microsoft vs Google vs Amazon vs OpenCV](https://www.kairos.com/blog/face-recognition-kairos-vs-microsoft-vs-google-vs-amazon-vs-opencv)

* [How to Process Live Video Stream Using FFMPEG and OpenCV](http://blog.lemberg.co.uk/how-process-live-video-stream-using-ffmpeg-and-opencv)
* [OpenCV remote (web-based) stream processing](https://github.com/ECI-Robotics/opencv_remote_streaming_processing)
* [Raspberry Pi Camera openCV rendering with low latency streaming with gstreamer via RTP](http://hopkinsdev.blogspot.com/2016/06/raspberry-pi-camera-opencv-rendering.html)

################################################################################



# Other Things to Install
* [Installing Tflearn on Raspberry Pi 3](http://www.instructables.com/id/Installing-Tflearn-on-Raspberry-Pi-3/)
* [Installing Keras with TensorFlow backend](https://www.pyimagesearch.com/2016/11/14/installing-keras-with-tensorflow-backend/)
* [Install dlib on the Raspberry Pi](https://www.pyimagesearch.com/2017/05/01/install-dlib-raspberry-pi/)




[01]:https://www.52pi.com/blog/19-instructions-of-command-line-in-raspi-config
[02]:https://raspberrypi.stackexchange.com/questions/28907/how-could-one-automate-the-raspbian-raspi-config-setup
[03]:http://jeffskinnerbox.me/posts/2016/Apr/27/howto-set-up-the-raspberry-pi-as-a-headless-device/
[04]:https://oneconfluence.verizon.com/display/TF2017/2017/09/05/HowTo%3A+Set-up+the+Raspberry+Pi+as+a+Headless+Device
[05]:https://blog.robseder.com/2015/09/29/scripts-to-update-the-raspberry-pi-and-debian-based-linux-distros/
[06]:https://www.pyimagesearch.com/2017/10/09/optimizing-opencv-on-the-raspberry-pi/
[07]:https://developer.arm.com/technologies/neon
[08]:https://developer.arm.com/technologies/floating-point
[09]:https://github.com/jeffskinnerbox/ts_dweepy
[10]:
[11]:https://www.raspberrypi.org/blog/raspbian-stretch/
[12]:https://www.raspberrypi.org/downloads/raspbian/
[13]:https://www.raspbian.org/
[14]:http://www.amazon.com/gp/product/B00GVRHON2?psc=1&redirect=true&ref_=oh_aui_detailpage_o00_s01
[13]:http://www.jeffgeerling.com/blogs/jeff-geerling/raspberry-pi-microsd-card
[15]:http://www.wirelesshack.org/best-micro-sd-card-for-the-raspberry-pi-model-2.html
[16]:https://www.raspberrypi.org/documentation/installation/installing-images/linux.md
[17]:https://learn.adafruit.com/adafruits-raspberry-pi-lesson-5-using-a-console-cable/overview
[18]:https://cdn-learn.adafruit.com/downloads/pdf/adafruits-raspberry-pi-lesson-5-using-a-console-cable.pdf
[19]:
[20]:https://dweet.io
[21]:https://github.com/buglabs/dweetio-client
[22]:https://thingspace.verizon.com/develop/apis/dweet/v1/index.html
[23]:https://www.networkworld.com/article/3133738/internet-of-things/dweetio-a-simple-effective-messaging-service-for-the-internet-of-things.html
[24]:https://stackoverflow.com/questions/1471994/what-is-setup-py
[25]:https://docs.python.org/3/install/index.html
[26]:
[27]:
[28]:
[29]:
[30]:
[31]:
[32]:
[33]:http://opencv.org
[34]:http://www.boost.org/
[35]:http://zbar.sourceforge.net/
[36]:http://eigen.tuxfamily.org
[37]:https://buildroot.uclibc.org/
[38]:https://www.raspberrypi.org/documentation/usage/webcams/
[39]:https://en.wikipedia.org/wiki/VideoCore
[40]:http://elinux.org/Raspberry_Pi_VideoCore_APIs#Built-in_Sample_Programs
[41]:https://github.com/opencv/opencv
[42]:https://www.npmjs.com/package/opencv
[43]:http://www.pyimagesearch.com/2017/09/04/raspbian-stretch-install-opencv-3-python-on-your-raspberry-pi/
[44]:https://www.adafruit.com/product/3099
[45]:https://en.wikipedia.org/wiki/Graphics_processing_unit
[46]:https://rg3.github.io/youtube-dl/download.html
[47]:https://thepihut.com/blogs/raspberry-pi-tutorials/16021420-how-to-install-use-the-raspberry-pi-camera
[48]:http://picamera.readthedocs.io/en/release-1.9/index.html
[49]:http://www.numpy.org/
[50]:http://jupyter.org/install.html
[51]:https://www.anaconda.com/
[52]:https://nbconvert.readthedocs.io/en/latest/
[53]:https://github.com/barbagroup/AeroPython/blob/master/lessons/01_Lesson01_sourceSink.ipynb
[54]:https://www.quora.com/What-is-the-difference-between-Jupyter-and-IPython-Notebook
[55]:http://jupyter.org/
[56]:https://ipython.org/
[57]:https://www.pyimagesearch.com/2015/03/30/accessing-the-raspberry-pi-camera-with-opencv-and-python/
