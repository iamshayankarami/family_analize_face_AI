from flask import Flask, request
import numpy as np
import sys

app = Flask(__name__)

@app.route('/')
def main():
    return"hello"

if __name__ == "__main__":
     app.run()
