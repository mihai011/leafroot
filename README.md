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
    4. TODO: github pipeline for fast deployment.
    5. TODO: continue implement features of FAST-API to this project and exemplify them.

## Project environment set up (for vscode and docker users)
    

    1. Clone this repo in a directory..
    2. Open it in vscode.
    3. Install Remote-Containers extension.
    4. Using Ctrl+Shift+P select Remote-Container:Open Folder in Container
    5. Create the  python virtual envirorment: "make venv"
    6. Run the tests: "make test_simple" or "make test_parallel" for parallel tests

## Programming norms 

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

# Start
gunicorn app.app:app --workers <cores> -k uvicorn.workers.UvicornH11Worker --bind 0.0.0.0

# Create migration and apply it:

alembic revision --autogenerate -m "<migration_message>"
alembic upgrade head


# Test (pytest parallel for fast testing)
pytest -n <cores>
