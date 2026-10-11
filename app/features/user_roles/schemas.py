from pydantic import Field, BaseModel, ConfigDict
import uuid

class UserRoleCreate(BaseModel):
    role_id: uuid.UUID = Field(
        ...,
        description="Id of the role to assign"
    )
    

class UserRoleUpdate(BaseModel):
    new_role_id: uuid.UUID = Field(
        ...,
        description="Id of the new role"
    )


class UserRoleResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user_id: uuid.UUID
    role_id: uuid.UUID