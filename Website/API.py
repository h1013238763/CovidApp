from flask import Blueprint, jsonify, request, redirect
import pickle
import os
from . import db 
from .Models import User, BlogPost, SecurityQuestions, UserPredictions  # Import User model # Import db instance
import random
from sqlalchemy import desc

API = Blueprint('API', __name__)

current_directory = os.path.dirname(os.path.abspath(__file__))
assets_directory = os.path.join(current_directory, 'Assets/Model')
imputer_file_path = os.path.join(assets_directory, 'imputer.pkl')
model_file_path = os.path.join(assets_directory, 'model.pkl')

with open(model_file_path, "rb") as model_file:
    model = pickle.load(model_file)

with open(imputer_file_path, "rb") as imputer_file:
    imputer = pickle.load(imputer_file)


def reformat_input(content):
    feature_map = {
        'SEX': {'male': 0, 'female': 1},
        'DIABETES': {'yes': 1, 'no': 0},
        'OBESITY': {'yes': 1, 'no': 0},
        'ASTHMA': {'yes': 1, 'no': 0},
        'TOBACCO': {'yes': 1, 'no': 0},
        'PATIENT_TYPE': {'yes': 1, 'no': 0}
    }
    
    reformatted_content = {}
    for feature, mapping in feature_map.items():
        value = content.get(feature, '').lower()
        reformatted_content[feature] = mapping.get(value, None)
        
    reformatted_content['AGE'] = int(content.get('AGE', 0))

    return reformatted_content



@API.route("/api/predict", methods=["POST"])
def predict():
    try:
        #example input {"SEX": "male", "AGE": 20, "DIABETES": "yes", "OBESITY": "yes", "ASTHMA": "yes", "TOBACCO": "yes", "PATIENT_TYPE": "no"}
        # Parse input features from JSON
        content = request.json
        reformatted_content = reformat_input(content)
        
        feature_array = [
            reformatted_content['SEX'],
            reformatted_content['AGE'],
            reformatted_content['DIABETES'],
            reformatted_content['OBESITY'],
            reformatted_content['ASTHMA'],
            reformatted_content['TOBACCO'],
            reformatted_content['PATIENT_TYPE']
        ]
        # Handle missing values using the imputer
        feature_array = imputer.transform([feature_array])

        # Make prediction
        prediction = model.predict_proba(feature_array)
        predi = UserPredictions(id=random.randint(1000,1000000), username=content.get("username"), prediction=prediction[0][1])
        db.session.add(predi)
        db.session.commit()
        # Return probability (the second class)
        return jsonify({"probability": prediction[0][1]})

    except Exception as e:
        return jsonify({"error": str(e)})


@API.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    # Query the database for the user
    user = User.query.filter_by(username=data.get("username")).first()
    if user:
        if user.password == data.get("password"):
            return jsonify(userAuthenticated="true"), 200
    elif user.password != data.get("password"):
        return jsonify(userAuthenticated="false", error_mes="password incorrect"), 200
    else: 
        return jsonify(userAuthenticated="false", error_mes="username not found || create account..."), 200
        

@API.route('/api/create_account', methods=['POST'])
def createAccount():
    data = request.get_json()
    if User.query.filter_by(username=data.get('username')).first():
        return jsonify(userAccountCreated="false", error_mes="user already exist...login."), 200
    else:
        new_user = User(id=random.randint(1000,1000000),username=data.get("username"), password=data.get("password"), email=data.get("email"))
        new_security_q1 = SecurityQuestions(id=random.randint(1000,1000000), username=new_user.username, question=data.get("question1"), answer=data.get("answer1"), qnumber=1)
        new_security_q2 = SecurityQuestions(id=random.randint(1000,1000000), username=new_user.username, question=data.get("question2"), answer=data.get("answer2"), qnumber=2)
        db.session.add(new_user)
        db.session.add(new_security_q1)
        db.session.add(new_security_q2)
        db.session.commit()  # For debugging
        for a in SecurityQuestions.query.all():
            print(a.username, a.question, a.answer, a.qnumber, a.id)
        return jsonify(userAccountCreated="true"), 200


def to_dict(row):
    return {column.name: getattr(row, column.name) for column in row.__table__.columns}


#first step and window allowing user to enter username example input {"username": "test"}
@API.route('/api/forgot_password', methods=['POST'])
def forgotPassword():
    data = request.get_json()
    user = User.query.filter_by(username=data.get("username")).first()
    if not user:
        return jsonify(nextStep="false", error_mes="username not found || create account..."), 200
    else:
        security_q = SecurityQuestions.query.filter_by(username=data.get("username")).all()
        questions = [to_dict(q) for q in security_q]
        return jsonify(nextStep="true", security_questions=questions ), 200 
#===================================================================================================


#example input {"username": "test", "firstA": "test", "secondA": "test", "new_password": "test"}
@API.route('/api/change_password', methods=['POST'])
def verifySecurityQuestions():
    data = request.get_json()
    user = User.query.filter_by(username=data.get("username")).first()
    if not user:
        return jsonify(nextStep="false", error_mes="username not found || create account..."), 200
    else:
        security_q1 = SecurityQuestions.query.filter_by(username=user.username, answer=data.get("firstA")).first()
        security_q2 = SecurityQuestions.query.filter_by(username=user.username, answer=data.get("secondA")).first()
        # if not security_q1 or not security_q2:
        #     return jsonify(nextStep="false", error_mes="security questionsincorrect..."), 200
        if not security_q1:
            return jsonify(nextStep="false", error_mes="first security question incorrect...", qindex=1), 200
        if not security_q2:
            return jsonify(nextStep="false", error_mes="second security question incorrect...", qindex=2), 200
        if data.get("new_password") != "":
            user.password = data.get("new_password")
            db.session.commit()
            return jsonify(nextStep="true", mess="password updated."), 200
        else:
            return jsonify(nextStep="false", err_mes="new username cannot be empty"), 200

#example input {"username": "test12", title: "test", body: "test"}
@API.route('/api/add_request_blog', methods=['POST'])
def addRequestBlog():
    data=request.get_json()
    if data.get("title") == "" or data.get("body") == "":
        return jsonify(blogPostRequested="false", error_mes="title and body cannot be empty"), 200
    new_blog_post = BlogPost(id=random.randint(1000,1000000), title=data.get("title"), body=data.get("body"), author=data.get("username", verified=False))
    db.session.add(new_blog_post)
    db.session.commit()
    return jsonify(blogPostRequested="true"), 200

#just call the function to retrive user verified blog posts by us
@API.route('/api/get_blog_posts', methods=['GET'])
def getBlogPosts():
    blog_posts = BlogPost.query.filter_by(verified=True).all()
    posts = [to_dict(post) for post in blog_posts]
    return jsonify(blog_posts=posts), 200

@API.route('/api/get_user_predictions_log', methods=['POST'])
def getUserPredictionsLog():
    data = request.get_json()
    # Retrieve the most recent two entries for the given username
    user_predictions = UserPredictions.query.filter_by(username=data.get("username")).order_by(desc(UserPredictions.date_posted)).limit(2).all()
    predictions = [to_dict(prediction) for prediction in user_predictions]
    if user_predictions:
        return jsonify(status="true", predictions=predictions), 200
    else:
        return jsonify(status="false", error_mes="no predictions found..."), 200

if __name__ == '__main__':
    API.run(debug=True)
