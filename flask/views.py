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
	form_data = request.form
	print(form_data)
	code_lines = ["import GAEngine, ChromosomeFactory, Utils"]
	#session["fileType"] = ".tar.gz"

	#if(len(payload["fileType"])<=8): # else, use what user chose
	#	session["fileType"] = payload["fileType"]

	#del payload["fileType"]

	print("Payload Data: ", form_data)
	if form_data["gene-generation"] == "1dregex":
		code_lines.append("factory = ChromosomeFactory.ChromosomeRegexFactory(%s,%s,'%s')"%(form_data["1dregex-datatype"],
							form_data["no-of-genes"], form_data["1dregex-regex"]))
	# Handle other stuff here
    


	

	if form_data["fitness-type"] == "equal":
		code_lines.append("ga = GAEngine.GAEngine(factory,%s,fitness_type=('equal',%s), cross_prob=%s, mut_prob = %s)"%(form_data["population-size"],
				form_data['fitness-equal'], form_data['crossover-rate'], form_data['mutation-rate']	))
	else:
		code_lines.append("ga = GAEngine.GAEngine(factory,%s,fitness_type='%s', cross_prob=%s, mut_prob = %s)"%(form_data["population-size"],
				form_data['fitness-type'], form_data['crossover-rate'], form_data['mutation-rate']	))

	if form_data["fitness"] != "custom":
		code_lines.append("ga.setFitnessHandler(Utils.Fitness.%s)"%(form_data["fitness"]))
	# Handle other stuff here




	if form_data["crossover-type"] != "custom":
		code_lines.append("ga.addCrossoverHandler(Utils.CrossoverHandlers.%s, %s)"%(form_data['crossover-type'],
				form_data['crossover-weight']))

	if form_data["mutation-type"] != "custom":
		code_lines.append("ga.addMutationHandler(Utils.MutationHandlers.%s,%s)"%(form_data['mutation-type'],
				form_data['mutation-weight']))

	if form_data["selection-type"] != "custom":
		code_lines.append("ga.setSelectionHandler(Utils.SelectionHandlers.%s)"%(form_data["selection-type"]))

	code_lines.append("ga.evolve(%s)"%(form_data['no-of-evolutions']))
	print('\n'.join(code_lines))
	#print("Session Data: ", session)

	#if(payload["pattern"] == "adapter"):
	#	session["pattern"] = "adapter"
	#	s = render.Adapter(json.loads(json.dumps(payload)))
	#	s.render()

	#elif(payload["pattern"] == "state"):
	#	session["pattern"] = "state"
	#	s = render.State(json.loads(json.dumps(payload)))
	#	s.render()

	#elif(payload["pattern"] == "iterator"):
	#	session["pattern"] = "iterator"
	#	s = render.Iterator(json.loads(json.dumps(payload)))
	#	s.render()

	#elif(payload["pattern"] == "policy"):
	#	session["pattern"] = "policy"
	#	s = render.Policy(json.loads(json.dumps(payload)))
	#	s.render()

	#print("Session Data: ", session)

	return jsonify({
			"success":True
		})


@app.route("/downloadCode",methods=["POST"])
def downloadCode():
	return redirect(url_for("codeDownload",
						filename=session.get("pattern") + session.get("fileType"),
						patternType=session.get("pattern"),
						fileType=session.get("fileType")))



app.run()
