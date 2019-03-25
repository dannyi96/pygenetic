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
	import sys
	sys.path.insert(0, '../pyGenetic')
	# import GAEngine
	# import Utils
	# import ChromosomeFactory
	payload = request.form
	code = "import GAEngine\nimport Utils\nimport ChromosomeFactory\n"
	for i in payload:
		print(payload[i])

	# for i in range(20):
	# 	print(payload[i])
	#session["fileType"] = ".tar.gz"

	#if(len(payload["fileType"])<=8): # else, use what user chose
	#	session["fileType"] = payload["fileType"]

	#del payload["fileType"]

	print("Payload Data: ", payload)

	if(payload["gene-generation"]=="1drange"):
		if(payload["1drange-duplicate"]=="yes"):
			duplicates=True
		elif(payload["1drange-duplicate"]=="no"):
			duplicates=False
		#factory = ChromosomeFactory.ChromosomeRangeFactory(payload["1drange-datatype"],int(payload["no-of-genes"]),int(payload["1drange-min"]),int(payload["1drange-max"]),str(duplicates))
		print(">>> str(duplicates) is ",str(duplicates))
		code += "factory = ChromosomeFactory.ChromosomeRangeFactory("+payload["1drange-datatype"]+","+payload["no-of-genes"]+","+payload["1drange-min"]+","+payload["1drange-max"]+","+str(duplicates)+")\n"
	elif(payload["gene-generation"]=="1dregex"):
		#factory = ChromosomeFactory.ChromosomeRegexFactory(payload["1dregex-datatype"],int(payload["no-of-genes"]),payload["1dregex-regex"])
		code += "factory = ChromosomeFactory.ChromosomeRangeFactory("+payload["1dregex-datatype"]+","+payload["no-of-genes"]+",'"+payload["1dregex-regex"]+"'"+")\n"

	print()
	print(code,"\n*******")

	if(payload["pySpark"]=="yes"):
		pyspark = True
	elif(payload["pySpark"]=="no"):
		pyspark = False

	if(payload["adaptive-mutation"]=="yes"):
		adaptive = True
	elif(payload["adaptive-mutation"]=="no"):
		adaptive = False

	if(payload["fitness-type"]=="min" or payload["fitness-type"]=="max"):
		fit_type = "'"+payload["fitness-type"]+"'"
	elif(payload["fitness-type"]=="equal"):
		fit_type = ('equal',float(payload["fitness-equal"]))
	
	#ga = GAEngine.GAEngine(factory=factory,population_size=int(payload["population-size"]),cross_prob=float(payload["crossover-rate"]),mut_prob=float(payload["mutation-rate"]),fitness_type=fit_type,adaptive_mutation=adaptive)
	code += "ga = GAEngine.GAEngine(factory=factory,population_size="+payload["population-size"]+",cross_prob="+payload["crossover-rate"]+",mut_prob="+payload["mutation-rate"]+",fitness_type="+str(fit_type)+",adaptive_mutation="+str(adaptive)+",use_pyspark="+str(pyspark)+")\n"

	code += "ga.addCrossoverHandler(Utils.CrossoverHandlers."+payload["crossover-type"]+","+payload["crossover-weight"]+")\n"
	code += "ga.addMutationHandler(Utils.MutationHandlers."+payload["mutation-type"]+","+payload["mutation-weight"]+")\n"
	code += "ga.setSelectionHandler(Utils.SelectionHandlers."+payload["selection-type"]+")\n"
	code += "ga.setFitnessHandler(Utils.Fitness."+payload["fitness"]+")\n"
	code += "ga.evolve("+payload["no-of-evolutions"]+")\n"
	# Take care of pyspark flag
	print()
	print(code,"\n*******")
	print()
	exec(code)
	

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
