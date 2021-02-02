from flask import Flask, render_template, redirect, request, session
from werkzeug.utils import secure_filename
from cs50 import SQL
from flask_bcrypt import Bcrypt
import os

# db = SQL("sqlite:///test.db")
db = SQL("sqlite:///diary.db")

UPLOAD_FOLDER = '/home/ubuntu/project/static/images/user_upload'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
bcrypt = Bcrypt(app)

app.debug = True
app.secret_key = "hello"


# the home route
@app.route("/", methods=['GET', 'POST'])
def home():

	if request.method == 'POST':
		if not session:
			return redirect("/")
		post_id = request.form.get('post-id')
		image_filename = db.execute("SELECT image FROM posts WHERE post_id = :post_id", post_id = post_id)


		db.execute("UPDATE posts SET isDeleted = 1 WHERE post_id = :post_id", post_id = post_id)

		if image_filename[0]['image']:
			os.remove(os.path.join(app.config['UPLOAD_FOLDER'], image_filename[0]['image']))

		return redirect("/")

	posts = None
	if session:
		posts = db.execute("SELECT username, post_id, content, image, datetime FROM posts JOIN users ON id=user_id WHERE user_id = :user_id AND isDeleted != 1 ORDER BY datetime DESC", user_id = session['id'])

	return render_template("home.html", session = session, posts = posts)


# check if the filename and format is valid
def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# generate formatted filename
# i.e some_ranadom_filename_2525.png becomes current number of images + 1.png (5.png)
def generate_filename(filename):
	# fetch the data of current named files
	count = db.execute("SELECT COUNT(*) FROM posts WHERE image IS NOT NULL")
	return str(count[0]['COUNT(*)'] + 1) + '.' + filename.rsplit('.', 1)[1]

# the add-post route
@app.route("/add-post", methods=['GET', 'POST'])
def add():

	# if user not logged in
	if not session:
		return redirect('/')

	# if user submits the form
	if request.method == "POST":

		# return request.files.get('image').filename

		# store the text content in local variable
		content = request.form.get('content')

		# if form contains an image
		if 'image' in request.files:



			# get the image
			image = request.files.get('image')

			# get the filename of that image
			image_filename = image.filename

			# ensure image name is not empty
			if image_filename != "":



				#	if extension is not allowed
				if not allowed_file(image_filename):
					return render_template('add-post.html', msg="invalid image format")

				# generate formatted name of the image file
				image_filename = generate_filename(image_filename)



				# save the image in specified path
				image.save(os.path.join(app.config['UPLOAD_FOLDER'], image_filename))

			# if image name is empty
			else:
				image_filename = None

		# store the post data in database
		db.execute("INSERT INTO posts (user_id, content, image, datetime) VALUES (:user_id, :content, :image, datetime('now', '+5.5 hours'))", user_id = session['id'], content = content, image = image_filename)

		return redirect("/")

	# if user lands on the page
	return render_template("add-post.html")

# login route
@app.route("/login", methods=['GET', 'POST'])
def login():
	# if user is already logged in
	if session:
		return redirect("/")

	# if user not logged in and submits the form
	if request.method == "POST":

		# store the credentials submitted by the user in variables
		username = request.form.get('username').lower()
		password = request.form.get('password')

		# fetch the details from the db with same username (if exists)
		users = db.execute("SELECT * FROM users WHERE username = :username ", username = username)

		# if no data exists with the username
		if not users:
			return render_template("login.html", msg="invalid username")

		# if the hash and the submitted password matched
		if bcrypt.check_password_hash(users[0]['password'], password):
			session['id'] = users[0]['id']
			return redirect('/')

		# if invalid password
		return render_template('login.html', msg="invalid password")

	# if user not logged in and land to the page
	return render_template("login.html", session = session)


# logout route
@app.route("/logout")
def logout():

	# clear the session data
	session.clear()

	return redirect("/")


# signup route
@app.route("/signup", methods=['GET', 'POST'])
def signup():

	# if user already logged in
	if session:
		return redirect("/")

	# if user submits the form
	if request.method == "POST":

		# store the submitted details in variables
		username = request.form.get('username').lower()
		password = request.form.get('password')
		confirm_password = request.form.get('confirm-password')

		# if password and confirm_password not same
		if(password != confirm_password):
			return render_template("signup.html", msg="passwords don't match")

		users = db.execute("SELECT * FROM users WHERE username = :username", username = username)

		# if username already exists
		if users:
			return render_template("signup.html", msg="username already exists")

		# hash the password
		pw_hash = bcrypt.generate_password_hash(password).decode('UTF-8')

		# store thr username and hash in the database
		db.execute("INSERT INTO users (username, password) VALUES (:username, :password)", username = username, password = pw_hash)

		return render_template("signup.html", msg='registration successful')


	# if user land to the page and not logged in
	return render_template("signup.html")




