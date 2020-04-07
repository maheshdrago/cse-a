from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import FileField,SubmitField,SelectField


class Gallery(FlaskForm):
    file = FileField('Image',validators=[FileAllowed(['jpg','png','pdf'])])
    submit = SubmitField('upload')
    options = SelectField('Folder',choices=[('image','image'),('pdf','pdf')])
