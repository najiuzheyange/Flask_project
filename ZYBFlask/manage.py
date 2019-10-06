from app import create,models
from flask_script import Manager
from flask_migrate import MigrateCommand,Migrate


app=create()
manager = Manager(app)
migrate=Migrate(app,models)


manager.add_command("db",MigrateCommand)

if __name__ == "__main__":
    manager.run()