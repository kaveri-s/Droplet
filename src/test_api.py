from flask import Flask, flash,session, render_template, request, redirect, Response ,jsonify, json, url_for
from database import *

app = Flask(__name__)
app.secret_key = 'droplet'

if __name__ == '__main__':
# run!
    app.run(debug=True)