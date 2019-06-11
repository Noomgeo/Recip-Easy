from flask import Flask
from flask import flash, render_template, request, url_for, session, redirect

from auth import Auth
from recipes import Recipes

app = Flask(__name__)
app.secret_key = b'aj(>,m87hJn9+-alkjns*jkj90($'

@app.route("/login/", methods=["POST", "GET"])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    if request.method == 'POST':
        username = request.form.get('username', None)
        password = request.form.get('password', None)
        auth = Auth()
        if auth.login(username, password):
            return redirect(url_for('show_recipes'))

    flash('Sorry! Could not log you in')
    return render_template('login.html')

def isloggedin():
    return 'username' in session

@app.route("/sign-up/", methods=["POST", "GET"])
def sign_up():
    if request.method == 'GET':
        return render_template('sign-up.html')

    username = request.form.get('username', None)
    password = request.form.get('password', None)
    password2 = request.form.get('password2', None)
    auth = Auth()
    if auth.has_user(username):
        flash('Sorry! This username already exists.')
        return render_template('sign-up.html')
    elif password == password2:
        auth.create_user(username, password)
        return redirect(url_for('show_recipes'))
    else:
        flash('Passwords do not match!')
        return render_template('sign-up.html')

@app.route("/logout/")
def logout():
    auth = Auth()
    auth.logout()
    flash('You were logged out')
    return redirect(url_for('show_recipes'))

@app.route("/")
def index():
    return render_template('login.html')

@app.route("/recipes/")
def show_recipes():
# If logged in, show recipes for the current user.

# Otherwise, redirect to the Login page.

#     if auth.is_logged_in():
        return render_template('recipes.html')

@app.route("/recipes/new/", methods=['GET', 'POST'])
def add_recipe():
    '''If request method is GET, load the 'add recipe' page.
    If request method is POST:
      1. Get all posted form data
      2. Get ID of currently logged-in user
      3. Call the relevant function of the Recipes class to add/create
         a new record in the recipes table. Pass in the relevant 
         information as arguments to the function.
      4. Redirect to the Recipes (listing) page.'''
    if request.method == 'GET':
        return render_template('add_recipe.html')

    elif request.method == 'POST':
        title = request.form.get('recipe-title')
        image = request.form.get('recipe-image')
        category = request.form.get('recipe-category')
        description = request.form.get('recipe-description')
        ingredients = request.form.get('recipe-ingredients')

        auth = Auth()
        user = auth.get_current_user()
        user_id = user[0]

        new_recipe = {
            'title': title,
            'image_URL': image,
            'category': category,
            'description': description,
            'ingredients': ingredients,
        }

        recipe = Recipes()
        recipe.add_recipe(new_recipe, user_id)
        return redirect (url_for('show_recipes'))


@app.route("/recipes/<int:recipe_id>/")
def show_recipe(recipe_id):
    '''Show the recipe that matches the given recipe ID.'''


@app.route("/recipes/delete/<int:recipe_id>/")
def delete_recipe(recipe_id):
    auth = Auth()
    user = auth.get_current_user()
    user_id = user[0]
    recipe = Recipes()
    recipe.delete_recipe(recipe_id, user_id)
    return redirect(url_for('show_recipes'))
    # else:
    #     flash('This is not your recipe to delete')
    #     return redirect(url_for('show_recipe', recipe_id=recipe_id))


