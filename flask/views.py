#from server.flaskr import app

from flask import Flask, render_template, request, redirect, url_for, session, jsonify, send_from_directory
from werkzeug import secure_filename
from urllib.parse import unquote
import os
import datetime
import json
import sys
import matplotlib.pyplot as plt

ga = None
file_index = 0

# Custom imports
#from GOF_templates import render
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = '/uploads/'
#app.secret_key = 'secretkeyhereplease'

@app.route("/")
def home():
	return render_template("index.html",title="Check all our features",isError=False, errorMessage=False)

@app.route("/ga_online")
def ga_online():
	return render_template("features/ga_online.html", title="Online GA Execution")


@app.route("/commonCodeCreate",methods=["POST"])
def commonCodeCreate():
	global file_index
	import sys
	sys.path.insert(0, '../pyGenetic')
	# import GAEngine
	# import Utils
	# import ChromosomeFactory
	payload = request.form
	precode = "import GAEngine\nimport Utils\nimport ChromosomeFactory\n"
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
		code = "factory = ChromosomeFactory.ChromosomeRangeFactory(data_type="+payload["1drange-datatype"]+",noOfGenes="+payload["no-of-genes"]+",minValue="+payload["1drange-min"]+",maxValue="+payload["1drange-max"]+",duplicates="+str(duplicates)+")\n"
	elif(payload["gene-generation"]=="1dregex"):
		#factory = ChromosomeFactory.ChromosomeRegexFactory(payload["1dregex-datatype"],int(payload["no-of-genes"]),payload["1dregex-regex"])
		code = "factory = ChromosomeFactory.ChromosomeRangeFactory(data_type="+payload["1dregex-datatype"]+",noOfGenes="+payload["no-of-genes"]+",pattern='"+payload["1dregex-regex"]+"'"+")\n"

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
	
	code += "ga = GAEngine.GAEngine(factory=factory,population_size="+payload["population-size"]+",cross_prob="+payload["crossover-rate"]+",mut_prob="+payload["mutation-rate"]+",fitness_type="+str(fit_type)+",adaptive_mutation="+str(adaptive)+",use_pyspark="+str(pyspark)+")\n"
	
	i = 0
	while True:
		if "crossover-type"+str(i) in payload.keys():
			if(payload["crossover-type"+str(i)] != "custom"):
				code += "ga.addCrossoverHandler(Utils.CrossoverHandlers."+payload["crossover-type"+str(i)]+","+payload["crossover-weight"+str(i)]+")\n"
			else:
				cleaned = unquote(payload["custom-crossover"+str(i)])
				custom_name = cleaned[cleaned.find("def ")+4:]
				custom_name = custom_name[:custom_name.find("(")]
				precode += cleaned + "\n"
				code += "ga.addCrossoverHandler("+custom_name+","+payload["crossover-weight"+str(i)]+")\n"
			i+=1
		else:
			break

	i = 0
	while True:
		if "mutation-type"+str(i) in payload.keys():
			if(payload["mutation-type"+str(i)] != "custom"):
				code += "ga.addMutationHandler(Utils.MutationHandlers."+payload["mutation-type"+str(i)]+","+payload["mutation-weight"+str(i)]+")\n"
			else:
				cleaned = unquote(payload["custom-mutation"+str(i)])
				custom_name = cleaned[cleaned.find("def ")+4:]
				custom_name = custom_name[:custom_name.find("(")]
				precode += cleaned + "\n"
				code += "ga.addMutationHandler("+custom_name+","+payload["mutation-weight"+str(i)]+")\n"
			i+=1
		else:
			break
	

	if(payload["selection-type"] != "custom"):
		code += "ga.setSelectionHandler(Utils.SelectionHandlers."+payload["selection-type"]+")\n"
	else:
		cleaned = unquote(payload["custom-selection"])
		custom_name = cleaned[cleaned.find("def ")+4:]
		custom_name = custom_name[:custom_name.find("(")]
		precode += cleaned + "\n"
		code += "ga.setSelectionHandler("+custom_name+")\n"

	

	if(payload["fitness"] != "custom"):
		code += "ga.setFitnessHandler(Utils.Fitness."+payload["fitness"]+")\n"
	else:
		cleaned = unquote(payload["custom-fitness"])
		custom_name = cleaned[cleaned.find("def ")+4:]
		custom_name = custom_name[:custom_name.find("(")]
		precode += cleaned + "\n"
		if(unquote(payload["extra-data"]).strip() != "#Enter data here" and payload["extra-data"] != ''):
			datas = unquote(payload["extra-data"]).split('\r\n')
			if(datas[-1].strip() == ''):
				datas = datas[:len(datas)-1]
			datas_string = ""
			for x in datas:
				precode += x +"\n"
				datas_string += "," + x[:x.find("=")].strip()

			code += "ga.setFitnessHandler("+custom_name + datas_string +")\n"
		else:
			code += "ga.setFitnessHandler("+custom_name+")\n"

	code += "ga.evolve("+payload["no-of-evolutions"]+")\n"
	# Take care of pyspark flag
	code = precode + code
	print()
	print("complete code ---> \n",code,"\n*******")
	print()
	filename = str(file_index)
	file_index += 1
	file = open("static/uploads/"+filename+".py", "w")
	file.write(code)
	file.close()
	return jsonify({'Filename': filename})
	#exec(code,globals())

	

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

	#return jsonify({
	#		"success":True
	#	})

