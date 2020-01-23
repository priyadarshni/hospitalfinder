from functools import wraps
import logging
import random
import threading
import numpy as np
import pymongo
import gridgrid
import cv2
import random
from flask import Flask, request, session, url_for, redirect, render_template
from mongo.user_mongo import UserMongo
from mongo import connect


_PORT = 5000
_HOST = '0.0.0.0'
_DEBUG = True

APP_NAME = "hospitalfinder"   

app = Flask(__name__)


@app.route('/')
def root():
    return render_template('index.html')


@app.route('/search', methods=["POST"])
def search():
    DEBUG_INFO = "app.py - /search - "
    query = request.form['search_box']
    query.strip()
    logging.debug(DEBUG_INFO + "query = " + query)

  
    if len(query) > 1:
       
        myresults=connect.get_data(query)
        import json
        myresults=json.loads(myresults)
                   
            
        return render_template('results.html', search_results=myresults)
        
    else:
        return redirect(url_for('index'))
        



def main():
    connection = pymongo.MongoClient("mongodb+srv://mongoproject:priya123@cluster0-jvyqt.mongodb.net/test?retryWrites=true&w=majority")
    db = connection['hospitals']
    testCollection = db['images']
    file_meta = db.file_meta
    file_used = ["hos1.jpg","hos2.jpg","hos3.jpg","hos4.jpg","hos5.jpg","hos6.jpg","hos7.jpg","hos9.jpg","hos10.jpg","hos11.jpg"]
    grid = gridgrid.Gridgrid(db, 'images') 
    
    
    a=random.randint(1,9)
    image = testCollection.find_one({'name': 'hos'+str(a)+'.jpg'})['images'][0]

# get the image from gridFS
    gOut = grid.get(image['imageID'])


    img = np.frombuffer(gOut.read(), dtype=np.uint8)     
    img = np.reshape(img, image['shape'])    
    cv2.imwrite('images/hos.jpg',img)
    connection.close()    
@app.route('/display/<string:id>')
def display_doc(id):
    
    if request.method == 'GET':
        results = list() 
        image_results = list()
        imageID = list()   
        query = id
        print(id)
        # Retrieve all details of the hospital
        query_results = connect_dbr.get_multiple_data1(id)
        import json      
        query_results=json.loads(query_results)
        
        for query_result in query_results:
           
            lat, long = connect.get_geo_info(query_result["STATE"])
            result = [query_result["ID"], query_result["NAME"],
                            query_result["ADDRESS"], query_result["CITY"],
                            query_result["STATE"], query_result["STATUS"],
                            query_result["POPULATION"], query_result["NAICS_DESC"],
                            query_result["NAICS_CODE"], query_result["SOURCE"],
                            query_result["X"],query_result["Y"]]
            results.append(result)
            main()
            
    return render_template("display.html", results=results)



if __name__ == '__main__':
   
    app.run(host=_HOST, debug=_DEBUG, port=_PORT)
    
