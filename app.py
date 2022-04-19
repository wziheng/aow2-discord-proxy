from email import header
from flask import Flask,request,render_template,jsonify,Response
from numpy import number
from requests import post
from time import time

app = Flask(__name__,static_folder="static")
SITE_NAME = 'https://discord.com/'
channel_block = {}

@app.route("/heartbeat")
def heartbeat():
    return jsonify({"status": "healthy"})

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>',methods=['GET','POST'])
def proxy(path):
	if request.method == "GET":
		if path == '':
			return render_template('index.html')
		else:
			return Response("<h1> 404 Not Found! </h1>",status=404)
	elif request.method == "POST":
		channel_id = path[13:31]
		# if channel_id in channel_block:
		# 	print(time()-channel_block[channel_id])
		if not channel_id in channel_block or time() > channel_block[channel_id]:
			data = request.get_json()
			url = SITE_NAME + path
			resp = post(url,data=data)
			#useful_headers = ["X-RateLimit-Limit","X-RateLimit-Remaining","X-RateLimit-Reset","X-RateLimit-Reset-After","X-RateLimit-Bucket"]
			#for header in useful_headers:
			#	print(header,resp.headers[header])
			if resp.status_code == 429:
				channel_block[channel_id] = time()+float(resp.headers["Retry-After"])
			elif int(resp.headers["X-RateLimit-Remaining"]) == 0:
				time_reset = float(resp.headers["X-RateLimit-Reset"])
				time_reset_after = time()+float(resp.headers["X-RateLimit-Reset-After"])
				channel_block[channel_id] = max(time_reset,time_reset_after)
			return Response(resp.text,status=resp.status_code)
		else:
			return Response("403 Forbidden (Requests Exceeded)",status=403)
