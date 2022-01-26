# ResidentialPortal-django-dynamoDB
A housing website using Django and DynamoNoSQL database

## Overview

This is a housing website named as "The Sunshine" Apartments. The front end is designed by using HTML, CSS, Javascript. DynamoDB is chosen as a backend database and Server-side application is written in DJango(Python) framework. We used Boto3 libraries to communicate with Dynamo DB database to make the application responsive. The application is listening on local port: 8080 when we run the command for manage.py from the terminal.


## Project Structure

AWS CLI installed with aws configuration for dynamoDB webservices.

By creating a Django project, Django creates a config directory for the project called "residential portal" which consists of files such as "_init_.py", "asgi.py", "settings.py", "urls.py", "wsgi.py"

We created an app directory called "dashboard" which consists of all files required for the main application of our project such as "_init_.py", "admins.py", "apps.py", "models.py", "tests.py", "urls.py" and "view.py"

dashboard/template/portal is where the .html files go.
.html files are as below:

amenities.html
amenities_reservation.html
dashboard.html
employeepage.html
FAQ.html
floorplans.html
gallery.html
importantn_numbers.html
index.html
maintenance.html
pay.html
payment_redirect.html
userpage.html


static/images/ is where images go. Syntax for images in .html is {% static '............' %} ex:
```
<img src="{% static 'images/homemarquee4.png' %}" alt="first" style="width:100%;">
```

dashboard/views.py is where we load the different views with any backend functions.

dashboard/urls.py is where we add our different paths.

Connection follows the below path for the home page:
```
residential portal/urls.py -> dashboard/urls.py -> '/' gets accessed from dashboard/views.py -> request is passed to "index.html"(home page)
```

## Instructions

Download the file from Github and go to directory CS157C-team2

Install Django:
```
pip3 install django 

```

Install Boto3:
```
pip3 install boto3
```

Install AWS:
```
$ pip3 install awscli --upgrade --user
```

Make sure to export the path to bash profile
``` 
Reference: https://docs.aws.amazon.com/cli/latest/userguide/install-macos.html#awscli-install-osx-path 
```

Start server on "localhost:8000" using 
```
python manage.py runserver
```

Open a web browser and navigate to local hosted server -> http://127.0.0.1:8000/ for the home page.

## References:

Following are a few websites that are being referred to build this website: 

Frontend:
```
https://github.com/nehagadge/Login-Portal/blob/master/home.ejs 
https://github.com/sniklaus/teaching-webdev
```

Django Framework - Server side application:
```
https://docs.djangoproject.com/en/3.2/
```

Boto3 Framework - Libraries to connect to DynamoDB:
```
https://boto3.amazonaws.com/v1/documentation/api/latest/guide/dynamodb.html
```

AWS DynamoDB - Backend database:
```
https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/WorkingWithDynamo.html
```



