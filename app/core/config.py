from pydantic_settings import BaseSettings,SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env')

    user: str 
    password: str 
    host: str 
    port: int 
    dbname: str 


settings = Settings()  # type: ignore[call-arg]