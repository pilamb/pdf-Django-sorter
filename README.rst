========================
A pdf sorter with Django 
========================


What?
-----


A classifing tool for pdf files.

When a file is uploaded its capable of extracting, if those methadata exist, the following info:

- Title
- Author/s
- Size (bytes)
- If protected by password
- Software used to make the file
- Pages number
- Commercial Code
- Date when it was created
- Date if it was modified

Also:

- URL, a website realated with the pdf
- Hash authomatically added when uploaded (md5)
- Tags (django-tagulous)


Basic operations can be achieved: upload a file, delete, edit, listing, and detail of each file, plus tags management.
Also some satistics of usage can be viewed.

Finally it is stored at a Postgres database called 'pdfwarehouse'.


Install
-------

SECRET_KEY is not shared, you need to create an env var called DJANGO_SECRET_KEY or the app wont work.

Its recommended to use virtualenv::
        
        mkrprogect <give-a-name>

Versions::

        Python 2.7.X y Django>=1.9

Extra needed modules::

        pip install -r requirements.txt

Its mandatory to create a posgres database::

        createdb pdfwarehouse

or::

        /usr/local/pgsql/bin/createdb pdfwarehouse

Launch the website::
        
        python manage.py runserver

Visit this link, you should see the content::

        http://127.0.0.1:8000

Access the admin at::

        http://127.0.0.1:8000/admin

Where a root user is needed, create one with::

        python manage.py createsuperuser


Main stack
----------

* Django
* Cookiecutter-django
* Chardet
* Pdfminer
* PostgreSQL
* Bootstrap


TODOS
-----

- It could be extended to use dropbox, owncloud, etc.
- Some not-unicode, not-latin might make the unicode detection fail.
- A second version will generate API REST. Its installed but not used.
