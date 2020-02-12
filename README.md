# Security_cam

Main file is under src folder -> camera-test.py

Security camera application that detects human faces and compares them to a list of known faces which triggers an email alert to the registered owners when an unknown face is detected. 

Detects faces using a Histogram of Oriented Gradients algorithm to find the part of the image that resembles a generic encoding of a face.

Utilizes a neural network trained to measure features of the face to generate the measurement of the detected faces and compare them to the measurement of the known faces measured in the past.

![Alt Text](https://github.com/gfmacaraeg/Security_cam/blob/master/footage_gif.gif)

