from flask import Flask,request,render_template,jsonify
from requests import get

app = Flask(__name__)
SITE_NAME = 'https://discord.com/'

@app.route("/heartbeat")
def heartbeat():
    return jsonify({"status": "healthy"})

@app.route('/')
def homepage():
	return render_template('templates/index.html')
@app.route('/<path:path>',methods=["GET","POST"])
def proxy(path):
	if request.method == "GET":
		return (f'{SITE_NAME}{path}').content

#def proxy(path):
#	return (f'{SITE_NAME}{path}').content

#if __name__ == '__main__':
#	app.run(port=80,debug=True)
