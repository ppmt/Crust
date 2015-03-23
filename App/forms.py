from flask.ext.wtf import Form
from wtforms.ext.sqlalchemy.fields import QuerySelectField  #import the ext to read database and create dropdown list
from wtforms import TextField, StringField, BooleanField, FloatField, DateField, SelectField, FieldList, FormField, TextAreaField, SubmitField
from wtforms.validators import Optional, DataRequired, Length
from .models import Supplierlist, Categorylist


#Functions used to create the dropdown form
def supplierlist():
    #supplier = Supplier.query.get(id)
    return Supplierlist.query

def categorylist():
    #supplier = Supplier.query.get(id)
    return Categorylist.query


class AddIngredientForm(Form):
    ingredient = StringField('Ingredient', validators=[DataRequired()])
    category = QuerySelectField('Category', query_factory=categorylist, get_label='category', allow_blank=False)
    #category= SelectField ('category' , choices=[('flour','flour'),('yeast','yeast')])  #works but is not dynamic!
    supplier = QuerySelectField(query_factory=supplierlist, get_label='supplier', allow_blank=True, blank_text=u'Choose an optional Supplier',validators=[Optional()])
    #supplier= SelectField ('supplier' , choices=[('Morrisons','Morrisons'),('Tesco','Tesco')])
    bag_size = FloatField('bagSize', validators=[DataRequired()])
    unit = SelectField ('unit' , choices=[('kg','kilogram'),('l','litre')])
    bag_cost = FloatField('bagCost', validators=[DataRequired()])
    purchaseDate = DateField('purchaseDate', validators=[Optional()])


class EditIngredientForm(Form):
    ingredient = StringField('Ingredient', validators=[DataRequired()])
    category = QuerySelectField('Category', query_factory=categorylist, get_label='category', allow_blank=False)
    #category= SelectField ('category' , choices=[('flour','flour'),('yeast','yeast')])  #works but is not dynamic!
    supplier = QuerySelectField(query_factory=supplierlist, get_label='supplier', allow_blank=True, blank_text=u'Choose an optional Supplier',validators=[Optional()])
    #supplier= SelectField ('supplier' , choices=[('Morrisons','Morrisons'),('Tesco','Tesco')])
    bag_size = FloatField('bagSize', validators=[DataRequired()])
    unit = SelectField ('unit' , choices=[('kg','kilogram'),('l','litre')])
    bag_cost = FloatField('bagCost', validators=[DataRequired()])
    purchaseDate = DateField('purchaseDate', validators=[Optional()])


class AddCategoryForm(Form):
    category = StringField('category', validators=[DataRequired()])


class IngredientListTemplate(Form):
    category = QuerySelectField(query_factory=categorylist, get_label=u'category', allow_blank=False)
    ingredient = StringField( validators=[DataRequired()])
    supplier = QuerySelectField(query_factory=supplierlist, get_label=u'supplier', allow_blank=True, blank_text=u'Choose an optional Supplier',validators=[Optional()])

    #No idea what it is for but it removes the CSRF token missing
    def __init__(self, *args, **kwargs):
           kwargs['csrf_enabled'] = False
           super(IngredientListTemplate, self).__init__(*args, **kwargs)

class IngredientListForm(Form):
    ingredient_list = FieldList(FormField(IngredientListTemplate), min_entries=3)


class Release(Form):
    paragraph = TextAreaField('Enter something for the text body:')
    submit = SubmitField('Submit')
