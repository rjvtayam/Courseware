from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, TextAreaField, SubmitField, DateTimeField
from wtforms.validators import DataRequired

class AssignmentForm(FlaskForm):
    title = StringField('Assignment Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    due_date = DateTimeField('Due Date', format='%Y-%m-%d %H:%M', validators=[DataRequired()])
    materials = FileField('Upload Materials', validators=[
        FileAllowed(['pdf', 'doc', 'docx', 'txt', 'zip'], 'Only documents allowed!')
    ])
    submit = SubmitField('Create Assignment')

class SubmissionForm(FlaskForm):
    file = FileField('Upload Your Work', validators=[
        FileRequired(),
        FileAllowed(['pdf', 'doc', 'docx', 'txt', 'zip'], 'Only documents allowed!')
    ])
    submit = SubmitField('Submit Work')

class CommentForm(FlaskForm):
    content = TextAreaField('Add a comment', validators=[DataRequired()])
    submit = SubmitField('Post Comment')