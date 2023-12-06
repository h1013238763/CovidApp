from flask import Blueprint, jsonify, request
from .API_CONTROLLER import API_CONTROLLER

API = Blueprint('API', __name__)

controller = API_CONTROLLER()

# Endpoint to predict COVID-19 risk based on user-input symptoms and demographic information
# Method: POST
# Expected input: JSON containing various health and symptom-related fields
@API.route("/api/predict", methods=["POST"])
def predict():
    try:
        controller.preprocess_request_data(request.get_json())
        return jsonify({"modelPrediction_v2": round(controller.predict())})
    except Exception as e:
        return jsonify({"error": str(e)})

# Endpoint for user login
# Method: POST
# Expected input: JSON containing "username" and "password"
@API.route('/api/login', methods=['POST'])
def login():
    return controller.preprocess_request_data(request.get_json()).login()

# Endpoint to create a new user account
# Method: POST
# Expected input: JSON containing "username", "password", and "email"
@API.route('/api/create_account', methods=['POST'])
def createAccount():
    return controller.preprocess_request_data(request.get_json()).create_account()

# Endpoint for initiating the password recovery process
# Method: POST
# Expected input: JSON containing "username"
@API.route('/api/forgot_password', methods=['POST'])
def forgotPassword():
    return controller.preprocess_request_data(request.get_json()).forgot_password()

# Endpoint for changing the user's password
# Method: POST
# Expected input: JSON containing "username", answers to security questions, and "new_password"
@API.route('/api/change_password', methods=['POST'])
def verifySecurityQuestions():
    return controller.preprocess_request_data(request.get_json()).change_password()

# Endpoint for submitting a new blog post request
# Method: POST
# Expected input: JSON containing "username", "title", and "body" of the blog post
@API.route('/api/add_request_blog', methods=['POST'])
def addRequestBlog():
    return controller.preprocess_request_data(request.get_json()).addRequestBlog()

# Endpoint to retrieve verified blog posts
# Method: GET
# No input expected; returns a list of verified blog posts
@API.route('/api/get_blog_posts', methods=['GET'])
def getBlogPosts():
    return controller.getBlogPosts()

# Endpoint to retrieve a user's prediction log
# Method: POST
# Expected input: JSON containing "username"
@API.route('/api/get_user_predictions_log', methods=['POST'])
def getUserPredictionsLog():
    return controller.preprocess_request_data(request.get_json()).getUserPredictionsLog()


# Endpoint to dynamically load different pages based on the URL parameter
# Method: GET
# URL Parameter: <page> - a string indicating the specific page to be loaded
# Description: 
#   This endpoint responds to GET requests and uses a URL parameter to determine
#   which page to load. It delegates the responsibility of loading the correct HTML
#   content to the `NAV_loadPage` method of the `controller`. The `page` parameter
#   is passed to this method, which then returns the appropriate HTML content
#   based on the provided parameter. This setup allows for a flexible page loading
#   mechanism where the specific page is determined at runtime based on the client's request.
@API.route('api/load_page/<page>')
def load_page(page):
    # Depending on the page parameter, load the appropriate HTML content
    return controller.NAV_loadPage(page)

if __name__ == '__main__':
    API.run(debug=False)
