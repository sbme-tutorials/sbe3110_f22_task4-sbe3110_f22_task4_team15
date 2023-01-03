from flask import Flask, render_template, send_file, request, redirect, jsonify
import numpy as np
import matplotlib.pyplot as plt
import math
import skimage.io 
from skimage.color import rgb2gray
from flask import Flask, render_template , request , jsonify
import cv2
import numpy as np 
import base64
import io
import PIL.Image as Pimage
import base64
from Fourier import Image
import json



app = Flask(__name__)
 
first_image=Image()
second_image=Image()


def encode_plt(file_name1):
    im= Pimage.open(file_name1)  
    data = io.BytesIO()
    im.save(data, "JPEG")
    encoded_img_data = base64.b64encode(data.getvalue())

    return encoded_img_data  


def decode_img(file,filename):
    npimg = np.fromstring(file, np.uint8)
    img = cv2.imdecode(npimg,cv2.IMREAD_COLOR)
    img = Pimage.fromarray(img.astype("uint8"))
    rawBytes = io.BytesIO()
    img.save(rawBytes, "JPEG")
    rawBytes.seek(0)
    img_base64 = base64.b64encode(rawBytes.read()) 
    with open("image.jpg", "wb") as fh:
        fh.write(base64.decodebytes(img_base64))  
    img = skimage.io.imread("image.jpg") 
    cv2.imwrite(filename, img) 
    original_image = cv2.imread(filename) 

    return original_image         


def save_magnitude_phase_plts(image,image_file_name1,image_file_name2):
    fig = plt.figure(figsize=(5, 5))
    plt.imshow(np.log(image.fourier_transformed_image_magnitude))
    plt.savefig(image_file_name1)
    plt.imshow(image.fourier_transformed_image_phase)
    plt.savefig(image_file_name2)

def save_reconstructed_image(reconstructed):
    fig = plt.figure(figsize=(4, 4))
    plt.imshow(np.abs(reconstructed), cmap='gray')
    plt.savefig('reconstructed.jpg')





@app.route("/", methods=["GET", "POST"])
def index():
    global first_image
    global second_image

    if request.method == "POST":


        if  request.get_json() != None:
            output = request.get_json()
            co = json.loads(output)

            reconstructed=first_image.reconstruct(second_image,co['Mag_rectangle_x: ' ]
            ,co['Mag_rectangle_y: '],co['Mag_rectangle_width: ' ],co['Mag_rectangle_height: '],
            co['Phase_rectangle_x: '],co['Phase_rectangle_y: '],co['Phase_rectangle_width: '],co[ 'Phase_rectangle_height: ' ],co['mode:'])
            
            save_reconstructed_image(reconstructed)
            encoded_img_data1=encode_plt("reconstructed.jpg")
            return jsonify({'status':str(encoded_img_data1)})

        file= request.files['image'].read()   # /// read image
        default_value = '0'
        name = request.form.get('name', default_value)   # //// to know which image is sent (image1 or iamge2)    
        
        if name==str(1):
            original_image1=decode_img(file,'image1.jpg')  
            first_image=Image(rgb2gray(original_image1),438,789,97)
            save_magnitude_phase_plts(first_image,"mag1.jpg","phase1.jpg")
            encoded_img_data1=encode_plt("mag1.jpg")
            encoded_img_data2=encode_plt("phase1.jpg")
        else:
            original_image2=decode_img(file,'image2.jpg') 
            second_image=Image(rgb2gray(original_image2),438,789,436)
            save_magnitude_phase_plts(second_image,"mag2.jpg","phase2.jpg")
            encoded_img_data1=encode_plt("mag2.jpg")
            encoded_img_data2=encode_plt("phase2.jpg")      

        return jsonify({'status':str(encoded_img_data1),'status2':str(encoded_img_data2)})



    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True, threaded=True)  
