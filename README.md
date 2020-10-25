# stigler_app

<p>Try it <a href="http://35.197.229.127:8000">Here</a></p>
 
sign up or use the already preconfigured username:edoardo password:stigler01

<p>[setup on local machine]</p>

- git clone
- install conda (https://www.anaconda.com/products/individual)
- open terminal (there should be "(base)" at the beginning of the line)
- conda env create stigler_app --file environment.yml
- conda activate stigler app
- cd into stigler_app/stigler_app
- python manage.py migrate
- python manage.py createsuperuser (create a superuser account)
- python manage.py runserver
- http://127.0.0.1:8000/init to initialise the database with a few values
- http://127.0.0.1:8000/login and login with superuser account
- click on dashboard
- click on "import local" (bottom right)
- database has been filled in with default values from a local excel file
- logout
<p>[end setup on local machine]</p>

<p>available users:</p>

- user:alessandra pwd:stigler01  (customer user)
- user:olivia pwd:stigler01 (customer user)
- user:edoardo pwd:stigler01  (staff user)

everything set now, you can generate a new menu in "Today's menu" or change the target macros in the "User" page
