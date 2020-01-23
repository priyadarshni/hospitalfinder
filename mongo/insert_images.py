import numpy as np
import pymongo
import gridgrid
import cv2
import random

connection = pymongo.MongoClient("mongodb+srv://mongoproject:priya123@cluster0-jvyqt.mongodb.net/test?retryWrites=true&w=majority")


db = connection['hospitals']
collection = db['images']
file_used = ["hos1.jpg","hos2.jpg","hos3.jpg","hos4.jpg","hos5.jpg","hos6.jpg","hos7.jpg","hos8.jpg","hos9.jpg","hos10.jpg","hos11.jpg","hos12.jpg","hos13.jpg","hos14.jpg"]
grid = gridgrid.Gridgrid(db, 'images') 
def main():

    a=random.randint(1,10)
    image = collection.find_one({'name': 'image'+str(a)+'.jpg'})['images'][0]


    gOut = grid.get(image['imageID'])


    image = np.frombuffer(gOut.read(), dtype=np.uint8)     
    image = np.reshape(image, image['shape'])    
    cv2.imshow('frame',image)
    cv2.waitKey(8000)

if __name__ == '__main__':
    main()