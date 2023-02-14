<!--
Maintainer:   jeffskinnerbox@yahoo.com / www.jeffskinnerbox.me
Version:      0.4.0
-->


<div align="center">
<img src="https://python-deprecated.readthedocs.io/en/latest/_images/logo-full.png" title="Deprecated is increasingly used as a technical term meaning 'to recommend against using something on the grounds that it is obsolete', or 'to declare some technological feature or function to be obsolescent'.  The earliest meaning of deprecate was 'to pray against, as an evil,' and soon after this first meaning it took on the additional sense 'to express disapproval of.' Meanwhile, depreciate, the closely related word with which it is often confused, means 'to lower in value.'" align="center">
</div>


----


# Freeboard
* Freeboard dashboard - https://freeboard.thingspace.io/board/Yx8HGW

# My Jupyter Notebooks
My expanding set of Jupyter Notebooks.

Pull text from `/home/jeff/blogging/content/ideas/`.


What if you Jupyter environment isn't on your local computer,
but instead on a remote compute accessible via TCP/IP?
You want to open and manipulate an Jupyter Notebook running on the remote computer.
This can be done by opening an SSH tunnel.
This tunnel will forward the port used by the remotely running Jupyter Notebook server instance
to a port on your local machine,
where it can be accessed in a browser just like a locally running Jupyter Notebook instance.

On the remote machine, start the Jupyter Notebooks server:

```bash
# on the remote machine, start the jupyter notebooks server
jupyter notebook --no-browser --port=8889
```

On the local machine, start an SSH tunnel:

```bash
# on the local machine, start an SSH tunnel
# run in background: ssh -f -N -L localhost:8888:localhost:8889 remote_user@remote_host
# run in foreground: ssh -N -L localhost:8888:localhost:8889 remote_user@remote_host
ssh -N pi@BlueRPi -L localhost:8888:localhost:8889
```

Now enter `localhost:8888` in your favorite browser to use the remote Jupyter Notebook!

**Within Chromebook ....**

1. In one window, login to desktop -- cd Jupyter-Notebooks ; jupyter notebook --no-browser --port=8889
2. In 2nd window -- ssh -N jeff@desktop -L localhost:8888:localhost:8889
3. In 3rd window -- gnome-www-browser
4. Now enter `localhost:8888` in the browser and now you can access the remote Jupyter Notebook!

# Sources

The people counting algorithm

* [People Counter 1 – Installing Python, OpenCV and trying it out](http://www.femb.com.mx/people-counter/people-counter-1-installing-python-opencv-and-trying-it-out/)
* [People Counter 2 – Opening a video stream](http://www.femb.com.mx/people-counter/people-counter-2-opening-a-video-stream/)
* [People Counter 3 – Drawing in the video window](http://www.femb.com.mx/people-counter/people-counter-3-drawing-in-the-video-window/)
* [People Counter 4 – Background Susbtraction](http://www.femb.com.mx/people-counter/people-counter-4-background-susbtraction/)
* [People Counter 5 – Morphological Transformations](http://www.femb.com.mx/people-counter/people-counter-5-morphological-transformations/)
* [People counter 6 – Find contours](http://www.femb.com.mx/people-counter/people-counter-6-find-contours/)
* [People counter 7 – Defining a person](http://www.femb.com.mx/people-counter/people-counter-7-defining-a-person/)
* [People counter 8 – Following movement](http://www.femb.com.mx/people-counter/people-counter-8-finding-movement/)
* [People Counter 9 – Counting](http://www.femb.com.mx/people-counter/people-counter-9-counting/)

Fast video processing

* [Faster video file FPS with cv2.VideoCapture and OpenCV](https://www.pyimagesearch.com/2017/02/06/faster-video-file-fps-with-cv2-videocapture-and-opencv)
* [Unifying picamera and cv2.VideoCapture into a single class with OpenCV](http://www.pyimagesearch.com/2016/01/04/unifying-picamera-and-cv2-videocapture-into-a-single-class-with-opencv/)
* [Increasing webcam FPS with Python and OpenCV](http://www.pyimagesearch.com/2015/12/21/increasing-webcam-fps-with-python-and-opencv/)
* [A series of OpenCV convenience functions](https://www.pyimagesearch.com/2015/02/02/just-open-sourced-personal-imutils-package-series-opencv-convenience-functions/)

Loading OpenCV

* [Optimizing OpenCV on the Raspberry Pi](https://www.pyimagesearch.com/2017/10/09/optimizing-opencv-on-the-raspberry-pi/)
* [Raspbian Stretch: Install OpenCV 3 + Python on your Raspberry Pi](https://www.pyimagesearch.com/2017/09/04/raspbian-stretch-install-opencv-3-python-on-your-raspberry-pi/)
