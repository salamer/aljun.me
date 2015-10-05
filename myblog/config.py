import os

basedir=os.path.abspath(os.path.dirname(__file__))

class Config:
	SECRET_KEY = os.environ.get('SECRET_KEY') or ''
	SSL_DISABLE = False
	SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    	SQLALCHEMY_RECORD_QUERIES = True
	DEBUG=True
	SQLALCHEMY_DATABASE_URI=''

	@staticmethod
	def init_app(app):
		pass

