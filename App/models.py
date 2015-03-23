from App import db, app


class Ingredientlist(db.Model):
    # Definition of the models
    id = db.Column(db.Integer, primary_key=True)
    ingredient = db.Column(db.String(64), index=True, unique=True)
    category_id = db.Column(db.Integer, db.ForeignKey('categorylist.id'))
    ## below needs to be moved to Categorylist....it could list all the ingredient under one category
    ## At least this is how I understant relationship
    #category = db.relationship('Categorylist', backref='category', lazy='dynamic')

    supplier_id = db.Column(db.Integer, db.ForeignKey('supplierlist.id'))
    bag_size = db.Column(db.Float, index=False, unique=False)
    bag_cost = db.Column(db.Float, index=False, unique=False)
    unit = db.Column(db.String(5), index=False, unique=False)
    cost_unit = db.Column(db.Float, index=False, unique=False)
    purchase_date = db.Column(db.DateTime)
    first_entry = db.Column(db.DateTime)
    last_update = db.Column(db.DateTime)

    @staticmethod
    def CostPerUnit(bag_size, bag_cost):
        return bag_cost/bag_size 

    def __repr__(self):
        return '<Ingredient %r>' % (self.ingredient)


class Categorylist(db.Model):
    # Definition of the models
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(30), index=True, unique=True)
    first_entry = db.Column(db.DateTime)
    last_update = db.Column(db.DateTime)
    #The link below allowed to transfer easily from category_id to the category name
    #it creates a virtual field in Ingredientlist that refers to the category names rather than just its id
    #https://stackoverflow.com/questions/22216510/foreign-key-relations-with-children-nested-foreign-keys
    categories = db.relationship('Ingredientlist', backref='category')

    @staticmethod
    def GetCatID(Category):
        cat = Categorylist.query.filter_by(category=Category).first()
        return cat.id

    def __repr__(self):
        #return '<Category %r>' % (self.category)
        return self.category   # this is what is return by the wftorm QuerySelectField...so must be just the category name


class Supplierlist(db.Model):
    # Definition of the models
    id = db.Column(db.Integer, primary_key=True)
    supplier = db.Column(db.String(60), index=True, unique=True)
    #supplier_code = db.Column(db.String(30), index=False, unique=False)
    first_entry = db.Column(db.DateTime)
    last_update = db.Column(db.DateTime)
    suppliers = db.relationship('Ingredientlist', backref='supplier')

    @staticmethod
    def GetCatID(Supplier):
        if Supplier=='None':
            return ""
        cat = Supplierlist.query.filter_by(supplier=Supplier).first()
        return cat.id

    def __repr__(self):
        #return '<Supplier %r>' % (self.supplier)
        return self.supplier # same as for category
