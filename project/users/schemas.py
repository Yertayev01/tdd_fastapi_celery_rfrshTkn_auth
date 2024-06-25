from pydantic import BaseModel, EmailStr, conint
from typing import Optional
from datetime import datetime
import typing as t

class UserBody(BaseModel):

    username: str
    email: str

class Token(BaseModel):
    user_id: int
    access_token: str
    token_type: str

class TokenData(BaseModel):
    user_id: Optional[int] = None

class User(BaseModel):
    user_id: int
    email: str
    socialKind: str
    name: str
    gender: str
    level: int
    self_intro: str
    # profile_images_path: str
    # profile_image_name: str
    
#profile image
class PhotoCreate(BaseModel):
    #user_id: int
    photo_url: str

class PhotoReturn(BaseModel):
    id: int
    user_id: int
    photo_url: str
    reg_dt: datetime
    mod_dt: datetime
    
    class ConfigDict:
        from_attributes = True
#user
class UserBase(BaseModel):
    username: str
    is_admin: t.Optional[bool] = False
  
class UserCreate(BaseModel):
    USER_ID: str
    LOGI_CD: str = "N"
    PSSWRD: str
    USER_NM: str
    EMAIL: str
    PHONE_NO: int
    REG_USER_ID: str = None
    MOD_USER_ID: str = None
    #self_intro: Optional[str] = None
    #photos: PhotoReturn

    
class UserAdminCreate(BaseModel):
    username: str
    password: str
    is_admin: t.Optional[bool] = False

class UserReturn(BaseModel):
    USER_MNG_ID: int
    EMAIL: str
    #USCL_CD: t.Optional[bool] = False

    class ConfigDict:
        from_attributes = True

class UserProfileReturn(BaseModel):
    user_id: int
    username: str
    self_intro: str

    class ConfigDict:
        from_attributes = True
    
class UserUpdate(UserBase):
    username: str
    password: t.Optional[str] = None

class UserAdminUpdate(UserBase):
    username: str
    is_admin: t.Optional[bool] = False
    password: t.Optional[str] = None

class UserLogin(BaseModel):
    EMAIL: str
    PSSWRD: str

#object
class AssetList(BaseModel):
    ASSET_ID: str
    ASSET_TITLE: str
    DESCRIPTION: str
    # save like comment count

class Asset(BaseModel):
    ASSET_ID: str
    ASSET_TITLE: str
    DESCRIPTION: str

#anchor
class AnchorList(BaseModel):
    ANCHOR_TITLE: str
    LATITUDE: float
    LONGITUDE: float

class SearchAnchor(BaseModel):
    ANCHOR_ID: str
    USER_MNG_ID: int
    ANCHOR_TITLE: str
    LATITUDE: float
    LONGITUDE: float
    DISTANCE: float

#video
class VideoReturn(BaseModel):
    VIDEO_ID: str
    VIDEO_TITLE: str
    VIDEO_DESCRIPTION: str
    REG_DT: datetime
    
    class ConfigDict:
        from_attributes = True

class VideoFile(BaseModel):
    video_file: str

    class ConfigDict:
        from_attributes = True


class VideoUpdate(BaseModel):
    VIDEO_TITLE: t.Optional[str] = None
    VIDEO_DESCRIPTION: t.Optional[str] = None


#comment
class ObjectCommentCreate(BaseModel):
    object_id: int
    comment: str

class ObjectCommentReturn(BaseModel):
    id: int
    object_id: int
    owner_id: int
    comment: str
    reg_dt: datetime
    mod_dt: datetime

    class ConfigDict:
        from_attributes = True


class NodeCommentCreate(BaseModel):
    node_id: int
    comment: str

class NodeCommentReturn(BaseModel):
    id: int
    node_id: int
    owner_id: int
    comment: str
    reg_dt: datetime
    mod_dt: datetime

    class ConfigDict:
        from_attributes = True

#like
class ObjectLikeCreate(BaseModel):
    object_id: int

class ObjectLikeReturn(BaseModel):
    id: int
    object_id: int
    owner_id: int
    reg_dt: datetime
    mod_dt: datetime

    class ConfigDict:
        from_attributes = True

class NodeLikeCreate(BaseModel):
    node_id: int

class NodeLikeReturn(BaseModel):
    id: int
    node_id: int
    owner_id: int
    reg_dt: datetime
    mod_dt: datetime

    class ConfigDict:
        from_attributes = True

# save
class ObjectSaveCreate(BaseModel):
    object_id: int

class ObjectSaveReturn(BaseModel):
    id: int
    object_id: int
    owner_id: int
    reg_dt: datetime
    mod_dt: datetime

    class ConfigDict:
        from_attributes = True

class NodeSaveCreate(BaseModel):
    node_id: int

class NodeSaveReturn(BaseModel):
    id: int
    node_id: int
    owner_id: int
    reg_dt: datetime
    mod_dt: datetime

    class ConfigDict:
        from_attributes = True

#update
class ObjectCommentUpdate(BaseModel):
    comment: str

class NodeCommentUpdate(BaseModel):
    comment: str

    
#object
class AssetUpdate(BaseModel):
    ASSET_TITLE: t.Optional[str] = None
    DESCRIPTION: t.Optional[str] = None


class AssetsReturn(BaseModel):
    ASSET_ID: str
    USER_MNG_ID: int
    ASSET_TYPE: str
    ASSET_TITLE: str
    DESCRIPTION: str
    
    class ConfigDict:
        from_attributes = True

class AssetReturn(BaseModel):
    json_file: bytes
    
    class ConfigDict:
        from_attributes = True


#node
class NodeUpdate(BaseModel):
    NODE_TITLE: t.Optional[str] = None
    NODE_DESCRIPTION: t.Optional[str] = None


class NodesReturn(BaseModel):
    NODE_ID: str
    USER_MNG_ID: int
    ASSET_ID: str
    NODE_TITLE: str
    NODE_DESCRIPTION: str
    LATITUDE: float
    LONGITUDE: float

    class ConfigDict:
        from_attributes = True

class NodeReturn(BaseModel):
    NODE_ID: str
    USER_MNG_ID: int
    ASSET_ID: str
    NODE_TITLE: str
    NODE_DESCRIPTION: str
    LATITUDE: float
    LONGITUDE: float
    REG_DT: datetime
    MOD_DT: datetime
    #comments: t.List[NodeCommentReturn]
    json_file: bytes

    class ConfigDict:
        from_attributes = True


class UpdatedNode(BaseModel):
    NODE_ID: str
    USER_MNG_ID: int
    ASSET_ID: str
    NODE_TITLE: str
    NODE_DESCRIPTION: str
    LATITUDE: float
    LONGITUDE: float
    REG_DT: datetime
    MOD_DT: datetime

    class ConfigDict:
        from_attributes = True

from pydantic import BaseModel


class NodeSearchRequest(BaseModel):
    LATITUDE: float
    LONGITUDE: float


class SearchNode(BaseModel):
    NODE_ID: str
    USER_MNG_ID: int
    ASSET_ID: str
    NODE_TITLE: str
    NODE_DESCRIPTION: str
    LATITUDE: float
    LONGITUDE: float
    DISTANCE: float

    class Config:
        from_attributes = True
#follow
class FollowList(BaseModel):
    user_id: int
    follower_id: int

class FollowUser(BaseModel):
    user_id: int
    follower_id: int

class FollowReturn(BaseModel):
    user_id: int
    follow_id: int
    reg_dt: datetime
    mod_dt: datetime