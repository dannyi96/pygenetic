#from server.flaskr import app

from flask import Flask, render_template, request, redirect, url_for, session, jsonify, send_from_directory, make_response, Response
from werkzeug import secure_filename
from urllib.parse import unquote
import os
import datetime
import json
import sys
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import gc
import pickle
from io import BytesIO

app = Flask(__name__)
persistent_store = {}

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
	payload = request.form
	precode = "import GAEngine\nimport Utils\nimport ChromosomeFactory\n"
	for i in payload:
		print(payload[i])

	print("Payload Data: ", payload)

	if(payload["gene-generation"]=="1drange"):
		if(payload["1drange-duplicate"]=="yes"):
			duplicates=True
		elif(payload["1drange-duplicate"]=="no"):
			duplicates=False
		print(">>> str(duplicates) is ",str(duplicates))
		code = "factory = ChromosomeFactory.ChromosomeRangeFactory(noOfGenes="+payload["no-of-genes"]+",minValue="+payload["1drange-min"]+",maxValue="+payload["1drange-max"]+",duplicates="+str(duplicates)+")\n"
	elif(payload["gene-generation"]=="1dregex"):
		code = "factory = ChromosomeFactory.ChromosomeRegexFactory(data_type="+payload["1dregex-datatype"]+",noOfGenes="+payload["no-of-genes"]+",pattern='"+payload["1dregex-regex"]+"'"+")\n"
	elif(payload["gene-generation"]=="custom"):
		cleaned = unquote(payload["custom-chromosome"])
		code = cleaned + "\n"

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
	return Response(code,mimetype="text/plain",headers={"Content-Disposition":"attachment;filename=ga.py"})

@app.route('/ga_init',methods=['POST'])
def ga_init():
	import sys
	sys.path.insert(0, '../pyGenetic')

	payload = request.form
	precode = "import GAEngine\nimport Utils\nimport ChromosomeFactory\n"
	for i in payload:
		print(payload[i])

	print("Payload Data: ", payload)

	if(payload["gene-generation"]=="1drange"):
		if(payload["1drange-duplicate"]=="yes"):
			duplicates=True
		elif(payload["1drange-duplicate"]=="no"):
			duplicates=False
		print(">>> str(duplicates) is ",str(duplicates))
		code = "factory = ChromosomeFactory.ChromosomeRangeFactory(noOfGenes="+payload["no-of-genes"]+",minValue="+payload["1drange-min"]+",maxValue="+payload["1drange-max"]+",duplicates="+str(duplicates)+")\n"
	elif(payload["gene-generation"]=="1dregex"):
		code = "factory = ChromosomeFactory.ChromosomeRegexFactory(data_type="+payload["1dregex-datatype"]+",noOfGenes="+payload["no-of-genes"]+",pattern='"+payload["1dregex-regex"]+"'"+")\n"
	elif(payload["gene-generation"]=="custom"):
		cleaned = unquote(payload["custom-chromosome"])
		code = cleaned + "\n"

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
	

	if(payload["selection-type"] == "tournament"):
		code += "ga.setSelectionHandler(Utils.SelectionHandlers."+payload["selection-type"]+","+payload["tournament-size"]+")\n"
	elif(payload["selection-type"] != "custom"):
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

	print()
	print("precode ---> \n",precode)
	print("code ---> \n",code)
	code = precode + code
	print("complete code ---> \n",code,"\n*******")
	print()
	code += "ga.evolve(1)"
	print(globals())
	print(globals().values())
	exec(code,globals())
	print(globals().values())
	print(ga)
	print(ga.calculateFitness([1,2]))
	print('swah')
	#ga_list.append(ga)
	response = jsonify({'Best-Fitnesses':ga.fitness_mappings[:10]})
	print(id(ga))
	print(type(id(ga)))
	print(str(id(ga)))
	response.set_cookie('ga_object',str(id(ga)))
	persistent_store[str(id(ga))] = ga
	print(str(id(ga)))
	print(persistent_store)
	return response

@app.route('/ga_evolve')
def ga_evolve():
	print()
	print('b',request.cookies.get('ga_object'))
	ga = persistent_store[(request.cookies.get('ga_object'))]
	print(persistent_store)
	print(ga)
	ga.continue_evolve(1)
	for key in persistent_store:
		print( key , persistent_store[ key ])
	return jsonify({'Best-Fitnesses':ga.fitness_mappings[:10]})

@app.route('/plot_fitness_graph')
def plot_fitness_graph():
	ga = persistent_store[(request.cookies.get('ga_object'))]
	print(persistent_store)
	print(ga)
	print(ga.statistics.statistic_dict['best-fitness'])
	print(persistent_store)
	del persistent_store[request.cookies.get('ga_object')]
	print(persistent_store)
	graph = ga.statistics.plot_statistics(['best-fitness','worst-fitness','avg-fitness'])
	canvas = FigureCanvas(graph)
	output = BytesIO()
	canvas.print_png(output)
	response = make_response(output.getvalue())
	response.mimetype = 'image/png'
	return response

@app.route("/downloadCode",methods=["POST"])
def downloadCode():
	return redirect(url_for("codeDownload",
						filename=session.get("pattern") + session.get("fileType"),
						patternType=session.get("pattern"),
						fileType=session.get("fileType")))

def object_by_id(id_):
    for obj in globals().values():
        if id(obj) == id_:
            return obj
    raise Exception("No found")

app.run()