
# from models import *
import os

from flask import Flask, request, render_template

app = Flask(__name__)

import cv2
import numpy as np
# import base64
# from io import BytesIO
# from PIL import Image


# api to process input
@app.route('/', methods=['GET', 'POST'])
def _upload_file():
    global num_input_image
    if request.method == 'GET':
        return render_template('h1.html')
    if request.method == 'POST':
        # save choose
        choose = request.form['so_thu_tu']

        path = r"static\\" + str(int(choose)-1)
        lists = os.listdir(path)
        # hists = [file for file in hists]
        list_path = []
        for file in lists:
            list_path.append("../static/"+str(int(choose)-1) + "/" + file)
        # print(list_path)
        return render_template('h2.html', paths=list_path)


# run server
if __name__ == '__main__':
    app.run(debug=True)



