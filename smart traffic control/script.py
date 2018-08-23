import os
from flask import Flask, render_template, request, redirect, session, url_for, flash, send_file, jsonify
from werkzeug import secure_filename
import numpy as np
import cv2
import shutil


app = Flask(__name__)
app.secret_key = os.urandom(24)


@app.route('/upload')
def upload():
	return render_template('index.html')

count = 0

@app.route('/upload',methods=['POST', 'GET'])
def upload_post():
	global count
	if request.method=='POST':
		img=request.files['img']
		count += 1
		new_name = 'image'+str(count)
		img.save(secure_filename(new_name))
		shutil.move(new_name, 'images/')

		car_cascade = cv2.CascadeClassifier('cars3.xml')
		img_name = 'images/'+new_name
		frames = cv2.imread(img_name)
		gray = cv2.cvtColor(frames, cv2.COLOR_BGR2GRAY)
		cars = car_cascade.detectMultiScale(gray, 1.1, 1)

		return str(len(cars))


if __name__ == '__main__':
	app.run(debug=True)
