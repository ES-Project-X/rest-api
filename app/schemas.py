from pydantic import BaseModel


class UserBase(BaseModel):
    email: str


class UserLogin(UserBase):
    password: str


class UserCreate(UserBase):
    username: str
    first_name: str
    last_name: str
    birth_date: str


class UserEdit(UserBase):
    email: str = None
    username: str = None
    password: str = None
    new_password: str = None
    first_name: str = None
    last_name: str = None
    image_url: str = None


class PointBase(BaseModel):
    latitude: float
    longitude: float


class POICreate(PointBase):
    name: str
    description: str
    type: str
    picture_url: str


class POIEdit(BaseModel):
    id: str
    description: str = None
    picture_url: str = None


class POIRateExistence(BaseModel):
    id: str
    rating: bool


class UserPOIBase(BaseModel):
    poi_id: str


class UserPOIManage(UserPOIBase):
    rating: bool


class RouteCreate(BaseModel):
    name: str
    points: list[str]


class RouteEdit(BaseModel):
    id: str
    description: str = None
    picture_url: str = None


class UserRouteBase(BaseModel):
    route_id: str


class UserRouteManage(UserRouteBase):
    rating: bool


class ClusterRequest(BaseModel):
    clusters: list[list[float]] = None


class RouteGet(BaseModel):
    name: str
    points: list[PointBase]


class POIRate(BaseModel):
    id: str
    status: bool

class FileUpload(BaseModel):
    base64_image: str
    image_type: str