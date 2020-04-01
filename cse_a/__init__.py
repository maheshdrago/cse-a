from flask import Flask



app = Flask(__name__)

app.config['SECRET_KEY']='newsecretkey'




from cse_a.views import core



app.register_blueprint(core)
