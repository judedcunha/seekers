from flask import Flask,render_template,request
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage
import cv2
import io
import numpy as np
import base64
import zipfile
import os
from PIL import Image
import pyrebase
from face_rec.predection_app import face_predectiona


config = {
  "apiKey": "AIzaSyDr4XCBr4Xd4zcckzSKmG6m7V0nMOzBBT8",
  "authDomain": "person-detection-8eed8.firebaseapp.com",
  "databaseURL": "https://person-detection-8eed8-default-rtdb.firebaseio.com",
  "projectId": "person-detection-8eed8",
  "storageBucket": "person-detection-8eed8.appspot.com",
  "messagingSenderId": "790443461965",
  "appId": "1:790443461965:web:2a5253744bc388c4bbfb04",
  "measurementId": "G-D1T0PTRK34"
}



UPLOAD_FOLDER = os.path.dirname(os.path.realpath("__file__"))
ALLOWED_EXTENSIONS = set(['zip'])
ALLOWED_EXTENSIONS1 = set(['jpg','jepg','png'])

firebase = pyrebase.initialize_app(config)
db = firebase.database()

# create flask server
app = Flask(__name__)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def allowed_file1(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS1


@app.route('/index')
def index():

   return render_template('main.html')

 
@app.route('/search')
def search():

   data_up = []

   users = db.child("search_person").get()
   data = users.val()
   
   for key, value in data.items():
      sub_data = []
      for k, v in value.items():
         sub_data.append(v)
      
      data_up.append(sub_data)

            
   
   return render_template('search.html', data = data_up)




@app.route('/getdata', methods = ['GET', 'POST'])
def getdata():
   
   data_filter = request.form['somedata'].split(",")
   print(data_filter)

   users = db.child("find_person").get()

   # for i in users.each():
   #    temp=i.val();
   #    print (temp['Age'])
   #    print(i.key(),i.val())
   #data = users.val()
   # data_key=users.key()

   # print(type(data))

   final_str = ""

   # print(data_filter[0])

   for i in users.each():   
      if not i :
         continue
      temp=i.val()



      # print(i[0])
      # print(type(i))

      # try:
      #    if (i['Full_name'].lower() == data_filter[0].lower() or data_filter[0] == "") and (i['Gender'].lower() == data_filter[1].lower() or data_filter[1] == "") and (i['Age'] == data_filter[2] or data_filter[2] == "") and (i['Height']== data_filter[3] or data_filter[3] == ""): 

      #       print(str(i['Aadhar_id']))
      #       final_str = final_str+ str(i['Aadhar_id'])+ ","
      # except Exception as e:
      #    print(str(i['Aadhar_id']))
      #    final_str = final_str+ str(i['Aadhar_id'])+ ","

      # print(i[0])
      if (temp['Full_name'].lower() == data_filter[0].lower() or data_filter[0] == ""): 
         if (temp['Gender'].lower() == data_filter[1].lower() or data_filter[1] == ""): 
            if (temp['Age'].lower() == data_filter[2].lower() or data_filter[2] == ""): 
               if (temp['Height'].lower() == data_filter[3].lower() or data_filter[3] == ""): 
      # if (i['Full_name'].lower() == data_filter[0].lower() or data_filter[0] == "") and (i['Gender'].lower() == data_filter[1].lower() or data_filter[1] == "") and (i['Age'] == data_filter[2] or data_filter[2] == "") and (i['Height']== data_filter[3] or data_filter[3] == ""): 
         
                  print(temp['Aadhar_id'])
                  final_str = final_str+ str(temp['Aadhar_id'])+ ","


   return jsonify({'msg': final_str[:-1]})


@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      
      print(request.form['aadhar'])

      file1 = request.files['pfile']
      print("here")
      print(file1)
      if file1.filename == '':
         flash('No selected file')
         return redirect(request.url)
      if file1 and allowed_file1(file1.filename):

         filename1 = secure_filename(file1.filename)
         filename1 = str(request.form['aadhar'])+".jpg"
         file1.save(os.path.join(UPLOAD_FOLDER, filename1))
         
         # photo1 = request.files['pfile']
         # in_memory_file1 = io.BytesIO()
         # photo1.save(in_memory_file1)
         # data1 = np.fromstring(in_memory_file1.getvalue(), dtype=np.uint8)
         # color_image_flag = 1
         # img1 = cv2.imdecode(data1, color_image_flag)
         
         # retval1, buffer1 = cv2.imencode('.jpg', img1)
         # jpg_as_text1 = base64.b64encode(buffer1)

         image_upload = cv2.imread(request.form['aadhar']+".jpg")

         storage = firebase.storage()
         # as admin
         storage.child( request.form['aadhar'] +".jpg").put(request.form['aadhar']+".jpg")

         # data_image1 = str(jpg_as_text1)
         # print('done')


      file = request.files['file']
      if file.filename == '':
         flash('No selected file')
         return redirect(request.url)
      if file and allowed_file(file.filename):
         filename = secure_filename(file.filename)
         filename = str(request.form['aadhar'])+".zip"
         file.save(os.path.join(UPLOAD_FOLDER, filename))
         zip_ref = zipfile.ZipFile(os.path.join(UPLOAD_FOLDER, filename), 'r')
         zip_ref.extractall(os.path.join(UPLOAD_FOLDER, "face_rec/ImagesAttendance"))
         zip_ref.close()
         print('done')


      db.child("find_person").child(request.form['aadhar'])

      data = {"Aadhar_id": request.form['aadhar'],
               "Full_name": request.form['name'],
               "Fathers_name": request.form['fname'],
               "Gender": request.form['gender'],
               "Age": request.form['age'],
               "Residence Place": request.form['rplace'],
               "Date Missing": request.form['date_missing'],
               "Place Missing": request.form['place_missing'],
               "Height": request.form['height'],
               "Weight": request.form['weight'],
               "complexion": request.form['Complexion'],
               "Build": request.form['Build'],
               "Hair": request.form['Hair'],
               "Fir_number": request.form['fir_number'],
               "Place": request.form['place']}
      db.set(data)

      

   return render_template('main.html')



@app.route("/im_size", methods=["POST"])
def process_image():
   
   file = request.files['image']
   # Read the image via file.stream
   img = Image.open(file.stream)

   pil_image = img.convert('RGB') 
   open_cv_image = np.array(pil_image) 
   
   open_cv_image = open_cv_image[:, :, ::-1].copy()
   height, width, channels = open_cv_image.shape


   height = open_cv_image.shape[0]
   width = open_cv_image.shape[1]

   new_width = 800 
   ratio = new_width / width # (or new_height / height)
   new_height = int(height * ratio)

   dimensions = (new_width, new_height)
   new_image = cv2.resize(open_cv_image, dimensions, interpolation=cv2.INTER_LINEAR)
   
   
   # img=cv2.imdecode(new_image,cv2.COLOR_BGR2RGB) # Convert Opencv format
   image_rgb = cv2.cvtColor(new_image, cv2.COLOR_BGR2RGB)
        
   data_name = face_predectiona(image_rgb)

   print(data_name[0])

   open_cv_image_rgb = cv2.cvtColor(open_cv_image, cv2.COLOR_BGR2RGB)
   _, im_arr = cv2.imencode('.jpg', open_cv_image_rgb)  # im_arr: image in Numpy one-dim array format.
   im_bytes = im_arr.tobytes()
   im_b64 = base64.b64encode(im_bytes)


   data_search_info = request.form['somedata']
   data_search = data_search_info.split(",")
   user_email = data_search[2].split('@')[0]

   if data_name[0]=='unknown':
      return jsonify({'Aadhar_id': "",
                   'Full_name': "Unkown",
                   'Fathers_name':"",
                   'Gender': "",
                   'Age': "Age",
                   'Residence_Place': "",
                   'Date_Missing': "",
                   'Place_Missing': "",
                   'Height': "",
                   'Weight': "",
                   'complexion': "",
                   'Build': "",
                   'Hair': "",
                   'Fir_number': "",
                   'Place': ""})



   users_info = db.child("user_details").child(user_email).get()
   check_fb = users_info.val()

   print(data_search)

   data_search = {"user_aadhar": check_fb['user_aadhar'],
            "user_phone": check_fb['user_phone'],
            "user_name": check_fb['user_name'],
            "user_lat": data_search[1],
            "user_long": data_search[0],
            "image": str(im_b64)}

   db.child("search_person").push(data_search)


   users = db.child("find_person").child(data_name[0]).get()
   data_fb = users.val()
   

   return jsonify({'Aadhar_id': data_fb["Aadhar_id"],
                   'Full_name': data_fb["Full_name"],
                   'Fathers_name':data_fb["Fathers_name"],
                   'Gender': data_fb["Gender"],
                   'Age': data_fb["Age"],
                   'Residence_Place': data_fb["Residence Place"],
                   'Date_Missing': data_fb["Date Missing"],
                   'Place_Missing': data_fb["Place Missing"],
                   'Height': data_fb["Height"],
                   'Weight': data_fb["Weight"],
                   'complexion': data_fb["complexion"],
                   'Build': data_fb["Build"],
                   'Hair': data_fb["Hair"],
                   'Fir_number': data_fb["Fir_number"],
                   'Place': data_fb["Place"]})





if __name__ == '__main__':
   app.run(host= '192.168.5.58',debug = True)