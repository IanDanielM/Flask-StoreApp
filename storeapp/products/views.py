from flask import Blueprint,render_template,url_for,redirect,request,flash,abort
from .forms import ProductForm
from .utils import save_picture
from storeapp import db
from storeapp.models import Product,Category
from storeapp.seller.utils import seller_required
from flask_login import login_required,current_user


product = Blueprint('product', __name__)


@product.route('/products')
def ProductsListView():
    products = Product.query.all()
    return render_template('products/listproducts.html',products=products)

@product.route('/seller/products/add',methods=['GET','POST'])
@login_required
@seller_required
def ProductsAddView():
    form = ProductForm()
    if form.validate_on_submit():
        category = Category.query.get(form.productcategory.data)
        picture_file = None
        if form.product_image.data:
            picture_file = save_picture(form.product_image.data)
        product = Product(name=form.productname.data,
                  price=form.productprice.data,
                  description=form.productdescription.data,
                  product_type=form.product_type.data,
                  quantity=form.productQuantity.data,
                  user_id=current_user.id, # type: ignore
                  categoryid =category.id,
                  Image1=picture_file)
        flash('Product saved successfully')
        db.session.add(product)
        db.session.commit()
        return redirect(url_for('product.ProductsListView'))
   
    return render_template('products/addproducts.html', form=form)



@product.route('/seller/product/edit/<int:id>',methods=['GET','POST'])
@seller_required
def edit_product(id):
    product = Product.query.get_or_404(id)
    form = ProductForm(obj=product)
    if form.validate_on_submit():
        category = Category.query.get(form.productcategory.data)
        picture_file = None
        if form.product_image.data:
            picture_file = save_picture(form.product_image.data)
            product.Image1 = picture_file
        product.name = form.productname.data
        product.price = form.productprice.data
        product.description = form.productdescription.data
        product.product_type = form.product_type.data
        product.quantity = form.productQuantity.data
        product.user_id = 7
        product.categoryid = category.id
        db.session.commit()
        flash('Product updated successfully')
        return redirect(url_for('product.ProductsListView'))
    elif request.method == 'GET':
        form.productname.data = product.name
        form.productprice.data = product.price
        form.productdescription.data = product.description
        form.product_type.data = product.product_type
        form.productQuantity.data = product.quantity
        form.productcategory.data = product.categoryid
        form.product_image.data = product.Image1
    
    return render_template('products/editproducts.html', form=form, product=product)


@product.route('/seller/product/<int:id>/delete', methods=['GET', 'POST'])
@seller_required
def delete_product(id):
    product=Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    flash('Product deleted successfully')
    return redirect(url_for('product.ProductsListView'))


#variationsviews









    









