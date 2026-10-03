import uuid
from pydantic import Field, BaseModel, ConfigDict

from app.features.users.schemas import RoleUserResponse


class RoleBase(BaseModel):
    name : str = Field(...,
                    description="Name of the role",
                    min_length=3
                )


class RoleCreate(RoleBase):
    # It only needs name since id is automated
    pass

class RoleResponse(RoleBase):
    model_config = ConfigDict(from_attributes=True)

    id : uuid.UUID = Field(...,
                        description="Id of role"
                    )
class RoleDetailResponse(RoleResponse):
    users : list[RoleUserResponse]= Field(
        default_factory=list,
        description="Users assigned to this role"
    )

class RoleUpdate(BaseModel):
    name : str | None = Field(
        default = None,
        min_length=3,
        description="New name of the rolenb"
    )