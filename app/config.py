from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "Chatbot Juridico"
    APP_VERSION: str = "0.1.0"

    VERIFY_TOKEN: str = ""
    ACCESS_TOKEN: str = ""
    APP_ID: str = ""
    APP_SECRET: str = ""
    PHONE_NUMBER_ID: str = ""
    VERSION: str = "v21.0"
    OPENAI_API_KEY: str = ""
    OPENAI_ASSISTANT_ID: str = ""

    class Config:
        env_file = ".env"


settings = Settings()
