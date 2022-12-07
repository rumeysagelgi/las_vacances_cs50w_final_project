
# LAS VACANCES SUITES



## Video Demo:
https://youtu.be/wJMPBBKcle4



## Description:
Las Vacances Suites is a web application that you can find suites (houses/flats/rooms) from all around the world which are available to book, similar to Airbnb. You also can view suites' reviews and ratings to understand what people who stayed there before think about their experience. It is even possible for users to create an account to leave reviews and ratings, create lists, and add their favorite suites to those lists as well as visit each other's profiles. Or, if they have a place that they want to feature on the application, they can add a new suite for booking to the database as well.



## Distinctiveness and Complexity:
Las Vacances Suites is not similar to any project we have already created through the course. It is not a commercial or encyclopedia website as well as neither an e-mail nor social media application. Also we never created:

 - multiple static JavaScript files
 - invisible containers which also can feature cover images such as the suites display field
 - custom removable favorites lists that users can create and name based on their liking
 - profiles that allow users to upload an avatar based on image link and to see other users' entire lists and reviews

 - and handled computations in Python views like finding the average of all ratings

during the course.


In terms of complexity, it was much more difficult to build than all the projects we have done so far. The application includes Django with several models for the back-end and multiple JavaScript files for the front-end:

 - I created three separate JavaScript files: one for searching suites and handling interactivity and functionality of the display area, one for allowing users to edit their reviews, and another one for resizing cover images.
 - Using Python language for the back-end, I created six different models and fifteen URL routes for the application. Especially inserting user profile lists and reviews available to others feature was quite complicated to accomplish and took such an effort.
 - I also added success and error *alerts* instead of simple individual pages to notify users.


Las Vacances Suites is made from scratch following the requirements provided as explained above.



## How to Run:
Go inside `/final_project` folder on your terminal and execute the following in order:

 - `python manage.py makemigrations` to generate the necessary files for the setup.
 - `python manage.py migrate` to execute the setup files that have created.
 - `python manage.py runserver` to run the server.

The default server address is http://127.0.0.1:8000/. Click on it after the server has run to open the application.

In order to setup Django Admin Interface (which is optional), go inside `/final_project` folder on your terminal and execute `python manage.py createsuperuser` and follow the instructions.



## Languages & Frameworks Used in This Project:

***Back-End:***
 - Python
 - Django
 - SQL

***Front-End:***
- JavaScript
- HTML + Jinja
- CSS
- Bootstrap



## Files:

### Static:

***image.js:*** Contains JavaScript function that resizes suite cover images.

***index.js:*** Contains JavaScript functions that allow users to search for and load suites, and then allow to click on them to go to that suite's page.

***review.js:*** Contains JavaScript functions that allow users to edit their reviews, and cancel or confirm the edit.

***styles.css:*** Specialized styling for the entire application. Specifies the navbar, header and buttons as well as index page, suite page, profile page, and review page.



### Templates:

***add_list.html:*** The page where users can create a new list for adding their favorite suites to.

***add_suite.html:*** The page where users, who want to display their place, can add a new suite into the application database.

***apology.html:*** Allows apology alerts.

***index.html:*** The page where users are redirected as soon as they run the application. Contains the logo, the search box and the display area.

***layout.html:*** Where the main HTML code is stored and all other template files extend from thanks to Jinja syntax.

***list.html:*** The page where displays a user list.

***lists.html:*** The page where displays all lists of a user.

***login.html:*** The page where users can log in to the application with their accounts.

***profile.html:*** The page where displays a user profile.

***register.html:*** The page where users can register an account.

***review.html:*** The page where displays a user review.

***suite_reviews.html:*** The page where displays all reviews of a suite.

***suite.html:*** The page where displays a suite.

***user_reviews.html:*** The page where displays all reviews from a user.



### Python:

***admin.py:*** Contains registered models for Django Admin Userface.

***models.py:*** Contains 6 different models of the application - User, Suite, List, List_item, Rating, Review

***urls.py:*** Contains paths for application and authentication routes.

***views.py:*** Contains all the views and entire back-end code.



### Others:

***db.sqlite3:*** The database of the application where entire data is stored. Here is the schema of the database:

 - CREATE TABLE IF NOT EXISTS lasvacances_user (
		id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
		username VARCHAR(150) NOT NULL UNIQUE,
		email VARCHAR(254) NOT NULL,
		password VARCHAR(128) NOT NULL,
		date_joined DATETIME NOT NULL,
		last_login DATETIME NULL,
		is_superuser BOOL NOT NULL,
		is_staff BOOL NOT NULL,
		is_active BOOL NOT NULL,
		avatar VARCHAR(200) NOT NULL
	);

 - CREATE TABLE IF NOT EXISTS lasvacances_suite (
		id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
		title VARCHAR(255) NOT NULL,
		address VARCHAR(255) NOT NULL,
		details TEXT NOT NULL,
		price VARCHAR(50) NOT NULL,
		image VARCHAR(200) NOT NULL
	);

 - CREATE TABLE IF NOT EXISTS lasvacances_review (
		id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
		title VARCHAR(255) NOT NULL,
		review TEXT NOT NULL,
		rating INTEGER NOT NULL,
		author_id BIGINT NOT NULL REFERENCES lasvacances_user (id) DEFERRABLE INITIALLY DEFERRED
		suite_id BIGINT NOT NULL REFERENCES lasvacances_suite (id) DEFERRABLE INITIALLY DEFERRED
	);

 - CREATE TABLE IF NOT EXISTS lasvacances_rating (
		id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
		rating DECIMAL NOT NULL,
		suite_id BIGINT NOT NULL UNIQUE REFERENCES lasvacances_suite (id) DEFERRABLE INITIALLY DEFERRED
	);

 - CREATE TABLE IF NOT EXISTS lasvacances_list (
		id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
		name VARCHAR(255) NOT NULL,
		author_id BIGINT NOT NULL REFERENCES lasvacances_user (id) DEFERRABLE INITIALLY DEFERRED
	);

 - CREATE TABLE IF NOT EXISTS lasvacances_list_item (
		id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
		list_id BIGINT NOT NULL REFERENCES lasvacances_list (id) DEFERRABLE INITIALLY DEFERRED,
		suite_id BIGINT NOT NULL REFERENCES lasvacances_suite (id) DEFERRABLE INITIALLY DEFERRED
	);

***requirements.txt:*** Lists the packages installed in the application.



## Requirements:
In a `README.md` in your project’s main directory, include a writeup describing your project *****(PLEASE FIND HERE: [Description](#description))*****, and specifically your file **MUST** include all of the following:

- **Under its own header within the `README` called `Distinctiveness and Complexity`**: Why you believe your project satisfies the distinctiveness and complexity requirements, mentioned above. *****(PLEASE FIND HERE: [Distinctiveness and Complexity](#distinctiveness-and-complexity))*****

- What’s contained in each file you created. *****(PLEASE FIND HERE: [Files](#files))*****

- How to run your application. *****(PLEASE FIND HERE: [How to Run](#how-to-run))*****

- Any other additional information the staff should know about your project. *****CLARIFICATION: This application does not let users to book a suite directly via the application.  In order to book a suite of their choice, users can find contact informations in Details section of Suite pages.*****

- Though there is not a hard requirement here, a `README.md` in the neighborhood of 500 words is likely a solid target, assuming the other requirements are also satisfied. *****IMPORTANT: This README file consists of over 1.000 words.*****
