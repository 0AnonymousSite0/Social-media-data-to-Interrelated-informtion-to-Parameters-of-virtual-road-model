# Extract interrelated information from social media data and incorporate them into virtual road models

!!! As the paper is under review, all contents in this repository currently are not allowed to be used by anyone until this announcement is deleted.  

# 0. A demonstration video of the SMD2II2PM approach 

![image](https://github.com/0AnonymousSite0/Social-media-for-road-transport-model/blob/main/A%20demonstrtaion%20video.gif)


# 1. General Introduction

1.1 This repository aims at providing the codes and data regarding the paper entitled “……” for the public, and it is developed by The University of ****.

1.2 All codes are developed on Python 3.6 or 3.7, and the IDE adopted is PyCharm (Professional version). The codes also support the GPU computing for higher speed; the Navida CUDA we adopted is V10.0.130. The Gis platform is Arcgis Pro 2.3, and the VRM platform is VISSIM 11; their liciences are necessary. 

1.3 We greatly appreciate the selfless spirits of these voluntary contributors of a series of open python libraries, including 
Bert (https://github.com/google-research/bert), Tensorflow (https://github.com/tensorflow/models), pytorch (https://github.com/pytorch/pytorch), Keras (https://github.com/keras-team/keras), Numpy (https://numpy.org/), labelImg (https://github.com/tzutalin/labelImg), pyExcelerator (https://github.com/WoLpH/pyExcelerator), py2neo (https://github.com/py2neo-org/py2neo), some base works (https://github.com/yongzhuo/Keras-TextClassification, https://github.com/zjunlp/DeepKE/tree/master), and so on. Our work stands on the shoulders of these giants.

1.4 Before submitting these codes to Github, all of them have been tested to be well-performed as shown in the video above.

1.5 The running environment clone based on Anaconda is provided in Google Drive (https://drive.google.com/drive/folders/1AjB1-vfJvOrtOM6J6NGbZhTUoHTRnemO?usp=sharing). Even so, we are not able to guarantee their operation in other computing environments due to the differences in the python version, computer operating system, and adopted hardware.

1.6 As for anything regarding the copyright, please refer to the MIT License or contact the authors.

# 2 The specifications of critical codes

## 2.1 Run the whole approach: “SM_to_Interrelated_Information_to_VRM_Parameters.py” 

Use your own key of twitter API and Neo4j parameters

![image](https://github.com/0AnonymousSite0/Social-media-for-road-transport-model/blob/main/Screenshots%20and%20Figures/Screenshot1.jpg)

Adjust the file directories and replace the tailor-made model

![image](https://github.com/0AnonymousSite0/Social-media-for-road-transport-model/blob/main/Screenshots%20and%20Figures/Screenshot2.jpg)

Adjust the file directories regarding the convertor

![image](https://github.com/0AnonymousSite0/Social-media-for-road-transport-model/blob/main/Screenshots%20and%20Figures/Screenshot3.jpg)

## 2.2 Train the SM2II model and develop the II2VP convertor:




