from flask import redirect, render_template, url_for,flash,request
from app import db, app
from .models import Brand, Category,AddItem
from .forms import AddItemForm

import secrets


@app.route('/addbrand', methods=['GET','POST'])
def addbrand():
    if request.method== "POST":
        getbrand= request.form.get('brand')
        brand= Brand(name=getbrand)
        db.session.add(brand)
        db.session.commit()

        flash(f' The Brand {getbrand} was added', 'success')
        return redirect(url_for('addbrand'))
    return render_template('products/addbrand.html',brands='brands')

@app.route('/additem/<int:id>')
def single_page(id):
    items= AddItem.query.get_or_404(id)
    return render_template('products/single_page.html',items=items)


@app.route('/addcategory', methods=['GET','POST'])
def addcategory():
    if request.method== "POST":
        getbrand= request.form.get('category')
        cat= Category(name=getbrand)
        db.session.add(cat)
        db.session.commit()

        flash(f' The Category {getbrand} was added', 'success')
        return redirect(url_for('addcategory'))
    return render_template('products/addbrand.html')


@app.route("/additem", methods=["GET", "POST"])
def additem():
    """Render the website's add new item page."""
    brands= Brand.query.all()
    catergories= Category.query.all()
    # Instantiate  form class
    form = AddItemForm(request.form)

    if request.method=="POST" and form.validate():
        title= form.title.data
        description=form.description.data
        
        price= form.price.data
        quantity=form.quantity.data
        

        addproduct=AddItem(title=title,description=description,price=price,quantity=quantity)

        db.session.add(addproduct)
        db.session.commit()
        flash("Product added","success")
        return redirect(url_for('home'))

        

    return render_template('products/additem.html',form = form, title="Add Product page",brands= brands, categories=catergories)
