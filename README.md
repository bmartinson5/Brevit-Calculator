README

Author: Benjamin Martinson

Note: port used is 5000 (specified at bottom of api.py)


For this project, a frontend was added to make it easier to access
the api. Now, to access the api, follow the instructions below:

First:

	'docker-compose up' from within current directory (same directory as README file)


Or try:

	'pip3 install requirements.txt'
	'python3 api.py'


NOTE: You can't use the api if you dont have a token, and you can't get a token if
      your not logged in.


To Register a new username and password:
	
	When running on default <host>:<port>  == http://0.0.0.0:5000

	Try url: http://localhost:5000/api/register

	-This should display templates/register.html

	-Submitting new username and password will add to the database and 
	 then redirect to login page (if already logged in to a user it will display token)


Login Page:

	url: http://localhost:5000/api/login

	-Once logged in a token will be displayed


Logout Page:

	url: http://localhost:5000/api/logout

	-Logging out will make you lose your access to token url


Display Token:

	url: http://localhost:5000/api/token

	-Will redirect to login url if not already logged in
	
	
Get an API resource (need a token first):

	curl -u <token>:x -i -X GET <host>:<port>/<api route> 

	-When successful, the api resource will be returned in JSON
	-If the token is incorrect, an error (401) is output

