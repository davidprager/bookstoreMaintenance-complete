from flask import Flask, render_template, request, redirect, url_for
import pymongo
from bson.objectid import ObjectId

# instantiate the app
app = Flask(__name__)

# Connect to MongoDB
client = pymongo.MongoClient()
db = client.bookstore
books = db.books
categories = db.categories

# set up routes
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/read')
def read():
    bks = books.find({})
    return render_template('read.html', books = bks) # render the read template

@app.route('/create')
def create():
    # get all the categories
    cats = categories.find({})
    return render_template('create.html', categories = cats) # render the create template


@app.route('/create', methods=['POST'])
def create_post():
    # create a new document with the data the user entered
    doc = {
        "title": request.form['title'],
        "author": request.form['author'],
        "ISBN": request.form['isbn'],
        "price": request.form['price'],
        "category": request.form['category']
    }
    # insert the new doc
    db.books.insert_one(doc) # insert a new document

    return redirect(url_for('read')) # tell the browser to make a request for the /read route


@app.route('/edit/<mongoid>')
def edit(mongoid):
    # get the doc that corresponds to the user selection
    doc = db.books.find_one({"_id": ObjectId(mongoid)})
    # get all the categories
    cats = categories.find({})

    return render_template('edit.html', mongoid=mongoid, doc=doc, categories = cats) # render the edit template


@app.route('/edit/<mongoid>', methods=['POST'])
def edit_post(mongoid):
    # create a new document with the data the user entered
    doc = {
        "title": request.form['title'],
        "author": request.form['author'],
        "ISBN": request.form['isbn'],
        "price": request.form['price'],
        "category": request.form['category']
    }
    # update the book with the new data
    db.books.update(
        {"_id": ObjectId(mongoid)}, # match criteria
        { "$set": doc }
    )

    return redirect(url_for('read')) # tell the browser to make a request for the /read route


@app.route('/delete/<mongoid>')
def delete(mongoid):
    # delete the book that corresponds to the user selection
    db.books.delete_one({"_id": ObjectId(mongoid)})
    return redirect(url_for('read')) # tell the web browser to make a request for the /read route.

@app.errorhandler(Exception)
def handle_error(e):
    # Output any errors - good for debugging.
    return render_template('error.html', error=e) # render the edit template


if __name__ == "__main__":
    app.run(debug = True)
