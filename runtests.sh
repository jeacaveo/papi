# Run tests and generate coverage report.

coverage run --source=. manage.py test -v 2
coverage report -m
