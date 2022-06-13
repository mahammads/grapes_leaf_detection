from genericpath import exists
import cv2
import os 
from pathlib import Path

def grayscale(img_path):
    d=  os.listdir(img_path)
    image=cv2.imread(os.path.join(img_path,d[0]))
    cv2.imshow('Original',image)
    grayscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    cv2.imshow('Grayscale', grayscale)
    return grayscale
    # img = os.path.join(gray_path , 'Grayscale.jpg')
    # cv2.imwrite((img), grayscale)
if __name__ == "__main__":
    # gray_path = Path(os.getcwd()+"/app/static/uploads/")
    # image = grayscale(gray_path)
    # cv2.imshow('new',image)
    pass