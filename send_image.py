from flask import Flask, send_file, Response, render_template
from flask_hot_reload import HotReload
import os

app = Flask(__name__)

hot_reload = HotReload(app, 
    includes=[
        'templates',  # template directory
        '.'          # current directory
    ],
    excludes=[
        '__pycache__',
        'node_modules',
        '.git',
        'tmp'
    ]
)

# Define paths to your images
image_paths = {
    'output': "output.gif",
    'banner': "banner.png",
    'qr': "qr.png"
}

def set_banner(path):
    image_paths['banner'] = path

@app.route('/')
def index():
   return render_template('index.html')

@app.route('/output')
def serve_output():
    return send_file(image_paths['output'], mimetype='image/gif')

@app.route('/banner')
def serve_banner():
    return send_file(image_paths['banner'], mimetype='image/png')

@app.route('/qr')
def serve_qr():
    return send_file(image_paths['qr'], mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
