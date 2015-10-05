from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from markdown import markdown
import bleach

class User(db.Model):
	__tablename__="users"
	id=db.Column(db.Integer,primary_key=True)
	username=db.Column(db.String(64),unique=True,index=True)
	password_hash=db.Column(db.String(128))

	@property
	def  password(self):
	    raise AttributeError('password is not a readable attribute')

	@password.setter
	def password(self,password):
		self.password_hash=generate_password_hash(password)

	def verify_password(self,password):
		return check_password_hash(self.password_hash,password)
	

	def __repr__(self):
		return self.username

class Post(db.Model):
	__tablename__="posts"
	id=db.Column(db.Integer,primary_key=True)
	title=db.Column(db.String(64))
	body = db.Column(db.Text)
    	body_html = db.Column(db.Text)
    	summury=db.Column(db.Text)
    	summury_html=db.Column(db.Text)

	timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

	category_id=db.Column(db.Integer,db.ForeignKey('categorys.id'))

	@staticmethod
    	def on_changed_body(target, value, oldvalue, initiator):
        		allowed_tags = ['a', 'abbr', 'acronym', 'b', 'code', 'blockquote','em', 'i',
                        			'strong','li','ol','pre','strong','ul','h1','h2','h3','p']
        		target.body_html = bleach.linkify(bleach.clean(
            			markdown(value, output_format='html'),
           			 tags=allowed_tags, strip=True)
        		)

        		

    	@staticmethod
    	def on_changed_summury(target, value, oldvalue, initiator):
        		allowed_tags = ['a', 'abbr', 'acronym', 'b', 'code', 'blockquote','em', 'i',
                        			'strong','li','ol','pre','strong','ul','h1','h2','h3','p']
        		target.summury_html = bleach.linkify(bleach.clean(
            			markdown(value, output_format='html'),
           			 tags=allowed_tags, strip=True)
        		)


db.event.listen(Post.body, 'set', Post.on_changed_body)
db.event.listen(Post.summury, 'set', Post.on_changed_summury)

class Category(db.Model):
	__tablename__="categorys"
	id=db.Column(db.Integer,primary_key=True)
	tag=db.Column(db.String(64))
	count=db.Column(db.Integer)
	posts=db.relationship("Post",backref="category")

class Like(db.Model):
	__tablename__="Like"
	id=db.Column(db.Integer,primary_key=True)
	like_count=db.Column(db.Integer)