@app.route('/ga_init',methods=['POST'])
def ga_init():
	import sys
	sys.path.insert(0, '../pyGenetic')

	payload = request.form
	precode = "import GAEngine\nimport Utils\nimport ChromosomeFactory\n"
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
		code = "factory = ChromosomeFactory.ChromosomeRangeFactory(data_type="+payload["1drange-datatype"]+",noOfGenes="+payload["no-of-genes"]+",minValue="+payload["1drange-min"]+",maxValue="+payload["1drange-max"]+",duplicates="+str(duplicates)+")\n"
	elif(payload["gene-generation"]=="1dregex"):
		#factory = ChromosomeFactory.ChromosomeRegexFactory(payload["1dregex-datatype"],int(payload["no-of-genes"]),payload["1dregex-regex"])
		code = "factory = ChromosomeFactory.ChromosomeRangeFactory(data_type="+payload["1dregex-datatype"]+",noOfGenes="+payload["no-of-genes"]+",pattern='"+payload["1dregex-regex"]+"'"+")\n"

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
	
	code += "ga = GAEngine.GAEngine(factory=factory,population_size="+payload["population-size"]+",cross_prob="+payload["crossover-rate"]+",mut_prob="+payload["mutation-rate"]+",fitness_type="+str(fit_type)+",adaptive_mutation="+str(adaptive)+",use_pyspark="+str(pyspark)+")\n"
	
	i = 0
	while True:
		if "crossover-type"+str(i) in payload.keys():
			if(payload["crossover-type"+str(i)] != "custom"):
				code += "ga.addCrossoverHandler(Utils.CrossoverHandlers."+payload["crossover-type"+str(i)]+","+payload["crossover-weight"+str(i)]+")\n"
			else:
				cleaned = unquote(payload["custom-crossover"+str(i)])
				custom_name = cleaned[cleaned.find("def ")+4:]
				custom_name = custom_name[:custom_name.find("(")]
				precode += cleaned + "\n"
				if(unquote(payload["crossover-extra-data"+str(i)]).strip() != "#Enter data here" and payload["crossover-extra-data"+str(i)] != ''):
					datas = unquote(payload["crossover-extra-data"+str(i)]).split('\r\n')
					while(datas[-1].strip() == ''):
						datas = datas[:len(datas)-1]
					datas_string = ""
					for x in datas:
						precode += x +"\n"
						datas_string += "," + x[:x.find("=")].strip()

					code += "ga.addCrossoverHandler("+custom_name+","+payload["crossover-weight"+str(i)]+datas_string+")\n"
				else:
					code += "ga.addCrossoverHandler("+custom_name+","+payload["crossover-weight"+str(i)]+")\n"
			i+=1
		else:
			break

	i = 0
	while True:
		if "mutation-type"+str(i) in payload.keys():
			if(payload["mutation-type"+str(i)] != "custom"):
				code += "ga.addMutationHandler(Utils.MutationHandlers."+payload["mutation-type"+str(i)]+","+payload["mutation-weight"+str(i)]+")\n"
			else:
				cleaned = unquote(payload["custom-mutation"+str(i)])
				custom_name = cleaned[cleaned.find("def ")+4:]
				custom_name = custom_name[:custom_name.find("(")]
				precode += cleaned + "\n"
				if(unquote(payload["mutation-extra-data"+str(i)]).strip() != "#Enter data here" and payload["mutation-extra-data"+str(i)] != ''):
					datas = unquote(payload["mutation-extra-data"+str(i)]).split('\r\n')
					while(datas[-1].strip() == ''):
						datas = datas[:len(datas)-1]
					datas_string = ""
					for x in datas:
						precode += x +"\n"
						datas_string += "," + x[:x.find("=")].strip()

					code += "ga.addMutationHandler("+custom_name+","+payload["mutation-weight"+str(i)]+datas_string+")\n"
				else:
					code += "ga.addMutationHandler("+custom_name+","+payload["mutation-weight"+str(i)]+")\n"
			i+=1
		else:
			break
	

	if(payload["selection-type"] != "custom"):
		code += "ga.setSelectionHandler(Utils.SelectionHandlers."+payload["selection-type"]+")\n"
	else:
		cleaned = unquote(payload["custom-selection"])
		custom_name = cleaned[cleaned.find("def ")+4:]
		custom_name = custom_name[:custom_name.find("(")]
		precode += cleaned + "\n"
		if(unquote(payload["selection-extra-data"]).strip() != "#Enter data here" and payload["selection-extra-data"] != ''):
			datas = unquote(payload["selection-extra-data"]).split('\r\n')
			while(datas[-1].strip() == ''):
				datas = datas[:len(datas)-1]
			datas_string = ""
			for x in datas:
				precode += x +"\n"
				datas_string += "," + x[:x.find("=")].strip()

			code += "ga.setSelectionHandler("+custom_name + datas_string +")\n"
		else:
			code += "ga.setSelectionHandler("+custom_name+")\n"

	

	if(payload["fitness"] != "custom"):
		code += "ga.setFitnessHandler(Utils.Fitness."+payload["fitness"]+")\n"
	else:
		cleaned = unquote(payload["custom-fitness"])
		custom_name = cleaned[cleaned.find("def ")+4:]
		custom_name = custom_name[:custom_name.find("(")]
		precode += cleaned + "\n"
		if(unquote(payload["extra-data"]).strip() != "#Enter data here" and payload["extra-data"] != ''):
			datas = unquote(payload["extra-data"]).split('\r\n')
			while(datas[-1].strip() == ''):
				datas = datas[:len(datas)-1]
			datas_string = ""
			for x in datas:
				precode += x +"\n"
				datas_string += "," + x[:x.find("=")].strip()

			code += "ga.setFitnessHandler("+custom_name + datas_string +")\n"
		else:
			code += "ga.setFitnessHandler("+custom_name+")\n"

	# code += "ga.evolve("+payload["no-of-evolutions"]+")\n"
	# Take care of pyspark flag
	print()
	print("precode ---> \n",precode)
	print("code ---> \n",code)
	code = precode + code
	print("complete code ---> \n",code,"\n*******")
	print()
	exec(code,globals())

	print(ga)
	print(ga.calculateFitness([1,2]))
	ga.evolve(1)
	print('swah')
	return jsonify({'Best-Fitnesses':ga.fitness_dict[:10]})
	#return render_template("features/generations.html", fitness_dict=ga.fitness_dict[:10])

@app.route('/ga_evolve')
def ga_evolve():
	#print('HERE',data)
	ga.continue_evolve(1)

	return jsonify({'Best-Fitnesses':ga.fitness_dict[:10]})

@app.route('/get_file/<path:path>')
def get_file(path):
    return send_from_directory('static/uploads/', path, as_attachment=True)


@app.route("/downloadCode",methods=["POST"])
def downloadCode():
	return redirect(url_for("codeDownload",
						filename=session.get("pattern") + session.get("fileType"),
						patternType=session.get("pattern"),
						fileType=session.get("fileType")))



app.run()
