########## Add to DB ##########
def add_db(db, element):
    db.add(element)
    db.commit()
    db.refresh(element)

########## Update db ##########
def update_db(db):
    db.commit()

########## Delete db ##########
def delete_db(db, element):
    db.delete(element)
    db.commit()
