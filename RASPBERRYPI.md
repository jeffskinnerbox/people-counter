
# Embedded Learning Library (ELL)
The Microsoft's [Embedded Learning Library (ELL)][03]
claims to help in the design and deployment of intelligent machine-learned models
onto resource constrained platforms and small single-board computers,
like Raspberry Pi, Arduino, and micro:bit.

[ELL Tutorials](https://microsoft.github.io/ELL/tutorials/)

# ???
OpenCV can be computationally very intensive, pushing the Raspberry Pi very hard,
and Raspberry Pi 3 tends to overheat when pushed to its limits.
The RPi's processor must protect itself from high temperatures,
so when the processor’s internal temperature approaches 85 degrees Celsius,
it protects itself by disables overclocking,
reverting to minimal speeds/freq and voltages,
or in some cases shutting down completely.

So the performance of the OpenCV algorithm may be impacted by the heat of the RPi processor.
To combat this, it could be beneficial to provide active cooling.
Microsoft blog, "[Active cooling your Raspberry Pi 3][01]",
provides some data on how effective adding a fan can be.
(NOTE: You can fine the Raspberry Pi 3 Fan Mount [STL file][07] [here][02],
and have it 3D printed at [shapeways][06] or other sites.
To view the STL file, you can use [this site][05].)


# Reading Processor Tempature and Clock Speed

config.txt - Overclocking options - https://www.raspberrypi.org/documentation/configuration/config-txt/overclocking.md



[01]:https://microsoft.github.io/ELL/tutorials/Active-cooling-your-Raspberry-Pi-3/
[02]:https://microsoft.github.io/ELL/gallery/Raspberry-Pi-3-Fan-Mount/
[03]:https://microsoft.github.io/ELL/
[05]:https://www.viewstl.com/
[06]:https://www.shapeways.com/
[07]:https://en.wikipedia.org/wiki/STL_(file_format)
[08]:
[09]:
[10]:
