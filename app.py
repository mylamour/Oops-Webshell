#!/usr/bin/env python
# coding: utf-8
# author : I

from flask import Flask
from flask_httpauth import HTTPBasicAuth
import os
import logging
import configparser
from logging import Formatter, FileHandler
from flask import Flask, request, jsonify,make_response,url_for,Response,render_template
from werkzeug.utils import secure_filename
from uuid import uuid1
from webshell.webshelldetect import webshelldetect,webshelldetectsingle
from uuid import uuid1

basedir = os.path.abspath(os.path.dirname(__file__))


config = configparser.ConfigParser()
config.read('./config.ini')
php_checkpoint =  config['modules_checkpoint']['php']
asp_checkpoint =  config['modules_checkpoint']['asp']
jsp_checkpoint =  config['modules_checkpoint']['jsp']

php_yara_rule = config['yara_rule_path']['php']
asp_yara_rule = config['yara_rule_path']['asp']
jsp_yara_rule = config['yara_rule_path']['jsp']
yara_rules = config['yara_rule_path']['yararules']

php_ssdeep_features = config['ssdeep_features']['php']
asp_ssdeep_features = config['ssdeep_features']['asp']
jsp_ssdeep_features = config['ssdeep_features']['jsp']
ssdeep_features = config['ssdeep_features']['ssdeepfeatures']

workpath = config['DEFAULT']['workpath']

UPLOAD_FOLDER = config['DEFAULT']['target_path']
BLACKLISTFILEFOLDER = config['DEFAULT']['blacklist_file']
WHITELISTFILEFOLDER = config['DEFAULT']['whitelist_file']

ALLOWED_EXTENSIONS = set(['php', 'asp','aspx', 'jsp'])
# ALLOWED_EXTENSIONS = set(['zip', 'tar.gz', '7z', 'rar'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['JSON_AS_ASCII'] = False
auth = HTTPBasicAuth()


_VERSION = 1  # API version

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def check_folder(folder):
    if os.path.exists(folder):
            pass
    else:
        import pathlib
        pathlib.Path(os.path.abspath(folder)).mkdir(
            parents=True, exist_ok=True)

@app.route("/",methods=['GET','PUT'])
def index():
    return render_template('./tmp.html')



users = {
  "test":"test"

}

@auth.get_password
def get_pw(username):
    if username in users:
        return users.get(username)
    return None


@app.route("/saveblack", methods=['GET', 'POST'])
@auth.login_required
def saveblacksample():
    if request.method == 'POST':
        file = request.files['filedata']
        try:
            filename = secure_filename(file.filename)
            file.save(os.path.join(BLACKLISTFILEFOLDER, filename))
            return jsonify({"Result": "Save Sample to BlackList Sucessful"})
        except Exception as e :
            return jsonify({"Warning": "Save Failed"})
    elif request.method == 'GET':
        return jsonify({"Notice": "Use Post Upload your File For Detect"})


@app.route("/saveblackdir", methods=['GET', 'PUT'])
@auth.login_required
def saveblackdirsample():
    if request.method == 'PUT':
        res = []

        uploaded_files = request.files.getlist("filedata[]")
        dirpath = os.path.join(BLACKLISTFILEFOLDER, str(uuid1()))
        check_folder(dirpath)

        for file in uploaded_files:
            filename = secure_filename(file.filename)
            # file.save(os.path.join(dirpath, filename))
            tmpres = {
                    'filename': file.filename,
                    'stat': 'Upload Sucessful' if file.save(os.path.join(dirpath, filename)) is None else 'Upload Failed'
                }
            res.append(tmpres)
        return jsonify({"Result": res})


    elif request.method == 'GET':
        return jsonify({"Warning": "Only use put to upload your file for detect"})

@app.route("/savewhite", methods=['GET', 'POST'])
@auth.login_required
def savewhitesample():
    if request.method == 'POST':
        file = request.files['filedata']
        try:
            filename = secure_filename(file.filename)
            file.save(os.path.join(WHITELISTFILEFOLDER, filename))
            return jsonify({"Result": "Save Sample to WhiteList Sucessful"})
        except Exception as e :
            print(e)
            return jsonify({"Warning": "Save Failed"})

    elif request.method == 'GET':
        return jsonify({"Notice": "Use Post Upload your File For Detect"})


@app.route("/savewhitedir", methods=['GET', 'PUT'])
@auth.login_required
def savewhitedirsample():
    if request.method == 'PUT':
        res = []

        uploaded_files = request.files.getlist("filedata[]")
        dirpath = os.path.join(WHITELISTFILEFOLDER, str(uuid1()))
        check_folder(dirpath)

        for file in uploaded_files:
            filename = secure_filename(file.filename)

            tmpres = {
                'filename': file.filename,
                'stat': 'Upload Sucessful' if file.save(os.path.join(dirpath, filename)) is None else 'Upload Failed'
            }
            res.append(tmpres)
        return jsonify({"Result": res})

    elif request.method == 'GET':
        return jsonify({"Warning": "Only use put to upload your file for detect"})

@app.route("/detect", methods=['GET','POST'])
@auth.login_required
def upload():
    if request.method == 'POST':
        file = request.files['filedata']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER,filename))
            if filename.endswith('php'):
                res = webshelldetectsingle(os.path.join(UPLOAD_FOLDER,filename),php_checkpoint)
            elif filename.endswith('asp') or filename.endswith('aspx'):
                res = webshelldetectsingle(os.path.join(UPLOAD_FOLDER, filename),asp_checkpoint)
            # JSP model 
                
            # May be there need a benchmark function
            return jsonify({"Result":res})
        else:
            return jsonify({"Warning":"Not file or not Allowed type"})
    elif request.method == 'GET':
        return jsonify({"Warning":"Only use POST to upload your file for detect"})

@app.route("/detectdir", methods=['GET','PUT'])
@auth.login_required
def uploaddir():
    if request.method == 'PUT':
        uploaded_files = request.files.getlist("filedata[]")
        dirpath = os.path.join(UPLOAD_FOLDER, str(uuid1()))
        check_folder(dirpath)
        for file in uploaded_files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(dirpath,filename))
        
        res = webshelldetect(dirpath,ssdeep_features,yara_rules,php_checkpoint)
        return jsonify({"Result":res})

    elif request.method == 'GET':
        return jsonify({"Warning":"Only use put to upload your file for detect"})

@app.errorhandler(500)
def internal_error(error):
    print(str(error))  

@app.errorhandler(404)
def not_found_error(error):
    print(str(error))

@app.errorhandler(405)
def not_allowed_error(error):
    print(str(error))

if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: \
            %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

if __name__ == '__main__':
    app.debug = True
    app.run(host="0.0.0.0",port = int(8080))
