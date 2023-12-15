#!/usr/bin/python3

import os
from flask import Flask, after_this_request, render_template, send_file
from src.http_util import HttpUtils


app = Flask(__name__)

base_url = 'http://localhost:2375'
http_utils = HttpUtils(base_url)

@app.route('/')
def index():

   images = http_utils.get_json_from_endpoint("images/json")

   containers = http_utils.get_json_from_endpoint("containers/json?all=true")

   return render_template("index.html",images=images,containers=containers)



@app.route('/container/<container_id>')
def inspect_container(container_id):

   # Fetch detailed data
   endpoint = "containers/" + container_id + "/json" 
   container_data = http_utils.get_json_from_endpoint(endpoint)


   # Fetch processes data
   endpoint = "containers/" + container_id + "/top" 
   container_processes = http_utils.get_json_from_endpoint(endpoint)


   # Fetch file system changes
   endpoint = "containers/" + container_id + "/changes" 
   container_changes = http_utils.get_json_from_endpoint(endpoint)

   return render_template('container_inspection.html', container_data=container_data, container_processes=container_processes, container_changes=container_changes)


@app.route('/container/<container_id>/json')
def inspect_container_raw(container_id):

   # Fetch detailed data
   endpoint = "containers/" + container_id + "/json" 
   container_data = http_utils.get_json_from_endpoint(endpoint)

   return container_data



@app.route('/container/<container_id>/top')
def inspect_container_processes(container_id):

   # Fetch detailed data
   endpoint = "containers/" + container_id + "/top" 
   container_data = http_utils.get_json_from_endpoint(endpoint)

   print(container_data)
   return container_data


@app.route('/container/<container_id>/stats')
def inspect_container_stats(container_id):

   # Fetch detailed data
   endpoint = "containers/" + container_id + "/stats?stream=false" 
   container_data = http_utils.get_json_from_endpoint(endpoint)


   return container_data


@app.route('/container/<container_id>/export')
def inspect_container_export(container_id):

   # Fetch detailed data
   endpoint = "containers/" + container_id + "/export" 
   container_data = http_utils.download_tar_file(endpoint,"temp_file.tar")

   response = send_file("temp_file.tar", as_attachment=True)
   

   #Remove the temporary file
   @after_this_request
   def remove_temp_file(response):
      os.unlink("temp_file.tar")
      return response
   
   return response

# main driver function
if __name__ == '__main__':

   # run() method of Flask class runs the application 
   # on the local development server.
   app.run(host='0.0.0.0')
