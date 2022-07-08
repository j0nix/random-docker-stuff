import urllib

from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    r = urllib.urlopen("http://j0nixService2:80")
    #return "<!-- request from service2service -->\n" + r.read()
    return "<html><head><title>Service2service</title></head><body><h1>Request from service2service to http://j0nixService2</h1><pre>" + r.read() + "</pre></body></html>"
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
