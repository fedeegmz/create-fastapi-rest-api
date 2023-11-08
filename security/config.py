from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # app_name: str = "Name"
    # admin_email: str = "example@email.com"
    is_test_db: bool
    jwt_secretkey: str
    mongodb_user: str
    mongodb_password: str
    mongodb_host: str

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()