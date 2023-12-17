from sqlalchemy.orm import Session
import app.models as models, app.schemas as schemas
from fastapi import HTTPException

SEP = "__"

def create_route(db: Session, route: schemas.RouteCreate, added_by: str):

    #check if route with same name exists
    db_route = db.query(models.Route).filter(models.Route.name == route.name).first()
    if db_route is not None:

        if(db_route.added_by == added_by):
            print(len(route.name.split(SEP)))
            print(len(route.points))
            if(len(route.name.split(SEP)) == len(route.points)):
                db.delete(db_route)
                db.commit()

    #create route
    db_route = models.Route(name=route.name,
                            added_by=added_by)
    try:
        db.add(db_route)
        db.commit()
        db.refresh(db_route)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    #create points and add route and points to route_point table
    for i in range(len(route.points)):
        db_point = models.Point(latitude=route.points[i].split(",")[0],
                                longitude=route.points[i].split(",")[1])
        try:
            db.add(db_point)
            db.commit()
            db.refresh(db_point)
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

        db_route.points.append(db_point)

    db.commit()
    db.refresh(db_route)

    return db_route

def get_routes_by_user(db: Session, user_id: str):
    db_routes = db.query(models.Route).filter(models.Route.added_by == user_id).all()

    routes = []
    points = []

    if db_routes is None:
        raise HTTPException(status_code=404, detail="Routes not found")
    else:
        for route in db_routes:
            for point in route.points:
                points.append(schemas.PointBase(latitude=point.latitude, longitude=point.longitude))
            routes.append(schemas.RouteGet(id=str(route.id),name=route.name, points=points))
            points = []

    routes_create = []
    routes_recorded = []

    #for each route get name
    for route in routes:
        names = route.name.split(SEP)
        points = route.points
        if(len(names) == len(points)):
            routes_create.append(schemas.RouteGet(id=str(route.id),name=route.name, points=points))
        else:
            routes_recorded.append(schemas.RouteGet(id=str(route.id),name=route.name, points=points))

    if len(routes_create) > 5:
        routes_create = routes_create[-5:]

    return {'created' : routes_create, 'recorded': routes_recorded}

def delete_route(db: Session, id: str, user_id: str):
    db_route = db.query(models.Route).filter(models.Route.id == id).first()
    if db_route is None:
        raise HTTPException(status_code=404, detail="Route not found")
    if db_route.added_by != user_id:
        raise HTTPException(status_code=401, detail="Not authorized")
    db.delete(db_route)
    db.commit()
    return db_route

def get_route(db: Session, id: str):
    db_route = db.query(models.Route).filter(models.Route.id == id).first()
    if db_route is None:
        raise HTTPException(status_code=404, detail="Route not found")
    return db_route