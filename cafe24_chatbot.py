import os
from dotenv import load_dotenv

from flask_migrate import Migrate, upgrade
from cafe24_app import create_app, db
from cafe24_app.models import Mall


dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db)

@app.shell_context_processor
def make_shell_context():
    return dict(db=db, Mall=Mall)