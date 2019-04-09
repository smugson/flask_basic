from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app= Flask(__name__)

app.config.update(

	SECRET_KEY='topsecret',
	SQLALCHEMY_DATABASE_URI='postgresql://postgres:topsecret@localhost/catalog_db',
#	SQLALCHEMY_DATABASE_URI='<database>//<user_id>:<password>@<server>/<database_name>',
	SQLALCHEMY_TRACK_MODIFICATIONS=False
	)

db = SQLAlchemy(app)

@app.route('/name')
@app.route('/')
def hello_flask():
	return "Hello SMugson"


#query- string: A GET request
@app.route('/new/')
def query_strings(greeting='Bonjour'):
	query_val=request.args.get('greetings', greeting)
	return '<h1> The greeting is : {0} </h1>'.format(query_val)


#getting rid of query string(self)
@app.route('/user')
@app.route('/user/<name>')
def no_query_strings(name='Lamarge'):
	return '<h1>This is :{} </h1>'.format(name)


#render_template
@app.route('/temp')
def using_template():
	return render_template('hello.html')


#using Jinja
@app.route('/watch')
def top_movies():
	movie_list = ['Lord of the rings',
				  'The Lords supper',
				  'Home alone',
				  'Pilgrim progress',
				  'John Wick',
				  'Ninth Mile']
	return render_template('movie.html',
							movies= movie_list,
							name = 'Smugson')


@app.route('/table')
def movies_plus():
	movies_dict ={'Lord of the rings': 02.14,
				  'The Lords supper' : 3.20,
				  'Home alone': 1.50,
				  'Pilgrim progress': 2.52,
				  'John Wick': 4.00,
				  'Ninth Mile': 1.42}
	return render_template('table.html',
							movies=movies_dict,
							name="Olami")


#Jinja filter
@app.route('/filters')
def filter_data():
	movies_dict ={'Lord of the rings': 02.14,
				  'The Lords supper' : 3.20,
				  'Home alone': 1.50,
				  'Pilgrim progress': 2.52,
				  'John Wick': 4.00,
				  'Ninth Mile': 1.42}
	return render_template('filter.html',
							movies=movies_dict,
							name=None,
							film='a christmas carol')


#macros can be liken to function in python
@app.route('/macros')
def jinja_macros():
	movies_dict ={'Lord of the rings': 02.14,
				  'The Lords supper' : 3.20,
				  'Home alone': 1.50,
				  'Pilgrim progress': 2.52,
				  'John Wick': 4.00,
				  'Ninth Mile': 1.42}
	return render_template('using_macros.html',
							movies=movies_dict)


class Publication(db.Model):
	__tablename__='publication'

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(80), nullable=False)

	def __init__(self, name):
		self.name = name

	def __repr__(self):
		return 'Publisher is {}'.format(self.name)


class Book(db.Model):
	__tablename__='book'

	id=db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(500), nullable=False, index = True)
	author = db.Column(db.String(150))
	avg_rating = db.Column(db.Float)
	format = db.Column(db.String(50))
	image = db.Column(db.String(100), unique=True)
	num_pages = db.Column(db.Integer)
	pub_date = db.Column(db.DateTime, default=datetime.utcnow())

	#relationship
	pub_id = db.Column(db.Integer, db.ForeignKey('publication.id'))


	def __init__(self, title, author, avg_rating, format, image, num_pages, pub_id):
		self.title = title
		self.author = author
		self.avg_rating= avg_rating
		self.format= format
		self.image=image
		self.num_pages=num_pages
		self.pub_id=pub_id

	def __repr__(self):
		return '{} by {}'.format(self.title, self.author)



if __name__ == '__main__':
	db.create_all()
	app.run(debug=True)

