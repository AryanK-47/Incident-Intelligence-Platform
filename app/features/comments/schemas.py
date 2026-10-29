from pydantic import Field, BaseModel, ConfigDict
import uuid
from datetime import datetime

class CommentBase(BaseModel):
    content : str = Field(...,
                        min_length=5,
                        max_length=100
                    )

'''Comment create needs
id -> automated UUID
incident_id  -> from URL/path
user_id -> from logged in user
created_at -> automated timestamp
'''

class CommentCreate(CommentBase):
    pass

class CommentUserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    name: str

class CommentResponse(CommentBase):

    model_config = ConfigDict(from_attributes=True)

    id : uuid.UUID = Field(...,
                        description="Id of comment"
                    )
    
    incident_id : uuid.UUID = Field(...,
                                    description="Id of incident"
                                )

    user: CommentUserResponse

    user_id : uuid.UUID =Field(...,
                            description="Id of user"
                            )
    
    created_at : datetime = Field(...,
                                description="Comment creation time "
                            )

