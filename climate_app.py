#import Flask
from flask import Flask

#Create an app, being sure to pass __name__
app = Flask(__name__)

@app.route("/")
def home():
    return(f"Welcome to Surfs Up! <br/>"
          f"Available routes:")

#@app.route("/precipitation")
#def precipitation():
#    return(
           

if __name__ == "__main__":
    app.run(debug=True)