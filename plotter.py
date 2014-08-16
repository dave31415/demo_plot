#!/usr/bin/env python2
'''Serving dynamic images with matplotlib (using flask).

The data is served inside the <img ...> tag, no need for extra resource
handler.
'''

# No windows should pop up in a web server
import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import numpy as np
from cStringIO import StringIO

from flask import Flask,request, g, url_for, render_template,jsonify
app = Flask(__name__)

import vincent

WIDTH = 600
HEIGHT = 300

def get_data(period):
    x = np.linspace(-10, 10, 1000)
    y=np.sin(2*np.pi*x/period)
    z=np.cos(2*np.pi*x/period)
    data={'x':x,'y':y,'z':z}
    return data

#vincent d3 plotting
@app.route("/data/multiline",methods=['POST','GET'])
def data_multiline():
    period = request.args.get('period',9)
    print period
    print request.args
    data=get_data(float(period))
    return vincent.Line(data, width=WIDTH, height=HEIGHT, iter_idx=('x')).to_json()

#matplotlib plotting
@app.route("/",methods=['POST','GET'])
def index():
    period=float(request.form.get('period', 4.0))
    frequency=1.0/period

    # Plot sin and cos between -10 and 10 (1000 points)
    fig = plt.figure(figsize=(6,4))
    ax = fig.add_subplot(1, 1, 1)
    
    data=get_data(period)
    x=data['x']
    y=data['y']
    z=data['z']
    
    ax.plot(x, y, label='sin(x)')
    ax.plot(x, z, label='cos(x)')
    ax.legend()

    # Encode image to png in base64
    io = StringIO()
    fig.savefig(io, format='png')
    data = io.getvalue().encode('base64')
        
    return render_template('main.html',data=data,period=period,frequency=frequency)

@app.route('/_add_numbers')
def add_numbers():
    a = request.args.get('a', 1, type=int)
    b = request.args.get('b', 1, type=int)
    res= np.sin(a)**2 + np.cos(b)**2
    return jsonify(result=res)




if __name__ == '__main__':
    app.run(debug=True,port=5001)
