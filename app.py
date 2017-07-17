#!/usr/bin/env python
# coding: utf-8
# author : I

from flask import Flask
import os
import logging
import configparser
from logging import Formatter, FileHandler
from flask import Flask, request, jsonify,make_response,url_for,Response
from werkzeug.utils import secure_filename
from uuid import uuid1
from webshell.webshelldetect import webshelldetect

basedir = os.path.abspath(os.path.dirname(__file__))


config = configparser.ConfigParser()
config.read('./config.ini')
php_checkpoint =  config['modules_checkpoint']['php']
asp_checkpoint =  config['modules_checkpoint']['asp']
jsp_checkpoint =  config['modules_checkpoint']['jsp']

php_yara_rule = config['yara_rule_path']['php']
asp_yara_rule = config['yara_rule_path']['asp']
jsp_yara_rule = config['yara_rule_path']['jsp']

php_ssdeep_features = config['ssdeep_features']['php']
asp_ssdeep_features = config['ssdeep_features']['asp']
jsp_ssdeep_features = config['ssdeep_features']['jsp']

workpath = config['DEFAULT']['workpath']

UPLOAD_FOLDER = config['DEFAULT']['target_path']
ALLOWED_EXTENSIONS = set(['php', 'asp', 'jsp'])
# ALLOWED_EXTENSIONS = set(['zip', 'tar.gz', '7z', 'rar'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

_VERSION = 1  # API version

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/detect", methods=['GET','PUT'])
def upload():
    if request.method == 'PUT':
        file = request.files['filedata']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))  # str(uuid1())
            res = webshelldetect(app.config['UPLOAD_FOLDER'],php_ssdeep_features,php_yara_rule,php_checkpoint)
            # May be there need a benchmark function
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