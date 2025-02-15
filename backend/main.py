# from application import workers
# import os
# from flask import Flask, jsonify
# from application.database import db
# from flask_jwt_extended import JWTManager
# from flask_cors import CORS

# app = Flask(__name__)

# # Ensure the directory exists for the database
# db_dir = os.path.dirname("C:/Users/Arnav Mehta/Desktop/Household help/backend/database_file/household_app.db")
# if not os.path.exists(db_dir):
#     os.makedirs(db_dir)

# # Configuration
# app.config["JWT_SECRET_KEY"] = "secret"  # Change this in production!   C:\Users\Arnav Mehta\Desktop\My Works\Household help\backend\database_file
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.abspath("C:/Users/Arnav Mehta/Desktop/My Works/Household help/backend/database_file/household_app.db")

# app.config["CACHE_TYPE"] = "RedisCache"
# app.config["CACHE_REDIS_URL"] = 'redis://localhost:6379/3'
# app.config["CACHE_DEFAULT_TIMEOUT"] = 300  # 5 minute
# app.config["REDIS_URL"] = 'redis://localhost:6379'
# app.config["broker_url"] = 'redis://localhost:6379/0'
# app.config["result_backend"] = 'redis://localhost:6379/0'
# app.config["broker_connection_retry_on_startup"] = True

# app.app_context().push()



# # Initialize extensions




# db.init_app(app)
# jwt_mgr = JWTManager(app)


# app.config["CELERY_BROKER_URL"] = "redis://localhost:6379/1"
# app.config["CELERY_RESULT_BACKEND"] = "redis://localhost:6379/2"


# # CORS setup
# CORS(app, resources={r"/*": {"origins": "http://localhost:8080"}})
# app.app_context().push()

# # Create tables if they don't exist
# with app.app_context():
#     celery=workers.celery
#     celery.conf.update(broker_url=app.config["CELERY_BROKER_URL"],result_backend=app.config["CELERY_RESULT_BACKEND"])
#     celery.Task=workers.ContextTask
#     app.app_context().push()


#     from application.routers import *  # Ensure this file imports your routes correctly
#     from application.models import *  # Ensure your models are defined properly
#     db.create_all()
    

# # Sample error handler
# @app.errorhandler(500)
# def internal_error(error):
#     return jsonify({"error": "Internal Server Error", "message": str(error)}), 500

# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=8000, debug=True)






















# from application import workers
# import os
# from flask import Flask, jsonify
# from application.database import db
# from flask_jwt_extended import JWTManager
# from flask_cors import CORS
# from application.tasks import daily_reminder, monthly_report  # Explicitly import tasks

# app = Flask(__name__)

# # Ensure the directory exists for the database
# db_dir = os.path.dirname("C:/Users/Arnav Mehta/Desktop/Household help/backend/database_file/household_app.db")
# if not os.path.exists(db_dir):
#     os.makedirs(db_dir)

# # Configuration
# app.config["JWT_SECRET_KEY"] = "secret"  # Change this in production!   C:\Users\Arnav Mehta\Desktop\My Works\Household help\backend\database_file
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.abspath("C:/Users/Arnav Mehta/Desktop/My Works/Household help/backend/database_file/household_app.db")

# app.config["CACHE_TYPE"] = "RedisCache"
# app.config["CACHE_REDIS_URL"] = 'redis://localhost:6379/3'
# app.config["CACHE_DEFAULT_TIMEOUT"] = 300  # 5 minute
# app.config["REDIS_URL"] = 'redis://localhost:6379'
# app.config["broker_url"] = 'redis://localhost:6379/0'
# app.config["result_backend"] = 'redis://localhost:6379/0'
# app.config["broker_connection_retry_on_startup"] = True

# app.app_context().push()



# # Initialize extensions




# jwt_mgr = JWTManager(app)


# app.config["CELERY_BROKER_URL"] = "redis://localhost:6379/1"
# app.config["CELERY_RESULT_BACKEND"] = "redis://localhost:6379/2"


# # CORS setup
# CORS(app, resources={r"/*": {"origins": "http://localhost:8080"}})



# app.app_context().push()

     
# db.init_app(app)
# app.app_context().push()


# celery=workers.celery
# celery.conf.update(broker_url=app.config["CELERY_BROKER_URL"],result_backend=app.config["CELERY_RESULT_BACKEND"])
# celery.Task=workers.ContextTask
# app.app_context().push()


# from application.routers import *  # Ensure this file imports your routes correctly
# from application.models import *  # Ensure your models are defined properly
    

# # Sample error handler
# @app.errorhandler(500)
# def internal_error(error):
#     return jsonify({"error": "Internal Server Error", "message": str(error)}), 500

# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=8000, debug=True)
import os
from flask import Flask, jsonify
from application.database import db
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from application.tasks import daily_reminder, monthly_report  # Explicitly import tasks
from application import workers
import logging
from application.cache import cache

# Logging setup
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

# Ensure the directory exists for the database
db_dir = os.path.dirname(os.path.abspath("C:/Users/Arnav Mehta/Desktop/My Works/Household help/backend/database_file"))
if not os.path.exists(db_dir):
    os.makedirs(db_dir)

# Configuration
app.config["JWT_SECRET_KEY"] = "secret"  # Change this in production!
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.abspath("C:/Users/Arnav Mehta/Desktop/My Works/Household help/backend/database_file/household_app.db")

app.config["CACHE_TYPE"] = "RedisCache"
app.config["CACHE_REDIS_URL"] = 'redis://localhost:6379/3'
app.config["CACHE_DEFAULT_TIMEOUT"] = 300  # 5 minute timeout
app.config["REDIS_URL"] = 'redis://localhost:6379'
app.config["broker_url"] = 'redis://localhost:6379/0'
app.config["result_backend"] = 'redis://localhost:6379/0'
app.config["broker_connection_retry_on_startup"] = True

# Celery Configuration
app.config["CELERY_BROKER_URL"] = "redis://localhost:6379/1"
app.config["CELERY_RESULT_BACKEND"] = "redis://localhost:6379/2"

# CORS setup
CORS(app, resources={r"/*": {"origins": "http://localhost:8080"}})

# Initialize extensions
jwt_mgr = JWTManager(app)

# Set up Celery
celery = workers.celery
celery.conf.update(broker_url=app.config["CELERY_BROKER_URL"], result_backend=app.config["CELERY_RESULT_BACKEND"])
celery.Task = workers.ContextTask

# Initialize the database
db.init_app(app)

# Create tables if they don't exist
with app.app_context():
    db.create_all()  # Only needed if tables are not already created

# Push app context only once after initialization
app.app_context().push()


cache.init_app(app)
app.app_context().push()

# Import routes and models after app context is set up
from application.routers import *  # Ensure this file imports your routes correctly
from application.models import *  # Ensure your models are defined properly

# Sample error handler
@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal Server Error", "message": str(error)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
