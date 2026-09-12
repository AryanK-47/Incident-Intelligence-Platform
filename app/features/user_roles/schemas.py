from pydantic import Field, BaseModel, ConfigDict
import uuid

class UserRoleResponse(BaseModel):

    model_config= ConfigDict(from_attributes=True)

    user_id : uuid.UUID = Field(...,
                                description= "Id of user"
                            )

    role_id : uuid.UUID = Field(...,
                                description="Id of the role"
                            )