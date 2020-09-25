from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from app import create_app
from models import db

APP = create_app()
migrate = Migrate(APP, db)
manager = Manager(APP)

manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    db.init_app(APP)
    manager.run()
