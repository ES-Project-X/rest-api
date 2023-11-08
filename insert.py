from app.database import SessionLocal, engine
from crud import user as crud_user, poi as crud_poi
import app.schemas as schemas
import app.models as models

models.Base.metadata.create_all(bind=engine)

def insert_data():
    
    db = SessionLocal()

    crud_user.create_user(db, schemas.UserCreate(
        email="testuser@mail.com",
        password="password",
        username="testuser",
        first_name="test",
        last_name="user",
        birth_date="01/01/2000"
    ))

    crud_user.create_user(db, schemas.UserCreate(
        email="testuser2@mail.com",
        password="password",
        username="testuser2",
        first_name="test",
        last_name="user",
        birth_date="01/01/2000"
    ))

    id_user = crud_user.get_user_by_email(db, "testuser@mail.com").id

    crud_poi.create_poi(db, schemas.POICreate(
        latitude=40.6301,
        longitude=-8.6562,
        name="testpoint1",
        description="testdesc1",
        type="bicycle-parking",
        picture_url="https://stplattaprod.blob.core.windows.net/liikenneprod/styles/og_image/azure/pyorapysakointi-jenni-huovinen.jpg?h=c176692e&itok=4KvwzNO_"
    ), id_user)

    crud_poi.create_poi(db, schemas.POICreate(
        latitude=40.6300,
        longitude=-8.6563,
        name="testpoint2",
        description="testdesc2",
        type="bicycle-shop",
        picture_url="https://images.squarespace-cdn.com/content/v1/5b330319af2096cdc763f454/1639764191013-JSG1K03LOLIWDNEYQ93H/IMG_1882.jpg?format=2500w"
    ), id_user)

    crud_poi.create_poi(db, schemas.POICreate(
        latitude=40.6304,
        longitude=-8.6542,
        name="testpoint3",
        description="testdesc3",
        type="drinking-water",
        picture_url="https://img.freepik.com/fotos-premium/bebedouro-de-rua_321831-4277.jpg"
    ), id_user)

    crud_poi.create_poi(db, schemas.POICreate(
        latitude=40.6315,
        longitude=-8.6292,
        name="testpoint4",
        description="testdesc4",
        type="toilets",
        picture_url="https://www.jpn.up.pt/wp-content/uploads/2018/02/wc_p%C3%BAblica_3_06-de-fevereiro-de-2018.jpg"
    ), id_user)

    crud_poi.create_poi(db, schemas.POICreate(
        latitude=40.6314,
        longitude=-8.6129,
        name="testpoint5",
        description="testdesc5",
        type="bench",
        picture_url="https://oilhavense.com/wp-content/uploads/2019/09/banco-de-jardim.jpg"
    ), id_user)

    db.close()

insert_data()

print("==== Data inserted ====")
    

    