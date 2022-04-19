from flask import Flask,request,render_template,jsonify,Response
from numpy import number
from requests import post
from time import time

app = Flask(__name__,static_folder="static")
SITE_NAME = 'https://discord.com/'
CAN_SEND = {}

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
		if channel_id in CAN_SEND:
			print(time()-CAN_SEND[channel_id])
		if not channel_id in CAN_SEND or time() >= CAN_SEND[channel_id]:
			data = request.get_json()
			url = SITE_NAME + path
			resp = post(url,data=data)
			#useful_headers = ["X-RateLimit-Limit","X-RateLimit-Remaining","X-RateLimit-Reset","X-RateLimit-Reset-After","X-RateLimit-Bucket"]
			#for header in useful_headers:
			#	print(header,resp.headers[header])
			if resp.status_code == 429 or int(resp.headers["X-RateLimit-Remaining"]) == 0:
				CAN_SEND[channel_id] = float(resp.headers["X-RateLimit-Reset"])
			return Response(resp.text,status=resp.status_code)
		else:
			return Response("403 Forbidden (Requests Exceeded)",status=403)
