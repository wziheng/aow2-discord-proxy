from flask import Flask,request,render_template,jsonify,Response
from requests import post

app = Flask(__name__,static_folder="static")
SITE_NAME = 'https://discord.com/'

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
		print(path)
		data = request.get_json()
		url = SITE_NAME + path
		resp = post(url,data=data)
		return Response(resp.text,status=resp.status_code)

#def proxy(path):
#	return (f'{SITE_NAME}{path}').content

#if __name__ == '__main__':
#	app.run(port=80,debug=True)
