from flask import render_template, redirect, session, request, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.recipe import Recipe

@app.route('/dashboard')
def dashboard():
    if 'user_id' in session:
        user_data = {
            'id': session['user_id']
        }
        user = User.get_by_id(user_data)
        recipes = Recipe.get_all()
        return render_template('dashboard.html', user=user, recipes=recipes)
    else:
        return redirect('/')
    
@app.route('/recipes/<int:id>')
def show_recipe(id):
    if 'user_id' in session:
        user_data = {
            'id': session['user_id']
        }
        user = User.get_by_id(user_data)
        data = { 'id': id }
        theRecipe = Recipe.get_one(data)
        return render_template('show_recipe.html', recipe=theRecipe, user=user)
    else:
        return redirect('/')

@app.route('/recipes/create')
def create_recipe():
    if 'user_id' in session:
        user_data = {
            'id': session['user_id']
        }
        user = User.get_by_id(user_data)
        return render_template('add_recipe.html', user=user)
    else:
        return redirect('/')

@app.route('/recipes/add', methods=['POST'])
def add_recipe():
    if not Recipe.validate_recipe(request.form):
        return redirect('/recipes/create')
    Recipe.save(request.form)
    return redirect('/dashboard')

@app.route('/recipes/<int:id>/edit')
def edit_recipe(id):
    if 'user_id' in session:
        user_data = {
            'id': session['user_id']
        }
        user = User.get_by_id(user_data)
        data = { 'id': id }
        theRecipe = Recipe.get_one(data)
        return render_template('edit_recipe.html', user=user, recipe=theRecipe)
    else:
        return redirect('/')

@app.route('/recipes/<int:id>/update', methods=['POST'])
def update_recipe(id):
    Recipe.update(request.form)
    return redirect(f'/recipes/{id}')

@app.route('/recipes/<int:id>/delete')
def delete_recipe(id):
    if 'user_id' in session:
        user_data = {
            'id': session['user_id']
        }
        user = User.get_by_id(user_data)
        data = { 'id': id }
        Recipe.delete(data)
        return redirect('/dashboard')
    else:
        return redirect('/')