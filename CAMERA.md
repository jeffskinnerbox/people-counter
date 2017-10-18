<!--
Maintainer:   jeffskinnerbox@yahoo.com / www.jeffskinnerbox.me
Version:      0.4.0
-->


The topic of computer vision and cameras is deep and complex.
It involves a range of technologies from photography,
lens, the physics of light, and how the brain + eye process color.
Raspberry Pi Camera Module is from the Raspberry Pi Foundation
is the most popular but many others exist,
making this topic even harder to fully understand.

The original [5-megapixel model was released in 2013][01],
and an [8-megapixel Camera Module v2 was released in 2016][02].
For both iterations, there are visible light and infrared versions.


* explain all of this!! - https://www.raspberrypi.org/documentation/hardware/camera/
* [Vision Campus](https://www.youtube.com/playlist?list=PLULhsSsX_9ge4g9maUkFGGLaG5S8_CiAC)

#  Camera Hardware
https://picamera.readthedocs.io/en/release-1.13/fov.html

# Tools
The Pi Camera drivers are proprietary, and in a sense,
that they do not follow any standard APIs.
That means that applications have to be written specifically for the Raspberry Pi camera.
Under Linux, the standard API for cameras (including web cams) is V4L (Video for Linux), and a number of applications have been written that support any camera with a V4L driver. An independent developer has now written a user space V4L driver for the Raspberry Pi camera, which is available from here3. With that driver, you can use generic Linux applications written for cameras. The driver has a few limitations: it is closed sourced, and can be a little slow because it runs as a user program rather than a kernel driver. The program worked reasonably well when I tested it and it is expected to continue to improve.

If you hook your camera up to a Linux box,
you can use `v4l2-ctld` to list the supported video formats.
The [`v4l2-ctl` tool][05] is used to control [video4linux][04] devices,
either video, vbi, radio or swradio, both input and output.
This tool uses the [USB video device class (UVC)][03] to query the info from the camera.
UVC is typically supported by recent webcams.

```bash
# install the v4l control tool
sudo apt install v4l-utils

# show the resolutions supported fo the MJPG pixel format
$ v4l2-ctl --device /dev/video0 --list-framesizes=MJPG
ioctl: VIDIOC_ENUM_FRAMESIZES
	Size: Discrete 160x120
	Size: Discrete 176x144
	Size: Discrete 320x240
	Size: Discrete 352x288
	Size: Discrete 640x480
	Size: Discrete 800x600
	Size: Discrete 960x720

# show all the supported rsolutions
v4l2-ctl --device /dev/video0 --list-formats-ext
```
* https://www.raspberrypi.org/forums/viewtopic.php?t=62364
* https://www.raspberrypi.org/documentation/usage/camera/raspicam/README.md
* http://www.home-automation-community.com/surveillance-with-raspberry-pi-noir-camera-howto/
* [How to use V4L2 Cameras on the Raspberry Pi 3 with an Upstream Kernel](https://blogs.s-osg.org/use-v4l2-cameras-raspberry-pi-3-upstream-kernel/)

# API - picamera Package
http://picamera.readthedocs.io/en/release-1.10/install3.html

http://picamera.readthedocs.io/en/release-1.10/api.html

# Recording to a network stream
http://picamera.readthedocs.io/en/release-1.10/recipes1.html#recording-to-a-network-stream

# Latency
[Understanding Video Latency: What is video latency and why do we care about it?](http://www.vision-systems.com/content/dam/VSD/solutionsinvision/Resources/Sensoray_video-latency_article_FINAL.pdf)



[01]:https://www.raspberrypi.org/blog/camera-board-available-for-sale/
[02]:https://www.raspberrypi.org/blog/new-8-megapixel-camera-board-sale-25/
[03]:https://en.wikipedia.org/wiki/USB_video_device_class
[04]:https://en.wikipedia.org/wiki/Video4Linux
[05]:http://trac.gateworks.com/wiki/linux/v4l2
[06]:
[07]:
[08]:
[09]:
[10]:
