<!--
Maintainer:   jeffskinnerbox@yahoo.com / www.jeffskinnerbox.me
Version:      0.3.0
-->

* To measure performance of threading, use `mpstat -P ALL 1`.
* To measure the Internet speed, use https://fast.com/

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

# Streaming Latency
The streaming latency has little to do with the encoding by the Pi,
but mostly to do with the playing or receiving end.
If the Pi weren’t capable of encoding a frame before the next frame arrived,
it wouldn’t be capable of recording video at all
since it buffers would rapidly become filled and stall.

Players typically introduce several seconds worth of latency.
The primary reason is that most players (e.g. VLC)
are optimized for playing streams over a network.
Such players allocate a large (multi-second) buffer
and only start playing once this is filled to guard against possible future packet loss.

For additional information, see the following:

* [Why is there so much latency when streaming video?](http://picamera.readthedocs.io/en/release-1.10/faq.html#why-is-there-so-much-latency-when-streaming-video)



