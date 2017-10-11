<!--
Maintainer:   jeffskinnerbox@yahoo.com / www.jeffskinnerbox.me
Version:      0.4.0
-->



# Performance and Speed Testing
* To measure performance of threading, use `mpstat -P ALL 1`.
* To measure the Internet speed, use https://fast.com/ or http://www.speedtest.net/
* See https://github.com/sivel/speedtest-cli
* at home using desktop, I'm getting 1ms to 10ms pings, 855Mbps upload, 847Mbps download
* at home using BlueRpi, I'm getting


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



