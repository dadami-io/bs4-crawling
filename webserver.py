from flask import Flask, render_template, send_file, request
from main import getImg
from main import getMusic

app = Flask(__name__, static_url_path='/static')


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/music')
def music():
    query=request.args.get('query', type=str)
    img=getMusic(query)
    return send_file(img, mimetype='image/png')



@app.route('/news')
def img():
    query=request.args.get('query', type=str)
    img=getImg(query)
    return send_file(img, mimetype='image/png')



app.run(host='0.0.0.0',port=4000,debug=False)

