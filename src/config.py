"""the file for importing of the config settings which will be used for the database connection
important! install pytest-dotenv==0.5.2, python-dotenv==1.0.1"""


from pydantic_settings import BaseSettings, SettingsConfigDict
import os


class Settings(BaseSettings):
    DB_USER: str
    DB_PASS: str
    DB_HOST: str
    DB_NAME: str
    DB_PORT: int
    MODE: str
    SECRETa: str
    JWT_LIFETIME_MINUTES: int

    @property
    def DB_URL(self):
        return f"mysql+aiomysql://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
    

    model_config = SettingsConfigDict(env_file = ".env", extra='allow')


settings = Settings()