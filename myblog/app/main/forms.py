from flask.ext.wtf import Form
from wtforms import StringField,TextAreaField,BooleanField,SelectField,SubmitField,PasswordField
from wtforms.validators import Required,Length,Regexp,Email
from wtforms import ValidationError
from flask.ext.pagedown.fields import PageDownField
from ..models import User

class SearchForm(Form):
	mater=StringField("what do you want?",validators=[Length(0,64)])

class PostForm(Form):
	title=StringField("TITLE",validators=[Required()])
	body=PageDownField("BODY",validators=[Required()])
	summury=PageDownField('SUMMURY',validators=[Required()])
	category=StringField("CATEGORY",validators=[Required()])
	submit=SubmitField('update')


class LoginForm(Form):
	email=StringField('Email',validators=[Required(),Length(1,64),Email()])
	password=PasswordField('password',validators=[Required()])
	remember_me=BooleanField('keep me logged in')
	submit=SubmitField('LOGIN')

class EditForm(Form):
	title=StringField("TITLE",validators=[Required()])
	body=PageDownField("BODY",validators=[Required()])
	summury=PageDownField('SUMMURY',validators=[Required()])
	
	submit=SubmitField('update')