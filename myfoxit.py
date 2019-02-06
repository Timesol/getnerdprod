from app import create_app, db, cli
import os
from app.models import User,City,Task


app=create_app()
cli.register(app)


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'City': City, 'User':User, 'Task': Task}




