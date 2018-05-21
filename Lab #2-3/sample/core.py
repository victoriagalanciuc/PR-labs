
import requests
import csv
import json
import time
#import xmltodict
import xml.etree.ElementTree
from threading import Thread 
from itertools import chain

Devices = {
    '0' : "Temperature",
    '1' : "Humidity",
    '2' : "Motion",
    '3' : "Alien Presence", 
    '4' : "Dark Matter",
    '5' : "Top Secret"}

URL = "http://desolate-ravine-43301.herokuapp.com"
RESULT = {"ID":[],"TYPE":[],"VALUE":[]}


####### OBTAINING URL LIST #######
def request_secret_key(url):
	# creating a response object 'request_response' which will store the request-response
	request_response = requests.post(url) # <Response [200]>
	# reading the content of the server's response (json response content)
	response_content = request_response.json() #u'path': u'/ro', u'method': u'GET'
	headers = request_response.headers  
	secret_key = headers['Session']
	secret_key_header = { "Session" : secret_key }
	urls_number = len(response_content)
	urls_list = []
	for i in range(urls_number):
		urls_list.append(url+response_content[i]["path"])
	return urls_list, response_content, urls_number, secret_key_header


####### PARSING DATA ACCORDING TO FORMAT #######
def parse_data(url):
	result = requests.get(url, headers=secret_key_header)   
	value_format = result.headers['Content-Type']
	if (value_format == "Application/json"):
		data = result.json()
		for key in data:
		    if key == "@id":
		        RESULT["ID"].append([data.get(key)])  
		    if key == "type":
		        RESULT["TYPE"].append([data.get(key)])   
		    if key == "value":
		        RESULT["VALUE"].append([data.get(key)]) 

	elif (value_format == "Application/xml"):
		data = xmltodict.parse(result.text)["device"]
		for key in data:
			if key == "@id":
				OUTPUT["ID"].append([data.get(key)])  
			if key == "type":
				OUTPUT["TYPE"].append([data.get(key)])   
			if key == "value":
				OUTPUT["VALUE"].append([data.get(key)])  

	elif (value_format == "text/csv"):
		d = {'device_id':[],
	     	'sensor_type':[],
	     	'value':[]}
		reader = csv.DictReader(result.text.splitlines())        
		for row in reader:
			for key in row:
				d[key].append(row[key])        
		data = d
		for key in data:
		    if key == "device_id":
		        RESULT["ID"].append(data.get(key))  
		    if key == "sensor_type":
		        RESULT["TYPE"].append(data.get(key)) 
		    if key == "value":
		        RESULT["VALUE"].append(data.get(key)) 

####### REQUESTING DATA FROM ALL DEVICES #######
def parallel_requests(url):
	for url in urls_list:
		threads = []
		threads.append(Thread(target=parse_data, args=(url,)))
		for thread in threads:
			thread.start()
		for thread in threads:
			thread.join()   

            
####### DATA AGGREGATION #######
def aggregate_data():
	id_list = list(chain.from_iterable(RESULT["ID"]))	
	type_list = list(chain.from_iterable(RESULT["TYPE"]))
	value_list = list(chain.from_iterable(RESULT["VALUE"]))

	data = {"ID":id_list,"TYPE":type_list,"VALUE":value_list}
	print data
	print("\n- RESULTS -")
	for i in range(len(Devices)):
		t=0
		print Devices[str(i)],": " #device name
		for j in data["TYPE"]:
			if j == str(i) or j==i: #ordering data by device type
				print "Device \t",data["ID"][t],"\t",data["VALUE"][t]
		t+=1 


urls_list, response_content, urls_number, secret_key_header = request_secret_key(URL)
parallel_requests(URL)
aggregate_data()