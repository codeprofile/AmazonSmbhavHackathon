
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from utils import *
from flask_cors import CORS
import os
import uuid



TEMPLATE_DIR = os.path.abspath('templates')
STATIC_DIR = os.path.abspath('styles')
app = Flask(__name__, template_folder=TEMPLATE_DIR, static_folder=STATIC_DIR)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
CORS(app)

app.config['UPLOAD_FOLDER'] = str(os.getcwd()) + "\\assets\\"


@app.route('/', methods=["GET"])
def art_gallary():
    artist_list = []
    artist_data = scanRecursive("artworkdata")
    # for dat in artist_data:
    #     artist_list.append({dat["artist_name"]:dat})
    # print(artist_list)
    # data_df = pd.DataFrame(artist_data)
    # for artist_name in data_df.artist_name.unique():
    #     artist_list.append({artist_name:data_df[data_df["artist_name"]==artist_name].to_dict()})
    return render_template('index.html',context=artist_data)


@app.route('/upload_artwork', methods=["GET"])
def upload_artwork():
    return render_template('upload_artwork.html',context={})


@app.route('/dashboard', methods=["GET"])
def dash_artwork():
    return render_template('dashboard.html')





@app.route('/upload_digital_asset_s3', methods=["POST"])
def upload_digital_asset_s3():
    print(request.form)
    print(request.files)
    if request.method == "POST":
        artist_name = request.form.get("artist_name")
        artist_description = request.form.get("artist_description")
        art_name = request.form.get("art_name")
        art_description = request.form.get("art_description")
        art_price = request.form.get("art_description")
        f = request.files['file']
        filepath = str(os.getcwd()) + "\\assets\\"
        f.save(dst=filepath + secure_filename(f.filename))
        upload_to_aws(filepath + f.filename, 'nftmetadata1', f.filename)
        insert_data = {"id":str(uuid.uuid4()).replace("-",""),"artist_name": artist_name, "artist_description": artist_description,"art_name": art_name, "art_description": art_description, "art_price": art_price
            ,"art_link":"file:\\" + filepath + f.filename}
        insert_data_db("artworkdata", insert_data)
        return render_template('upload_artwork.html',context={"message":"file and details are successfully uploaded"})



if __name__ == '__main__':
   app.run(debug = True)