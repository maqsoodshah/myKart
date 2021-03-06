from myStore import db, bcrypt, mongo
from flask import render_template, redirect, url_for, Blueprint, flash, request, redirect, send_from_directory
from myStore.seller.forms import ItemForm
from flask_login import current_user, login_required, login_user, logout_user
from myStore.models import User
from bson.objectid import ObjectId
import os
from functools import wraps

seller = Blueprint('seller', __name__)
APP_ROOT = os.path.dirname(os.path.abspath(__file__))


def roles_required(f):
  @wraps(f)
  def decorated_function(*args, **kwargs):
    id = current_user.get_id()
    print('user id : ', id)
    usera = mongo.db.user.find_one({"_id": ObjectId(id)})
    print(usera)
    print(usera['email'], " ", usera['role'])
    if usera['role'] == 'customer':
      flash('You are not an seller')
      return redirect(url_for('users.login'))

    return f(*args, **kwargs)
  return decorated_function


@seller.route('/seller/additem', methods=['GET', 'POST'])
@login_required
@roles_required
def additem():
  form = ItemForm()
  if(itemdetail(form)):
    return viewupdate()

  return render_template('sellerdash.html', title='ADD item', Legend='Add Item', form=form, item={})


@seller.route('/seller/selvu')
@login_required
@roles_required
def viewupdate():
  print("executing viewupdate")
  sellerid = current_user.get_id()
  print("got userid")
  items = mongo.db.items.find({'SellerId': sellerid})
  print("query executed")
  print(items)
  return render_template('sellerviewupdate.html', title='youritems', items=items)


@seller.route('/seller/<string:item_id>', methods=['GET', 'POST'])
@login_required
@roles_required
def selleritemview(item_id):
  print("executing seller item view")
  sellerid = current_user.get_id()

  item = mongo.db.items.find_one_or_404({"_id": ObjectId(item_id)})
  form = ItemForm()

  if(item['SellerId'] == sellerid):
    print("ALL OK")
    if(itemdetail(form, itemid=item['_id'])):
      return viewupdate()
  else:
    print("GAdbad")

  return render_template('sellerdash.html', title='Update Item', Legend='Update Item', item=item, form=form)


@seller.route('/seller/orders', methods=['GET', 'POST'])
@login_required
@roles_required
def ordersrecieved():
  sellerid = current_user.get_id()
  ordersrec = mongo.db.order.find({"item_details": {"$elemMatch": {"SellerId": sellerid}}})
  print("printing order Details")
  a = []
  for doc in ordersrec:
    for itemd in doc['item_details']:
      if(itemd['SellerId'] == sellerid):
        itemdetail = mongo.db.items.find_one({'_id': ObjectId(itemd['item_id'])})

        d = [itemdetail, itemd, doc['delivery_details']]
        a.append(d)
  print("printing order Details")
  for x in a:
    print("\n", x)

  return render_template('orderreceived.html', title='Orders', ordersr=a)


@seller.route('/seller/delete/<string:item_id>', methods=['GET', 'POST'])
@login_required
@roles_required
def sellerdelete(item_id):
  sellerid = current_user.get_id()
  print("executing delete")
  item = mongo.db.items.find_one_or_404({"_id": ObjectId(item_id)})
  if(item['SellerId'] == sellerid):
    print("ALL OK")
    mongo.db.items.remove({"_id": ObjectId(item_id)})
  else:
    print("GAdbad")
  items = mongo.db.items.find({'SellerId': sellerid})

  return viewupdate()


def itemdetail(form, itemid=0):

  sellerid = current_user.get_id()
  sellerinfo = mongo.db.user.find_one({'_id': ObjectId(sellerid)})
  target = os.path.join(APP_ROOT, '../static')
  print(target)
  print(request.files.getlist("images"))
  if not os.path.isdir(target):
    os.mkdir(target)
  imageslist = []
  if form.validate_on_submit():
    for upload in request.files.getlist("images"):
      print("Entered file section")
      print(upload)
      print("{} is the file name".format(upload.filename))
      filename = upload.filename
      # This is to verify files are supported
      ext = os.path.splitext(filename)[1]
      if (ext == ".jpg") or (ext == ".png"):
        print("File supported moving on...")
      else:
        render_template("Error.html", message="Files uploaded are not supported...")
      destination = "/".join([target, form.category.data, filename])
      imageslist.append(filename)
      print("Accept incoming file:", filename)
      print("Save it to:", destination)
      upload.save(destination)
      print("printing imageslist")
      for x in imageslist:
        print(x)

    a = form.material_Care.data
    formdata = {
        'Category': form.category.data,
        'Seller': sellerinfo['username'],
        'Type': form.typeofitem.data,
        'Image': imageslist,
        'Brand': form.brand.data,
        'Short Description': form.short_Description.data,
        'Description': form.description.data,
        'Mrp': form.mrp.data,
        'Discount': form.discount.data,
        'Price': (form.mrp.data - ((form.mrp.data * form.discount.data) / 100)),
        'Size': form.sizenqty.data,
        'Product Details': form.productDetails.data,
        'Material & Care': [a, 0],
        'Tags': form.tags.data,
        'SellerId': sellerid}
    if(itemid == 0):
      mongo.db.items.insert(formdata)
      return 1
    else:
      mongo.db.items.update({"_id": itemid}, formdata)
      print("data updated")
      return 1

  else:
    return 0
