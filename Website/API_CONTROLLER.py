import pickle
import os
from . import db 
from .Models import User, BlogPost, SecurityQuestions, UserPredictions  # Import User model # Import db instance
import random
from sqlalchemy import desc
import pandas as pd
from flask import jsonify, render_template


current_directory = os.path.dirname(os.path.abspath(__file__))
assets_directory = os.path.join(current_directory, 'Assets/Model')
imputer_file_path = os.path.join(assets_directory, 'imputer.pkl')
model_file_path = os.path.join(assets_directory, 'model.pkl')

with open(model_file_path, "rb") as model_file:
    model = pickle.load(model_file)


with open(imputer_file_path, "rb") as imputer_file:
    imputer = pickle.load(imputer_file)




class API_CONTROLLER:
    request_obj = None
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(API_CONTROLLER, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        # Initialize your controller here, but do NOT create a new self instance
        pass
    
    def preprocess_request_data(self, request_obj):
        self.request_obj = None
        self.request_obj = request_obj
        return self
    
    def reformat_request(self):
        feature_map = {
            'Fever': {'yes': 1, 'no': 0},
            'Tiredness': {'yes': 1, 'no': 0},
            'Dry-Cough': {'yes': 1, 'no': 0},
            'Difficulty-in-Breathing': {'yes': 1, 'no': 0},
            'Sore-Throat': {'yes': 1, 'no': 0},
            'None_Sympton': {'yes': 1, 'no': 0},
            'Severity_None': 0,
            'Severity_Mild': 0,
            'Severity_Moderate': 0,
            'Severity_Severe': 0,
            'Age_0-9': 0,
            'Age_10-19': 0,
            'Age_20-24': 0,
            'Age_25-59': 0,
            'Age_60+': 0,
        }

        reformatted_content = {}

        # Handle binary features
        for feature in feature_map:
            if 'Age_' not in feature and 'Severity_' not in feature:
                value = self.request_obj.get(feature, '').lower()
                reformatted_content[feature] = feature_map[feature].get(value, 0)

        # Handle age groups
        age = int(self.request_obj.get('AGE', 0))
        if age <= 9:
            reformatted_content['Age_0-9'] = 1
        elif 10 <= age <= 19:
            reformatted_content['Age_10-19'] = 1
        elif 20 <= age <= 24:
            reformatted_content['Age_20-24'] = 1
        elif 25 <= age <= 59:
            reformatted_content['Age_25-59'] = 1
        else:
            reformatted_content['Age_60+'] = 1

        # Handle severity level
        severity_level = self.request_obj.get("SEVERITY_LEVEL", 0)
        if severity_level == 1:
            reformatted_content['Severity_None'] = 1
        elif severity_level == 2:
            reformatted_content['Severity_Mild'] = 1
        elif severity_level == 3:
            reformatted_content['Severity_Moderate'] = 1
        elif severity_level == 4:
            reformatted_content['Severity_Severe'] = 1

        return reformatted_content


    
    def predict(self):
        reformatted_content = self.reformat_request()

        # Removed the manually created feature_array
        feature_names = [
            'Fever', 'Tiredness', 'Dry-Cough', 'Difficulty-in-Breathing', 'Sore-Throat',
            'None_Sympton', 'Age_0-9', 'Age_10-19', 'Age_20-24', 'Age_25-59', 'Age_60+',
            'Severity_Mild', 'Severity_Moderate', 'Severity_None', 'Severity_Severe',
        ]

        feature_array = pd.DataFrame([reformatted_content], columns=feature_names)

        # Apply the imputer and the model
        feature_array = imputer.transform(feature_array)
        prediction = model.predict_proba(feature_array)

        # Adjusted the conditions to check if 'yes' for severity levels
        if (self.request_obj.get("Severity_Mild") == "no" and
                self.request_obj.get("Severity_Moderate") == "no" and
                self.request_obj.get("Severity_Severe") == "no"):
            prediction -= 0.50

        symptom_names = ['Fever', 'Tiredness', 'Dry-Cough', 'Difficulty-in-Breathing', 'Sore-Throat', 'None_Sympton']

        # Adjusted the condition to check 'no' for symptoms and 'yes' for all severity levels
        if all(self.request_obj.get(symptom) == "no" for symptom in symptom_names) and \
        (self.request_obj.get("Severity_Mild") == "no" or
            self.request_obj.get("Severity_Moderate") == "no" or
            self.request_obj.get("Severity_Severe") == "no"):
            prediction -= 0.50

        if prediction[0][1] < 0:
            prediction[0][1] = 0

        return prediction[0][1]

    def login(self):
        user = User.query.filter_by(username=self.request_obj.get("username")).first()
        user_object = {"username": user.username, "password": user.password, "email": user.email, "id": user.id,}
        if user:
            if user.password == self.request_obj.get("password"):
                return jsonify(userAuthenticated="true", user=user_object ), 200
            else:  # This handles the incorrect password case
                return jsonify(userAuthenticated="false", error_mes="password incorrect"), 200
        else:  # This handles the user not found case
                return jsonify(userAuthenticated="false", error_mes="username not found || create account..."), 200

    
    def create_account(self):
        if User.query.filter_by(username=self.request_obj.get('username')).first():
            return jsonify(userAccountCreated="false", error_mes="user already exist...login."), 200
        if User.query.filter_by(email=self.request_obj.get('email')).first():
            return jsonify(userAccountCreated="false", error_mes="email already exist...login."), 200
        else:
            new_user = User(id=random.randint(1000,1000000),username=self.request_obj.get("username"), password=self.request_obj.get("password"), email=self.request_obj.get("email"))
            new_security_q1 = SecurityQuestions(id=random.randint(1000,1000000), username=new_user.username, question=self.request_obj.get("question1"), answer=self.request_obj.get("answer1"), qnumber=1)
            new_security_q2 = SecurityQuestions(id=random.randint(1000,1000000), username=new_user.username, question=self.request_obj.get("question2"), answer=self.request_obj.get("answer2"), qnumber=2)
            db.session.add(new_user)
            db.session.add(new_security_q1)
            db.session.add(new_security_q2)
            db.session.commit()  # For debugging

            return jsonify(userAccountCreated="true"), 200
   
    def to_dict(self, row):
        return {column.name: getattr(row, column.name) for column in row.__table__.columns}
    


    # send back data: user questions and answers {username, question1, answer1, question2, answer2} 
    def forgot_password(self):
        user = User.query.filter_by(username=self.request_obj.get("username")).first()
        if not user:
            return jsonify(nextStep="false", error_mes="username not found || create account..."), 200
        else:
            security_q = SecurityQuestions.query.filter_by(username=self.request_obj.get("username")).all()
            questions = [self.to_dict(q) for q in security_q]
            return jsonify(nextStep="true", security_questions=questions), 200 


    # change and update password for given user {username, newpassword}
    def change_password(self):
        user = User.query.filter_by(username=self.request_obj.get("username")).first()
        if not user:
            return jsonify(valid="false", error_mes="username not found || create account..."), 200
        else:
            user.password = self.request_obj.get("new_password")
            db.session.commit()
            return jsonify(valid="true", mess="password updated!"), 200

    
    def addRequestBlog(self):
        self.request_obj=self.request_obj
        if self.request_obj.get("title") == "" or self.request_obj.get("body") == "":
            return jsonify(blogPostRequested="false", error_mes="title and body cannot be empty"), 200
        new_blog_post = BlogPost(id=random.randint(1000,1000000), title=self.request_obj.get("title"), body=self.request_obj.get("body"), author=self.request_obj.get("username"), verified=False)
        db.session.add(new_blog_post)
        db.session.commit()
        return jsonify(blogPostRequested="true"), 200
    
    def getBlogPosts(self):
        blog_posts = BlogPost.query.filter_by(verified=True).all()
        posts = [self.to_dict(post) for post in blog_posts]
        return jsonify(blog_posts=posts), 200
    
    def getUserPredictionsLog(self):
        self.request_obj = self.request_obj
        # Retrieve the most recent two entries for the given username
        user_predictions = UserPredictions.query.filter_by(username=self.request_obj.get("username")).order_by(desc(UserPredictions.date_posted)).limit(2).all()
        predictions = [self.to_dict(prediction) for prediction in user_predictions]
        if user_predictions:
            return jsonify(status="true", predictions=predictions), 200
        else:
            return jsonify(status="false", error_mes="no predictions found..."), 200
        
    def NAV_loadPage(self, page):
        try:
            # Render the template directly without jsonify
            return render_template(f'{page}.html')
        except:
            # Handle the error properly (returning an error page or 404)
            return render_template('error.html'), 404
