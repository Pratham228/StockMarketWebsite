from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from login import db
from login.models import Post
from login.posts.forms import PostForm

posts = Blueprint('posts',__name__)

@posts.route('/post/new',methods=['GET','POST'])
@login_required
def new_post():
    form  = PostForm()
    if form.validate_on_submit():
        post = Post(name=form.name.data,author=form.author.data,user_id=current_user.id)
        db.session.add(post)
        db.session.commit()
        flash('Your Post has been created','success')
        return redirect(url_for('main.home'))
    return render_template('create_post.html',title='New Post',form=form,legend = 'New Post')

@posts.route('/post/<int:post_id>')
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html',title=post.name,post=post)

    
@posts.route('/post/<int:post_id>/update',methods=['GET','POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.user_id != current_user.id:
        abort(403)
    form =PostForm()
    if form.validate_on_submit():
        post.name = form.name.data
        post.author = form.author.data
        db.session.commit()
        flash("Your post has been updated",'success')
        return redirect(url_for('posts.post',post_id=post.id))
    elif request.method == 'GET':
        form.name.data= post.name
        form.author.data= post.author
    return render_template('create_post.html',title='Update Post',form=form,legend = 'Update Post')

@posts.route('/post/<int:post_id>/delete',methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.user_id != current_user.id:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash("Your post has been deleted",'success')
    return redirect(url_for('main.home'))
