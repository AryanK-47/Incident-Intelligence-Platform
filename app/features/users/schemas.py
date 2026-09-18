from pydantic import BaseModel, EmailStr, Field, field_validator, ConfigDict
import uuid

def validate_password(password:str) -> str:
    uppers = sum(1 for c in password if c.isupper())
    lowers = sum(1 for c in password if c.islower())
    spaces = sum(1 for c in password if c.isspace())
    specials = sum(1 for c in password if not c.isalnum() and not c.isspace())
    nums = sum(1 for c in password if c.isdigit())
    
    if len(password) < 8:
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
    
    return password

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
    def password_validation(cls, value: str) -> str:
        return validate_password(value)

class UserResponse(UserBase):
    id :uuid.UUID = Field(...,
                        description="Id of user"
                    )

class UserUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name : str | None = None
    email : EmailStr | None = None
    password : str | None = None
    
    @field_validator('password')
    @classmethod
    def password_validation(cls, value : str | None):
        if value is None: return value
        return validate_password(value)