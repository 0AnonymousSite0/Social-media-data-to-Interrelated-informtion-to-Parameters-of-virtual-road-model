# Extract interrelated information from social media data and incorporate them into virtual road models


# 0. A demonstration video of the SM2II2VP approach 

![image](https://github.com/0AnonymousSite0/Social-media-for-road-transport-model/blob/main/A%20demonstrtaion%20video.gif)


# 1. General Introduction

1.1 This repository aims at providing the codes and data regarding the paper entitled “……” for the public, and it is developed by The University of ****.

1.2 All codes are developed on Python 3.6 or 3.7, and the IDE adopted is PyCharm (Professional version). The codes also support the GPU computing for higher speed; the Navida CUDA we adopted is V10.0.130.

1.3 We greatly appreciate the selfless spirits of these voluntary contributors of a series of open python libraries, including 
Bert (https://github.com/google-research/bert), Tensorflow (https://github.com/tensorflow/models), pytorch (https://github.com/pytorch/pytorch), Keras (https://github.com/keras-team/keras), Numpy (https://numpy.org/), labelImg (https://github.com/tzutalin/labelImg), pyExcelerator (https://github.com/WoLpH/pyExcelerator), py2neo (https://github.com/py2neo-org/py2neo), some base works (https://github.com/yongzhuo/Keras-TextClassification, https://github.com/zjunlp/DeepKE/tree/master), and so on. Our work stands on the shoulders of these giants.

1.4 Before submitting these codes to Github, all of them have been tested to be well-performed as shown in the video above.

1.5 The Python environment clone based on Anaconda is provided in Google Drive (https://drive.google.com/drive/folders/1iqD30Gqp4zKBqnEm0Uup64xuQndZz6lT?usp=sharing). Even so, we are not able to guarantee their operation in other computing environments due to the differences in the python version, computer operating system, and adopted hardware.

1.6 As for anything regarding the copyright, please refer to the MIT License or contact the authors.


# 2 The specifications of reusing the codes

2.1 Run the “SM_to_Interrelated_Information_to_VRM_Parameters.py”

2.1 Use your own key of twitter API

2.2 Use your own Neo4j parameters

2.3 The license of ArcGis and VISSIM is indispensable






## 1.1 Codes for training an object detector with transfer learning


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

