from database import *

with Database() as db:
    db.execute('select * from user;')
    results = db.fetchall()
    print(results)