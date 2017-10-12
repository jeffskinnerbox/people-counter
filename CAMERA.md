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


explain all of this!! - https://www.raspberrypi.org/documentation/hardware/camera/

# Tools
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

# API - picamera Package
http://picamera.readthedocs.io/en/release-1.10/install3.html

http://picamera.readthedocs.io/en/release-1.10/api.html

# Recording to a network stream
http://picamera.readthedocs.io/en/release-1.10/recipes1.html#recording-to-a-network-stream



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
