#Defines the app thats a part of the app package; runs the application
from app import app, db
from app.models import User, Order
"""
Run using *python3 menu.py*
export FLASK_APP=microblog.py 
^Use so you can type flask run in the terminal

pip install flask
pip install python-dotenv
pip install flask-wtf
pip install flask-sqlalchemy
pip install flask-migrate
pip install flask-login
pip install email-validator
pip install wtforms_components
pip install flask-mail
pip install pyjwt
pip install Flask-JSGlue  
pip install requests  
pip install awsebcli
1. Flask
2. So you can keep environmental variables (like FLASK_APP) in .flaskenv file above app folder 
3. For making web forms
4. Translate SQL tables/demands into code related stuff (classes, objects)
5. So you can save changes to database after making them (to initialize: *flask db init*)
    1. Adds each change into a migration repository (flask db migrate -m *explanation*)
    2. Applies migrations to database in order they were added (flask db upgrade)
    Use command *flask db downgrade* to get rid of update
    For big updates (adding another modelx)
6. To keep users logged in thru dif pages in website
7. To validate emails (It's needed tho not used in form)
8. To get validator DateRange, and others
9. Sending emails
10. Security for emails
11. To use Flask.url_for() in js code
    1. Have to put {{ JSGlue.include() }} in head
12. for Ajax, json python - js connection
13. AWS
"""
@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Order': Order}

if __name__ == "__main__":
    app.run(debug=True)