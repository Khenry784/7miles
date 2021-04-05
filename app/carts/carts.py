from flask import redirect, render_template, url_for,flash,request,session,current_app
from app import db, app
from app.products.models import AddItem






@app.route('/addCart', methods=["POST"])
def addCart():
    
    try:
        id= request.form.get('id')
        quantity=request.form.get("quantity")
        items= AddItem.query.filter_by(id=id).first()
        if id and quantity and request.method=="POST":
            DictItems= {id:{'title':items.title,"price":items.price,"Quantity":items.quantity}}

            if 'ShoppingCart' in session:
                print(session ["ShoppingCart"])
                if id in session ['ShoppingCart']:
                    print("This Item is Already in you Cart!")
                else:
                    return redirect(request.referrer)
            else:
                session['ShoppingCart']=DictItems
                return redirect(request.referrer)

    except Exception as e:
        print(e)
    finally:
        return redirect(request.referrer)


@app.route('/cart')
def getCart():
    if 'ShoppingCart' not in session:
        return redirect(request.referrer)
    return render_template('cart.html')