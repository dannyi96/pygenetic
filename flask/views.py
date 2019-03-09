#from server.flaskr import app

from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from werkzeug import secure_filename
import os
import datetime
import json
import sys

# Custom imports
#from GOF_templates import render
app = Flask(__name__)

#app.secret_key = 'secretkeyhereplease'

@app.route("/")
def home():
	return render_template("index.html",title="Check all our features",isError=False, errorMessage=False)

@app.route("/ga_online")
def ga_online():
	return render_template("features/ga_online.html", title="Online GA Execution")


@app.route("/commonCodeCreate",methods=["POST"])
def commonCodeCreate():
	payload = request.get_json()
	session["fileType"] = ".tar.gz"
	
	if(len(payload["fileType"])<=8): # else, use what user chose
		session["fileType"] = payload["fileType"]
	
	del payload["fileType"]

	print("Payload Data: ", payload)
	print("Session Data: ", session)

	if(payload["pattern"] == "adapter"):
		session["pattern"] = "adapter"
		s = render.Adapter(json.loads(json.dumps(payload)))
		s.render()
	
	elif(payload["pattern"] == "state"):
		session["pattern"] = "state"
		s = render.State(json.loads(json.dumps(payload)))
		s.render()

	elif(payload["pattern"] == "iterator"):
		session["pattern"] = "iterator"
		s = render.Iterator(json.loads(json.dumps(payload)))
		s.render()
    
	elif(payload["pattern"] == "policy"):
		session["pattern"] = "policy"
		s = render.Policy(json.loads(json.dumps(payload)))
		s.render()
	
	print("Session Data: ", session)

	return jsonify({
			"success":True
		})


@app.route("/downloadCode",methods=["POST"])
def downloadCode():
	return redirect(url_for("codeDownload",
						filename=session.get("pattern") + session.get("fileType"), 
						patternType=session.get("pattern"), 
						fileType=session.get("fileType")))


@app.route("/codeDownload/<path:filename>/<path:patternType>/<path:fileType>")
def codeDownload(filename,patternType,fileType):
	if(fileType in app.config["ALLOWED_COMPRESSED_FILE_EXTENSIONS"]):
		beautify_cmd = "astyle --style=attach -s4 -xG -xe -YFpCHUSK --recursive ./GOF_templates/templates/output/" + patternType + "/*.cpp,*.h"
		os.system(beautify_cmd)
		os.system("find . -type f -name '*.orig' -exec rm {} +")
		
		utils.checkAndCreateDownloadsFolder()

		utils.makeCompressedfile(outputFilename=os.path.join(app.config['CODE_DOWNLOAD_FOLDER'],filename),
						   sourceDir=os.path.join("./GOF_templates/templates/output/",patternType),
						   fileType=fileType)

		print("Path:",os.path.join(app.config["USER_DOWNLOAD_FOLDER"],filename))

		return send_from_directory(app.config["USER_DOWNLOAD_FOLDER"],filename,as_attachment=True)
	else:
		print("codeDownload error")
		return (render_template("index.html",isError=True,errorMessage="Please create code by choosing a pattern first."),302)


app.run()
