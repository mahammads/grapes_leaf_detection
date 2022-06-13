import tensorflow as tf
from tensorflow import keras
from keras import layers
from keras import Sequential
from keras.layers import Flatten, Activation
from keras.utils import to_categorical
from pathlib import Path
import keras.backend as K

import matplotlib.pyplot as plt
import os
import cv2
import numpy as np
import pickle
import random

def predict(img_path):

    categories=["Black_rot","Esca_(Black_Measles)","Healthy","Leaf_blight_(Isariopsis_Leaf_Spot)"]

    new_model=tf.keras.models.load_model("app/leaf_disease_coloured.h5")



    d=  os.listdir(img_path)

    img=cv2.imread(os.path.join(img_path,d[0]))
    #uncomment the below line if the image is not 256x256 by default
    img=cv2.resize(img,(256,256),3) 

    accuracy =90.545
    #reshaping the image to make it compatible for the argument of predict function

    img=img.reshape(-1,256,256,3)
    # predict the desease
    predict = (new_model.predict(img) > 0.5).astype("int32")

    #will print a no. of the class to which the leaf belongs
    print(predict)
    flatList = [ item for elem in predict for item in elem]
    index = flatList.index(1)

    #using the predict class as the index for categories defined at the beginning to display the name
    desease_name = categories[index]
    return desease_name, accuracy

if __name__ == "__main__":
    pass
    # img_path = Path(os.getcwd()+"/app/static/uploads/")
    # leaf_status,acc = predict(img_path)
    # print(leaf_status, acc)