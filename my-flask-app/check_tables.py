# check_tables.py
from app import create_app, db
from sqlalchemy import inspect

app = create_app('development')
app.app_context().push()

inspector = inspect(db.engine)
tables = inspector.get_table_names()

print("Tables in the database:")
for table in tables:
    print(table)
