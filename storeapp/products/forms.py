#CRUD PRODUCT fORM 
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,SelectField, DecimalField, IntegerField,TextAreaField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField, FileAllowed
from storeapp.models import Category,Product
from flask import current_app 


class ProductForm(FlaskForm):
    productname = StringField('Product Name', validators=[DataRequired()])
    productprice = DecimalField('Price', validators=[DataRequired()],places=2,rounding=None) # type: ignore
    productdescription = TextAreaField('Description', validators=[DataRequired()])
    productQuantity = IntegerField('Quantity', validators=[DataRequired()])
    productcategory = SelectField('Category', validators=[DataRequired()], coerce=int)  # type: ignore
    product_type= SelectField('Product Type', validators=[DataRequired()],choices=['physical','digital'])
    product_image = FileField('Product Image', validators=[FileAllowed(['jpg','png'])])
    submit = SubmitField('Submit')
    
    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        self.productcategory.choices = [(c.id, c.name) for c in Category.query.all()]
        




