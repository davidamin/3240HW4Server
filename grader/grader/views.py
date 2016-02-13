from django.shortcuts import render, render_to_response, get_object_or_404
from django.template import Context, RequestContext, loader
from django.template.loader import get_template
from django.http import HttpResponse
from django.http import JsonResponse

from django.utils import dateparse

from datetime import datetime

from django.conf import settings

import os
import json
import logging
import subprocess
import threading

from django.core.files.base import ContentFile

class RunCmd(threading.Thread):
	def __init__(self, cmd, timeout):
		threading.Thread.__init__(self)
		self.cmd = cmd
		self.timeout = timeout
		self.results = b""

	def run(self):
		#self.p = subprocess.Popen(self.cmd, shell=True,stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
		self.p = subprocess.Popen(self.cmd, shell=True,stdout=subprocess.PIPE)
		self.p.wait()
		#self.results += self.p.stdout.read()
		self.results += self.p.communicate()[0]

	def Run(self):
		self.start()
		self.join(self.timeout)

		if self.is_alive():
			self.p.kill()      #use self.p.kill() if process needs a kill -9
			self.join()
		return self.results

def index(request):
	return HttpResponse('<html><title> 3240 HW4 Grading Site </title><body>Submit your HW4 script. This is <b> NOT </b> turning it in for grading. Use collab for that. This is just to test.<br />Again <b>WE DO NOT SAVE THESE, YOU STILL NEED TO SUBMIT TO COLLAB</b><form method="post" enctype="multipart/form-data" action="/test"><input type="file" name="code" /><input type="submit" name="submit" value="Upload" /></form></body></html>')

def test(request):
	BASE_PATH="C:\\Users\\User\\"
	name = request.FILES['code'].name
	file_content = ContentFile( request.FILES['code'].read() )
	now = "temp-" + datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
	#try:
	os.mkdir(os.path.join(BASE_PATH, str(now)))
	filename = os.path.join(BASE_PATH, str(now), name)
	fout = open(filename, 'wb+')
	for chunk in file_content.chunks():
		fout.write(chunk)
	fout.close()
	arg_string = "cp " + os.path.join(settings.BASE_DIR,"3240HW4Grader.py") + " " + os.path.join(BASE_PATH,str(now))
	arg_string += ";python3 " +os.path.join(BASE_PATH,str(now),"3240HW4Grader.py -d")
	results = RunCmd(arg_string, 60).Run()
	#subprocess.call("copy " + os.path.join(settings.BASE_DIR,"3240HW4Grader.py") + " " + os.path.join(BASE_PATH,str(now)), shell=True)
	#results = subprocess.check_output("py -3 " +os.path.join(BASE_PATH,str(now),"3240HW4Grader.py -d"), shell=True)
	#results = results.replace(b'\n',b'<br />')
	return HttpResponse(results)
	#except:
	#	return HttpResponse('File Upload Error: Please try again.')
	
	