import os
from flask import Flask, render_template, request, flash, redirect, session
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)

app.secret_key = os.environ