# Social media for road transport model
 Exploit social media data for road transport model
 
 
# Data-and-Codes-for-Integrating-Computer-Vision-and-Traffic-Modelling

# 0. A demonstration video of the SM2II2VP approach 

![image](https://github.com/0AnonymousSite0/Data-and-Codes-for-Integrating-Computer-Vision-and-Traffic-Modelling/blob/master/2.%20Video%20clips%20and%20Screenshots/List%20of%20all%20materials%20in%20the%20GitHub.png)


# 1. Certain video clips during the study

## 1.1 Computer vision for perceiving real-time traffic conditions

![image](https://github.com/0AnonymousSite0/Data-and-Codes-for-Integrating-Computer-Vision-and-Traffic-Modelling/blob/master/2.%20Video%20clips%20and%20Screenshots/Video%20clips/Video%20Clip%20(1).gif)

![image](https://github.com/0AnonymousSite0/Data-and-Codes-for-Integrating-Computer-Vision-and-Traffic-Modelling/blob/master/2.%20Video%20clips%20and%20Screenshots/Video%20clips/Video%20Clip%20(2).gif)

![image](https://github.com/0AnonymousSite0/Data-and-Codes-for-Integrating-Computer-Vision-and-Traffic-Modelling/blob/master/2.%20Video%20clips%20and%20Screenshots/Video%20clips/Video%20Clip%20(3).gif) 

## 1.2 Traffic simulation for near-real-time optimization

![image](https://github.com/0AnonymousSite0/Data-and-Codes-for-Integrating-Computer-Vision-and-Traffic-Modelling/blob/master/2.%20Video%20clips%20and%20Screenshots/Video%20clips/Video-Clip-_Traffic-simulation_.gif) 

# 2 General Introduction

2.1 This repository aims at providing the codes and data regarding the paper entitled “Integrating Computer Vision and Traffic Simulation for Near-real-time Signal Timing Optimization of Multiple Intersections” for the public, and it is developed by The University of ****.

2.2 All codes are developed on Python 3.6, and the IDE adopted is PyCharm (Professional version). The codes also support the GPU computing for higher speed; the Navida CUDA we adopted is V10.0.130.

2.3 We greatly appreciate the selfless spirits of these voluntary contributors of a series of open python libraries, including 
OpenCV (https://opencv.org/), Tensorflow (https://github.com/tensorflow/models), Keras (https://github.com/keras-team/keras), Numpy (https://numpy.org/), labelImg (https://github.com/tzutalin/labelImg), pyExcelerator (https://github.com/WoLpH/pyExcelerator), some base works ( https://github.com/Cartucho/mAP, https://github.com/peter-moran/vehicle-detector, https://github.com/ckyrkou/CNN_Car_Detector, https://github.com/nicholaskajoh/ivy, and https://github.com/qqwweee/keras-yolo3), and so on. Our work stands on the shoulders of these giants.

2.4 Before submitting these codes to Github, all of them have been tested to be well-performed as shown in the screenshots below.

2.5 The Python environment clone based on Anaconda is provided in Google Drive (https://drive.google.com/drive/folders/1iqD30Gqp4zKBqnEm0Uup64xuQndZz6lT?usp=sharing). Even so, we are not able to guarantee their operation in other computing environments due to the differences in the python version, computer operating system, and adopted hardware.

2.6 As for anything regarding the copyright, please refer to the MIT License.


# 3. The specifications of developed codes


## 3.1 Codes for training an object detector with transfer learning


This is for doing transfer learning of ready-developed detector (i.e., Yolo v3 in this case study). The manually labelled images are attached in the "labelled images of local traffic for transfer learning" file. We use the open-source tool 
labelImg (https://github.com/tzutalin/labelImg) to manually label the images. Additionally, the training process supports GPU computing.

![image](https://github.com/0AnonymousSite0/Data-and-Codes-for-Integrating-Computer-Vision-and-Traffic-Modelling/blob/master/2.%20Video%20clips%20and%20Screenshots/Screenshots/The%20running%20code%20for%20the%20transfer%20learning%20of%20a%20vehicle%20detector%20(1).png)
Figure 1. The transfer learning program is loading the existing model and freezing certain layers (The warnings in red colours are caused by the version of TensorFlow, which do not influence the program running)

![image](https://github.com/0AnonymousSite0/Data-and-Codes-for-Integrating-Computer-Vision-and-Traffic-Modelling/blob/master/2.%20Video%20clips%20and%20Screenshots/Screenshots/The%20running%20code%20for%20the%20transfer%20learning%20of%20a%20vehicle%20detector%20(2).png)
Figure 2. The transfer learning program is training epoch by epoch


## 3.2 Codes for comparing tracking algorithms


It supports to do the examination of eight widely recognized tracking algorithms, including Boosting, MIL, KCF, TLD, MedianFlow, CSRT, MOSSE, GoTurn. Additionally, as the Caffe model of GoTurn exceeds 100M, it has also been uploaded to Google Drive (https://drive.google.com/drive/folders/1iqD30Gqp4zKBqnEm0Uup64xuQndZz6lT?usp=sharing). 

![image](https://github.com/0AnonymousSite0/Data-and-Codes-for-Integrating-Computer-Vision-and-Traffic-Modelling/blob/master/2.%20Video%20clips%20and%20Screenshots/Screenshots/The%20running%20program%20for%20examining%20and%20selecting%20different%20tracking%20algorithms.png)
Figure 3. The running program for examining and selecting different tracking algorithms (The colourful lines are the trajectories of each vehicle)


## 3.3 Codes for detecting and tracking vehicles


The detector is developed based on Yolo V3 by transfer learning, and selected tracker is KCF. Besides, the user could alternate the video resources through "iscam" as shown in the figure below. Here, the real-time video signals are transmitted through the RSTP protocol. Due to privacy protection and public security, we are not allowed to provide the URL of the real-time traffic surveillance video in this case, but you could test the codes with other RSTP sources. The “region of interest” (i.e. yellow shadow in the third video below) could be added to avoid some mis-detections, such as the cars parked on the roadsides.


![image]( https://github.com/0AnonymousSite0/Data-and-Codes-for-Integrating-Computer-Vision-and-Traffic-Modelling/blob/master/2.%20Video%20clips%20and%20Screenshots/Screenshots/Transmitting%20and%20receiving%20real-time%20video%20signal.png)
Figure 4. The program is transmitting real-time traffic surveillance videos

![image](https://github.com/0AnonymousSite0/Data-and-Codes-for-Integrating-Computer-Vision-and-Traffic-Modelling/blob/master/2.%20Video%20clips%20and%20Screenshots/Screenshots/The%20program%20is%20detecting%20and%20tracking%20vehicles.png)
Figure 5. The developed detector and selected tracker is detecting and tracking vehicles


## 3.4 Codes for manipulating traffic model


This is mainly designed for automatically operate the traffic simulation model, including amendeding parameters and conducting simulation-based optimiozation of signal timing solutions. A reminder is that running this program needs the VISSIM COM API that is a commercial product, but we think that the API should be easily available, as the VISSIM is one of the most widely used transportation-related software all over the world.


![image](https://github.com/0AnonymousSite0/Data-and-Codes-for-Integrating-Computer-Vision-and-Traffic-Modelling/blob/master/2.%20Video%20clips%20and%20Screenshots/Screenshots/The%20runnning%20codes%20for%20automatically%20operate%20the%20traffic%20simulation%20model.png)
Figure 6. The program is automatically operating the traffic simulation model

![image](https://github.com/0AnonymousSite0/Data-and-Codes-for-Integrating-Computer-Vision-and-Traffic-Modelling/blob/master/2.%20Video%20clips%20and%20Screenshots/Screenshots/Screenshots%20of%20traffic%20simulation%201.png)
Figure 7. Screenshot of traffic simulation model (a)

![image](https://github.com/0AnonymousSite0/Data-and-Codes-for-Integrating-Computer-Vision-and-Traffic-Modelling/blob/master/2.%20Video%20clips%20and%20Screenshots/Screenshots/Screenshots%20of%20traffic%20simulation%202.png)
Figure 8. Screenshot of traffic simulation model (b)

