from flask import render_template, flash, redirect, session, url_for, request, g, render_template_string
from App import app, db
from .models import Ingredientlist, Categorylist, Supplierlist
from datetime import datetime
from .forms import AddIngredientForm, EditIngredientForm, AddCategoryForm, IngredientListForm, Release


@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    return render_template('index.html',
                           title='Home',
                           user='Philippe'
                            )


@app.route('/ingredients', methods=['GET', 'POST'])
def ingredient():
    form = IngredientListForm()
    if form.validate_on_submit():
        pass
        return redirect(url_for('database'))
    return render_template("ingredients.html",
                            action = 'Save',
                            title='List of Ingredients',
                            form = form
                          )


@app.route('/test', methods=['GET', 'POST'])
def test():
    form = Release()
    if form.validate_on_submit():
        # this generates the word doc
        document = Document()
        document.add_paragraph(form.paragraph.data)
        f = StringIO()
        document.save(f)
        length = f.tell()
        f.seek(0)
        return redirect(url_for('database'))
    return render_template('test_repeat.html', form=form)


@app.route('/recipe', methods=['GET', 'POST'])
def recipe():
    return render_template('recipe.html')

@app.route('/cost', methods=['GET', 'POST'])
def cost():
    return "True"

@app.route('/database', methods=['GET', 'POST'])
def database():
    #items = Ingredientlist.query.order_by(Categorylist.category_id).all()
    ingredients = Ingredientlist.query.order_by(Ingredientlist.category_id)
    return render_template('display_database.html',
                            title = 'List of all ingredients stored in the database',
                            ingredients = ingredients)


@app.route('/add_ingredient', methods=['GET', 'POST'])
def add_ingredient():
    form = AddIngredientForm()
    if form.validate_on_submit():
        if request.form['btn'] == "Add":
            datenow= datetime.utcnow()
            #print (str(form.category.data))
            if not form.purchaseDate.data:
                form.purchaseDate.data= datenow

            #Commit item to database (no check for the moment)
            #I will want to verify that it is not a doublon or things like that

            # Prepare insertion
            item = Ingredientlist(  ingredient = form.ingredient.data,
                                    category_id = Categorylist.GetCatID(str(form.category.data)),  # need to convert to string to make it work!
                                    supplier_id = Supplierlist.GetCatID(str(form.supplier.data)),
                                    bag_size = form.bag_size.data,
                                    bag_cost = form.bag_cost.data,
                                    unit = form.unit.data, ## look if really needed
                                    cost_unit = Ingredientlist.CostPerUnit(form.bag_size.data,form.bag_cost.data),
                                    purchase_date = form.purchaseDate.data,
                                    first_entry = datenow ,
                                    last_update = datenow
                                )
            # Add to database
            db.session.add(item)
            # Commit to database
            db.session.commit()

            flash('Data entry accepted')
            # And return to database display
            return redirect(url_for('database'))
    # Display form
    return render_template('ingredient_form.html',
                           title='Add Ingredient',
                           action="Add",
                           form=form)

@app.route('/edit/ingredient/<int:id>', methods=['GET', 'POST'])
def edit_ing(id):
    #read the data from the id
    ing = Ingredientlist.query.get(id)
    form = EditIngredientForm(obj=ing) #put the object in the form

    if form.validate_on_submit():
        if request.form['btn'] == "Update":
            form.populate_obj(ing)  # retrieve value from the form and update the SQL object
            ing.last_update = datetime.utcnow()
            ing.cost_unit = Ingredientlist.CostPerUnit(form.bag_size.data,form.bag_cost.data) #force recalculation
            db.session.add(ing) ## Then all you need to do is save it back in the database
            db.session.commit() ## and commit
        elif request.form['btn'] == "Delete":
            db.session.delete(ing)
            db.session.commit()
        return redirect(url_for('database'))

    return render_template('ingredient_form.html',
                           title='Edit Ingredient',
                           action="Update",
                           form=form)

@app.route('/add_category', methods=['GET', 'POST'])
def add_category():
    form = AddCategoryForm()

    if form.validate_on_submit():
        datenow= datetime.utcnow()
        item = Categorylist (   category = form.category.data,
                                first_entry = datenow,
                                last_update = datenow
                            )
        # Add to database and commit
        db.session.add(item)
        db.session.commit()
        # And return to database display
        return redirect(url_for('database'))
    # Display form
    return render_template('category_form.html',
                           title='Add Category',
                           action="Add",
                           form=form)

@app.route('/edit/category/<int:id>', methods=['GET', 'POST'])
def edit_cat(id):
    ing = Categorylist.query.get(id)
    form = AddCategoryForm(obj=ing) #put the object in the form
    if form.validate_on_submit():
        if request.form['btn'] == "Update":
            form.populate_obj(ing)  # retrieve value from the form and update the SQL object
            ing.last_update = datetime.utcnow()
            db.session.add(ing) ## Then all you need to do is save it back in the database
            db.session.commit() ## and commit
        return redirect(url_for('database'))
    return render_template('category_form.html',
                           title='Update Category',
                           action="Update",
                           form=form)
