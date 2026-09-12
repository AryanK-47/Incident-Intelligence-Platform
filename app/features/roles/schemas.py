from pydantic import Field, BaseModel, ConfigDict
import uuid

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