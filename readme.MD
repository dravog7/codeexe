# Code executor

## WHAT IS IT

- a django project based on a django app that uses celery to handle task queue and runs submitted programs to be evaluated to a given input and output.

## DEPENDENCIES

- RabbitMq server (Celery broker)

- modules in requirements.txt

## HOW TO INSTALL

- be sure to have python3 and pip3 installed

-run install.sh (also set superuser to see database from django admin page)

## HOW TO TEST

- ./manage.py test


## HOW TO RUN

- run run.sh

- Use ctrl+C to exit

- goto localhost:8000/admin/

- you can add submissions here. there is only 1 question initially. Its output can be found in execution/questions/1.
- once u add a submission u get its id (its name would be like submission object(id))
- goto localhost:8000/id/ to run your submission
- check in admin board for the result
- (UI not built yet)