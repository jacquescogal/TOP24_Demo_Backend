fastapi app

to run:
uvicorn main:app --reload


Client (frontend):
- ui/ux
- user input


Server (backend):
- api router
    - Needs to accept certain parameters (username,password)
    - Validate the parameters
        - checking in database if username exists
        - checking if password matches
    - If valid, return a token

Database:

- database
