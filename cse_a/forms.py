from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import FileField,SubmitField,TextField


class Gallery(FlaskForm):
    image = FileField('Image',validators=[FileAllowed(['jpg','png'])])
    delete = TextField('delete')
    submit = SubmitField('upload')
