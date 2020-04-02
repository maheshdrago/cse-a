
from flask import Blueprint,request,redirect,url_for
from flask import render_template,request
import os
from flask import current_app
from cse_a import app
from cse_a.models import Message,db
from PIL import Image
from cse_a.forms import Gallery


core = Blueprint('core',__name__)

@core.route('/')
def index():
    return render_template('index.html')

@core.route("/pccn")
def pccn():
    return render_template('pccn.html')

@core.route("/mc")
def mc():
    return render_template("mc.html")

@core.route("/cns")
def cns():
    return render_template("cns.html")

@core.route("/cd")
def cd():
    return render_template("cd.html")

@core.route("/wt")
def wt():
    return render_template("wt.html")

@core.route("/donate")
def donate():
    return render_template('donate.html')


@core.route('/contact',methods=['GET','POST'])
def contact():
    if request.method=="GET":

        return render_template('contact.html')
    else:
        name =  request.form['name']
        email = request.form['email']
        message = request.form['message']

        entry = Message(name,email,message)
        db.session.add(entry)
        db.session.commit()

        return render_template('feedback.html',name=name,email=email,message=message)

@core.route('/upcomingEvents')
def upcomingEvents():
    return render_template('blog.html')


@core.route('/about')
def about():
    return render_template('about.html')


@core.route('/gallery')
def gallery():
    images = os.listdir(os.path.join(app.static_folder, "images/gallery"))
    return render_template('gallery.html', images=images)


@core.route('/timeTable')
def timeTable():
    return render_template('how-it-works.html')


@core.route('/assignments')
def assignments():
    return render_template('blog-single.html')


@core.route('/upload',methods=['POST','GET'])
def upload():
    form = Gallery()
    if request.method=="POST":
        if form.validate_on_submit:
            if form.image.data:
                pic = form.image.data
                filename = pic.filename
                path = os.path.join(current_app.root_path,'static\images\gallery',filename)
                p = Image.open(pic)
                p.save(path)
                return render_template('upload.html',status=True,form=form)
    return render_template('upload.html',status=False,form=form)



@core.route('/delete',methods=['POST'])
def delete():
    image = request.form['image_name']
    path = os.path.join(current_app.root_path,'static\images\gallery',image)
    os.remove(path)
    return redirect(url_for('core.upload'))
