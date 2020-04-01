from cse_a import app




app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False

if __name__ == '__main__':
    app.run()
