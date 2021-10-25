<h3>Driver Drowsiness Detection System</h3>

<h2>Introduction</h2>
<br>The project is fully based on AI and lies in the field of computer vision and Machine learning. The project focuses to capture the real-time drowsy state of driver through the eyes state the dataset for building the model will be the images of eyes which is categorized into open eyes dataset and close eyes dataset. The model is built by training the open/close eyes images so the project is based on supervised learning and to build the model CNN (Convolution Neural Network) algorithm is used as it works better than other algorithm as the dataset are the set of images.</br>
<br>A camera is placed in front of the driver that processes the images frames from the video and with the Voila Jones algorithm it detects the face structure and with the haar cascade eye classifier we can able to detect the ROI i.e. eyes After extracting the eyes from the video the image is feed to the CNN model and the model identify whether the eyes are open or closed. And if the eyes are closed for a certain frames the alarm is buzzed. If the user close the eyes the counter value appears in the frame starting from 10 and if the user continuously close the eyes the counter value decrease and reaches to 0 and the alarm buzzed to alert the driver showing alert message on the screen.</br>

<h2>Aims of the project</h2>
<br>* Developing a face detection system.</br>
<br>* Extracting the facial region especially eyes.</br>
<br>* Developing the drowsiness detection system through eye closure/blink.</br>
<br>* Developing a complete web based application</br>

<h2>Datasets</h2>
<br>I have taken the dataset from “MRL Eye Dataset”. The dataset consists the total images of 84,898 with the data of total 37 different persons 4 women and 33 men. The dataset images are low and high resolution and all are captured in different lighting conditions. This dataset was really developed to detect the pupil of the eyes but for the project the dataset is used for training the CNN model to differentiate between open and close eyes.</br>

<h2>Building a Model</h2>
<br>For this project to build the model 2 different approaches and technique are considered and among them best technique is finalized and consider as a real model. The two approaches are:</br>
<br>* Building the model by own</br>
<br>* Using the concept of transfer learning</br>

<h1>Building the model by own</h1>
<br>Here first the dataset is prepared and split into training, validation and testing. About 17000 images are considered and out of that about 12000 images are taken for testing, about 2000 images are taken for validation and about 3000 images for testing the model. After that total three folder is created for training, validation and testing and in each of the folder again two sub folder is created as Open Eyes where all open eyes image are placed and other Close Eyes where all close eyes image are placed and the process to make model start. After running about 10 epoch the model get the accuracy of 93% on training data while 94% on validation data which is good as it was able to identify between open and close eyes. But it got only 81% on testing data.</br>

<img src="images/1.JPG">  <img src="images/2.JPG"> 

<h1>Using the concept of Transfer Learning</h1>
<br>For the second approach I have used the concept of transfer learning to create the model. Transfer learning means to transfer the knowledge of already pertained model to the model we are going to build. This technique is used to see if transfer learning technique performs better than the model we created. As we are going to use pre trained model we didn’t use many images to build our model For this model only 1672 images are taken for training, and 500 images for testing for validation I have used 10% data out of 1672 training images. We can take small amount of data and can build the model with higher accuracy and testing accuracy. For this the same above process is repeat and two folder namely training and testing is created and inside each of them again sub folder open eyes and close eyes are created. Open eyes images are placed in open eyes folder and close eyes image are taken into close eyes folder. After running about 10 epoch the model get the accuracy of 100% on training data as well 100% on validation data which is good as it was able to identify between open and close eyes. But it got only 89.66% on testing data i.e. about 90% which is better than above model.</br>  




