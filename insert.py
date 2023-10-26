from app.database import SessionLocal, engine
import app.crud as crud
import app.schemas as schemas
import app.models as models

models.Base.metadata.create_all(bind=engine)

def insert_data():
    
    db = SessionLocal()

    crud.create_user(db, schemas.UserCreate(
        email="testuser@mail.com",
        password="password",
        username="testuser",
        first_name="test",
        last_name="user",
        birth_date="01/01/2000"
    ))

    crud.create_user(db, schemas.UserCreate(
        email="testuser2@mail.com",
        password="password",
        username="testuser2",
        first_name="test",
        last_name="user",
        birth_date="01/01/2000"
    ))

    id_user = crud.get_user_by_email(db, "testuser@mail.com").id

    crud.create_poi(db, schemas.POICreate(
        latitude=40.6301,
        longitude=-8.6562,
        name="testpoint1",
        description="testdesc1",
        type="bicycle-parking",
        picture_url=""
    ), id_user)

    crud.create_poi(db, schemas.POICreate(
        latitude=40.6300,
        longitude=-8.6563,
        name="testpoint2",
        description="testdesc2",
        type="bicycle-shop",
        picture_url=""
    ), id_user)

    crud.create_poi(db, schemas.POICreate(
        latitude=40.6304,
        longitude=-8.6542,
        name="testpoint3",
        description="testdesc3",
        type="drinking-water",
        picture_url=""
    ), id_user)

    crud.create_poi(db, schemas.POICreate(
        latitude=40.6315,
        longitude=-8.6292,
        name="testpoint4",
        description="testdesc4",
        type="toilets",
        picture_url=""
    ), id_user)

    crud.create_poi(db, schemas.POICreate(
        latitude=40.6314,
        longitude=-8.6129,
        name="testpoint5",
        description="testdesc5",
        type="bench",
        picture_url=""
    ), id_user)

    db.close()

insert_data()

print("==== Data inserted ====")
    

    