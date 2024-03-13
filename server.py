from flask_app import app

from flask_app.controllers import cars, renters, owners

if __name__=="__main__":     
    app.run(debug=True)  