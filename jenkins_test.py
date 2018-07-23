#!/usr/bin/python3 

import os
import requests
from requests.auth import HTTPBasicAuth
import json
import sqlite3 as sqlite
from datetime import datetime

#configurations
db_path 		= './json.db'
jenkins_url 	= 'http://ci.hng.tech/api/json'
status_codes 	= {"notbuilt" : -1 , "red": 0, "blue" : 1, "undefined" : 9 }
jenkins_user	= ""
jenkins_pass 	= ""

#Create Connection to sqlite database first
try:
	conn = sqlite.connect(db_path)

	#create jobs table if it does not exist 
	sql = """CREATE TABLE IF NOT EXISTS jobs (
		id integer PRIMARY KEY,
		job_name varchar(200) NOT NULL,
		status tinyint(1) NOT NULL,
		created_at datetime NOT NULL
	) """
	cursor = conn.cursor()
	cursor.execute(sql)
except Error as e:
	print(e)

#Fetch Jenkins data
get_payload = requests.get(jenkins_url, auth=HTTPBasicAuth(jenkins_user, jenkins_pass))
data = get_payload.json()

for job in data['jobs']:
	#parse content 
	job_status = job['color']
	if job_status not in status_codes:
		job_status = "undefined"

	payload = [None, job['name'], job_status, datetime.now()]
	insertion_sql = "INSERT INTO jobs(id, job_name, status, created_at) VALUES (?,?,?,?)"

	try:
		#write to sqlite DB 
		cursor.execute(insertion_sql, payload)
		conn.commit()
	except Exception as e :
		print(e)


print("Jobs have been fetched and inserted")
	
