from pydantic_settings import BaseSettings,SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env')

    user: str 
    password: str 
    host: str 
    port: int 
    dbname: str 
    JWT_SECRET_KEY:str
    JWT_ALGORITHM:str="HS256"
    EXPIRATION:int=30


settings = Settings()  # type: ignore[call-arg]