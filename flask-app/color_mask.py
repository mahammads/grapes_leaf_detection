import cv2
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
import os

# nemo = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
# plt.imshow(nemo)
# plt.show()
def affected_region(img_path):

    d=  os.listdir(img_path)
    img=cv2.imread(os.path.join(img_path,d[0]))

    hsv_nemo = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)

    sensitivity = 5
    lower_bound = np.array([94 - sensitivity, 80, 2]) 
    upper_bound = np.array([94 + sensitivity, 255, 255]) 
    #create mask 
    msk = cv2.inRange(hsv_nemo, lower_bound, upper_bound) 

    result = cv2.bitwise_and(img, img, mask=msk)
   
    def calcPercentage(msk): 
        ''' 
        returns the percentage of white in a binary image 
        ''' 
        height, width = msk.shape[:2] 
        num_pixels = height * width 
        count_brown = cv2.countNonZero(msk) 
        percent_bronw = (count_brown/num_pixels) * 100 
        percent_bronw = round(percent_bronw,2) 
        return percent_bronw 
    perc = calcPercentage(msk)
    print(perc)
    return result, perc

if __name__ == "__main__":
    # gray_path = Path(os.getcwd()+"/app/static/uploads/")
    # output_name = 'app/static/uploads/InfraBl.jpg'
    # fig,percet =  affected_region(gray_path)
    # cv2.imwrite(output_name,fig)
    # print(percet)
    pass