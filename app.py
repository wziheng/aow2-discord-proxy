from flask import Flask,request
from requests import get

app = Flask(__name__)
SITE_NAME = 'https://discord.com/'

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def proxy(path):
	print(path)
	return get(f'{SITE_NAME}{path}').content

#if __name__ == '__main__':
#	app.run(port=80,debug=True)
