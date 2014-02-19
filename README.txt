 ~~ Curriculum Analysis and Tracking Application ~~
 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
 ~ 2013/2014  Software Engineering Design Project ~
 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- make sure you have the environment prepped for the application (correct versions of python, django, and other various libraries)

- run ‘manage.py syncdb’ if there is no database created
- afterwards, run ‘populate_db.py’ to populate the new database with test entries
(if it throws an error, make sure python PATH is set to project.settings)
(run the following command in terminal/unix based machines ‘export DJANGO_SETTINGS_MODULE=“project.settings”’)

- if there is a database (or once its made), run ‘manage.py runserver’ to access the application on the localhost (localhost/curriculum)