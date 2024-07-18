from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env', env_file_encoding='utf-8'
    )

    DATABASE_URL: str

    # class Config:
    #     # Este Config class é opcional se você não quiser especificar nada
    #     env_file = None  # Desativa o uso de arquivos .env}
