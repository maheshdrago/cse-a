
from flask import Blueprint,request,redirect,url_for
from flask import render_template,request
import os
from flask import current_app
from cse_a import app
from cse_a.models import Message,db,Attendance,Cse_Gallery,Technical
from PIL import Image
from cse_a.forms import Gallery
import datetime
import boto3
import requests
import json

core = Blueprint('core',__name__)
s3 = boto3.client('s3', aws_access_key_id='AKIAURANAD5QSGAU4AO3', aws_secret_access_key='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')
bucket_name='cse-static-a'


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
    names = ['me1.png','devank.jpg','yashwanth.jpg','aswin.jpg']
    urls=[]
    for i in names:
        url = s3.generate_presigned_url(ClientMethod='get_object',
                                Params={
                                    'Bucket': bucket_name,
                                    'Key': 'developers/{}'.format(i),
                                },
                                ExpiresIn=3600)
        urls.append(url)

    return render_template('about.html',urls=urls)

@core.route('/attendance_add',methods=['POST','GET'])
def attendance_add():
    present = request.form['present']
    row = Attendance(present=present)
    db.session.add(row)
    db.session.commit()


    return redirect(url_for('core.attendance'))

@core.route('/gallery')
def gallery():
    urls=[]
    images = Cse_Gallery.query.all()
    for i in images:
        url = s3.generate_presigned_url(ClientMethod='get_object',
                                Params={
                                    'Bucket': bucket_name,
                                    'Key': 'Images/{}'.format(i.name),
                                },
                                ExpiresIn=3600)
        urls.append(url)


    return render_template('gallery.html', images=urls)


@core.route('/timeTable')
def timeTable():
    return render_template('timetable.html')


@core.route('/assignments')
def assignments():
    return render_template('blog-single.html')

@core.route('/attendance')
def attendance():
    date = datetime.datetime.now()
    a = Attendance.query.order_by(Attendance.date.desc())
    return render_template('attendance.html',a = a,date=date)

@core.route('/upload_gallery',methods=['POST','GET'])
def upload():
    try:
        error = None
        form = Gallery()
        if request.method=="POST":
            if form.validate_on_submit:
                if form.options.data=='image':
                    if form.file.data:
                        try:
                            file = form.file.data
                            filename = file.filename
                            image = Cse_Gallery(name=filename)
                            db.session.add(image)
                            db.session.commit()

                            s3.put_object(Body=file,
                                      Bucket=bucket_name,
                                      Key='Images/{}'.format(filename),

                                )
                            return("<h1>upload successful<h1>")
                        except Exception as e:
                            return (str(e))

                elif form.options.data=='pdf':
                    try:
                        pdf = form.file.data
                        filename = pdf.filename
                        s3.put_object(Body=pdf,
                                      Bucket=bucket_name,
                                      Key='pdfs/{}'.format(filename) )
                    except Exception as e:
                        return (str(e))


            return render_template('upload.html',form=form,error=error)
        return render_template('upload.html',form=form,error=error)
    except:
        error = 'Try again............'
        return render_template('upload.html',form=form,error=error)

@core.route('/challenge/<int:id>',methods=["POST","GET"])
def challenge(id):
    output = None
    code = None
    ele = Technical.query.filter_by(id=id).first()
    languages = {"ada": 53,"bash": 14, "brainfuck": 19, "c": 1,"clojure": 13,"cobol": 36, "coffeescript": 59, "cpp": 2, "cpp14": 58,
             "csharp": 9,"db2": 44,"elixir": 52, "erlang": 16, "fortran": 54,"fsharp": 33, "go": 21, "groovy": 31,
             "haskell": 12, "haxe": 69, "java": 3, "nodejs": 20,"julia": 57, "kotlin": 71, "lolcode": 38, "lua": 18,
             "maven": 45, "mysql": 10, "prolog": 64, "objectivec": 32, "ocaml": 23, "octave": 46, "oracle": 11,
             "pascal": 25, "perl": 6, "php": 7, "pypy": 61, "pypy3": 62,"python2": 5, "python3": 30, "r": 24, "racket": 49, "ruby": 8,
             "rust": 50, "d": 26, "sbt": 70,"scala": 15, "smalltalk": 39, "swift": 51, "tcl": 40, "text": 28,
             "tsql": 42, "visualbasic": 37, "whitespace": 41, "unlamda": 48
             }
    if request.method=='POST':
        def solve(code,input_,lang):

            content = {'content-type':'application/json'}
            if input_=='':
                input_=' '

            url = 'https://api.jdoodle.com/v1/execute'

            data = {
                            'script': code,
                            'language': lang,
                            'stdin':input_,
                            'versionIndex': '0',
                            'clientId': 'b294d436264a9f669f8e8810318c01c2',
                            'clientSecret': '90a81d009c2a15ed2d7603b671b36369495ff024f5f0b6cecc2b20d0b6d0019',
                }
            response = requests.post(url,data=json.dumps(data),headers=content)
            res=response.json()

            return res

        lang = request.form.get('lang')
        code = request.form.get('code')
        input_ = request.form.get('input')
        output = solve(code,input_,lang)
        return render_template("challenge.html",output=output,code=code,ele=ele,languages=languages)




    return render_template('challenge.html',ele=ele,languages=languages,output=output,code=code)


@core.route('/technical')
def technical():
    challenges = Technical.query.all()
    return render_template('technical.html',challenges=challenges)
