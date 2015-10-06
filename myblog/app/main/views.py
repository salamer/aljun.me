from flask import jsonify,render_template, redirect, url_for, abort, flash, request,current_app, make_response
from flask.ext.login import login_required, current_user
from . import main
from .. import db
from ..models import User,Post,Category,Like
from .forms import SearchForm,PostForm,LoginForm,EditForm
from flask.ext.login import login_user,logout_user,login_required

PER_POSTS_PER_PAGE=8


@main.route('/',methods=['GET',"POST"])
def index():

	form=LoginForm()
	if form.validate_on_submit():
		user=User.query.filter_by(email=form.email.data).first()
		if user is not None and user.verify_password(form.password.data):
			login_user(user,form.remember_me.data)
			return redirect(url_for('.index'))
		else:
			flash('invalid username or password')

	page=request.args.get('page',1,type=int)

	
	pagination=Post.query.order_by(Post.timestamp.desc()).paginate(
		page,per_page=PER_POSTS_PER_PAGE,error_out=False)
	posts=pagination.items
	categorys=Category.query.order_by(Category.count)[::-1]


	return render_template('index.html',posts=posts,pagination=pagination,categorys=categorys)

@main.route('/category/<tag>',methods=['GET'])
def category(tag):
	
	category=Category.query.filter_by(tag=tag).first()
	posts=category.posts
#	pagination=post.paginate(
#		page,per_page=PER_POSTS_PER_PAGE,error_out=False)
#	the_post=pagination.items
	return render_template("category_search.html",posts=posts)
	

@main.route('/post/<int:index>',methods=['GET'])
def post(index):
	post=Post.query.get_or_404(index)
	return render_template("post.html",post=post)

@main.route('/',methods=['GET','POST'])
def write():
	form=PostForm()
	the_category=Category.query.all()
	if form.validate_on_submit():
		
		category=Category.query.filter_by(tag=form.category.data).first()
		if category is None:
			category=Category(tag=form.category.data,count=1)
		else:
			category.count=int(category.count)+1
		post=Post(
			title=form.title.data,
			body=form.body.data,
			summury=form.summury.data,
			category=category
		)
		
		db.session.add(category)
		db.session.add(post)
		db.session.commit()
		
		flash("ok")
		return redirect(url_for('.index'))

	return render_template("write.html",form=form,the_category=the_category)



@main.route('/logout',methods=['GET'])
@login_required
def logout():
	logout_user()
	flash("you have been logged out")
	return redirect(url_for('.index'))

@main.route('/about',methods=['GET'])
def about_website():
	liked=Like.query.get_or_404(1)
	return render_template('about.html',liked=liked)


#@main.route('/login',methods=['GET','POST'])
#def login():
#    form=LoginForm()
 #   if form.validate_on_submit():
 #       user=User.query.filter_by(email=form.email.data).first()
 #       if user is not None and user.verify_password(form.password.data):
  #          login_user(user,form.remember_me.data)
 #           return redirect('.index')
 #       flash('invalid usernamen or password')
#    return render_template('login.html',form=form)

@main.route('/',methods=['GET','POST'])
def edit(index):
	post=Post.query.get_or_404(index)
	form=EditForm()
	if form.validate_on_submit():
		post.title=form.title.data
		post.body=form.body.data
		post.summury=form.summury.data
		db.session.add(post)
		return redirect(url_for('.index'))
	form.title.data=post.title
	form.body.data=post.body
	form.summury.data=post.summury
	return render_template('edit.html',form=form)

@main.route('/like')
def like():
	like=Like.query.get_or_404(1)
	like.like_count=int(like.like_count)+1
	db.session.add(like)
	db.session.commit()
	liked=like.like_count
	return jsonify({"liked":liked})


@main.app_errorhandler(404)
def page_not_found(error):
	return render_template("404.html"),404
