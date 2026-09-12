from pydantic import BaseModel, EmailStr, Field, field_validator, ConfigDict
import uuid

class UserBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    email: EmailStr=Field(...,
                        description="The email of the user"
                    )

    name: str=Field(...,
                    description="The name of the user"
                )
    

class UserCreate(UserBase):
    password: str = Field(...,
                        description="The password of the user"
                    )

    @field_validator('password')
    @classmethod
    def password_must_be_strong(cls, value: str) -> str:

        uppers = sum(1 for c in value if c.isupper())
        lowers = sum(1 for c in value if c.islower())
        spaces = sum(1 for c in value if c.isspace())
        specials = sum(1 for c in value if not c.isalnum() and not c.isspace())
        nums = sum(1 for c in value if c.isdigit())

        if len(value) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if uppers < 1:
            raise ValueError('Password must contain at least one uppercase letter')
        if lowers < 1:
            raise ValueError('Password must contain at least one lowercase letter')
        if spaces > 0:
            raise ValueError('Password must not contain spaces')
        if specials < 1:
            raise ValueError('Password must contain at least one special character')
        if nums < 1:
            raise ValueError('Password must contain at least one number')

        return value

class UserResponse(UserBase):
    id :uuid.UUID = Field(...,
                        description="Id of user"
                    )