Papi
====

REST API for Prismata related data.

Install as library
--------------------

    **pip install papi**

Development environment
-----------------------

0. Virtual environment (look at virtualenvwrapper):

   Create:

    mkvirtualenv papi

   Activate:

    workon papi

1. Install dependencies:

    pip install -r requirements-dev.txt

2. Run tests:

    ./runtests.sh

3. Run linters:

    ./runlinters.sh

4. No need to run migrations, but if you must:

    python manage.py migrate

Documenation
------------

- Go to any of this endpoints for more info:

    /api/docs/swagger/

    /api/docs/redoc/

- Or go to the docstring for LatestUnitVersionViewSet in units/views.py.
