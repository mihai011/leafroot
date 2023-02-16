# fast-api-full
Hello and welcome to a FastAPI template base project.
This repo serves as base project for everyone to use and build upon
new applications.

## Features

    1. Everything is asynchronous. Since pretty much all web applications are at their core I/O bound, this project makes
    it easier for new developers to read, understand and write
    asynchronous code. And by "everything" I mean everything:
        - asynchronous controllers
        - asynchronous connections to a postgresql database
        - asynchronous and parallel tests
    2. Alembic made migrations for the database.
    3. Docker containers and local environment already set up.
    4. Circle CI config for testing implemented.
    6. Implemented health check.
    7. TODO: Add Mongo and other NO-SQLs and Apache Kafka to app.
    8. TODO: Circle CI pipeline for fast deployment to AWS, ETA and Heroku.
    9. TODO: Add chat integration using socketio
    10. Implement healthcheck. (done)
    11. TODO: Implement stress test.
    12. TODO: Mock mongo database for test


## Project environment set up (for vscode and docker users)


    1. Clone this repo in a directory..
    2. Open it in vscode.
    3. Install Dev-Containers extension.
    4. Export the variabile ENV_FILE to the newly created .env_user file.
    5. Run "make start_full_services"
    6. Attack to the "backend" service using the vscode extension.



## Programming norms

   1.Please add docstring on each new file, class, and functions to stipulate their purpose and functionality.
   An example for one is down below:

        ```
        def add_binary(a, b):
            '''
            Returns the sum of two decimal numbers in binary digits.

                    Parameters:
                            a (int): A decimal integer
                            b (int): Another decimal integer

                    Returns:
                            binary_sum (str): Binary string of the sum of a and b
            '''
            binary_sum = bin(a+b)[2:]
            return binary_sum


        print(add_binary.__doc__)
        ```
    2. To check correctitude of the code format use "make lint" to get a score for your style on the project, Always push for a 10!
    3. Use the following commands for some help:
       1. "make format" - formats your code using the "black" functionality
       2. "make typehint" - check for mis typing variables
    4. Use the command "make coverage" or "make coverage_parallel" to
    verify what percentage of your code is checked, Push for 100%!

# Create migration and apply them:

alembic revision --autogenerate -m "<migration_message>"
alembic upgrade head
