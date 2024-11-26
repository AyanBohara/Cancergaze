
import pickle
import numpy as np
from SVM import SVM
from standarize import standardize_data
from login import LoginForm, SignupForm
from flask_login import LoginManager, UserMixin, current_user, login_user, logout_user, login_required
from flask_bcrypt import Bcrypt
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, flash, redirect, url_for, request, Response, send_file, jsonify


# Initializes a Flask app
app = Flask(__name__, static_url_path="/static")

app.config['SECRET_KEY'] = "de9e5b220476ba0aba47040eb9b2fea9"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///god.db'
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = "info"

db = SQLAlchemy(app)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(20), nullable=False)
    lastname = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    

    def repr(self):
        return f"User({self.id}{self.firstname},{self.email},{self.password})"


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()  # Instantiate your form here
    if form.validate_on_submit():
        # Your login logic here
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user, remember=True)
            return redirect(url_for('index'))
        else:
            flash('Login unsuccessful. Please check email and password.', 'danger')

    # Pass the form to the template
    return render_template('login.html', form=form)

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = SignupForm()
    if form.validate_on_submit():
        # Check if the email already exists
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash(
                'Email address already in use. Please choose a different one.', 'danger')
            return render_template('signup.html', form=form)

        # Hash the password
        hashed_password = generate_password_hash(form.password.data)

        # Create a new user object
        new_user = User(
            firstname=form.firstname.data,
            lastname=form.lastname.data,
            email=form.email.data,
            password=hashed_password
        )

        # Add the user to the database
        db.session.add(new_user)
        db.session.commit()

        # Flash a success message and redirect to the login page
        flash('Account created successfully! You can now log in.', 'success')
        return redirect(url_for('login'))

    return render_template('signup.html', form=form)



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))







# Load the trained SVM model from the .pkl file
with open("SVM_model.pkl", "rb") as file:
    model_SVM = SVM.load_model("SVM_model.pkl")

@app.route("/")
@login_required 
def index():
    return render_template("index.html")

# SVM Prediction
def predict_svm(features):
    final_features = [np.array(features)]
    final_features = standardize_data(final_features)
    prediction_proba = model_SVM.predict_proba_svm(final_features)
    benign_prob = prediction_proba[0]
    output = model_SVM.predict(final_features)

    if np.any(output == 1):
        return f"The patient is predicted as Malignant with a probability of {benign_prob:.2%}."
    else:
        return f"The patient is predicted as Benign with a probability of {1 - benign_prob:.2%}."

@app.route("/predict", methods=["GET", "POST"])
def predict():
    if request.method == "POST":
        try:
            # Convert form data to float values
            features = [
                float(request.form["radius_mean"]),
                float(request.form["perimeter_mean"]),
                float(request.form["area_mean"]),
                float(request.form["concave_points_mean"]),
                float(request.form["radius_worst"]),
                float(request.form["perimeter_worst"]),
                float(request.form["area_worst"]),
                float(request.form["concave_points_worst"]),
            ]

            # Call the prediction function
            prediction = predict_svm(features)
            return render_template("predict.html", prediction=prediction)

        except ValueError as e:
            # Handle errors and provide feedback
            return render_template("predict.html", prediction=f"Invalid input: {e}")

    return render_template("predict.html")  # For GET request, load the form

@app.route("/data")
def data():
    return render_template("data.html")

#for future need
@app.route("/faq")
def faq():
    return render_template("faq.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

# Fix for missing image route
@app.route("/image")
def image():
    return render_template("image.html")  # Ensure you have image.html in the templates folder

@app.route("/user_logout")
def user_logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=True)
