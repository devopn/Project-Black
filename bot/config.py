from dataclasses import dataclass
import os

@dataclass
class TelegramConfig:
    token: str


@dataclass
class Config:
    telegram: TelegramConfig


config = Config(
    telegram=TelegramConfig(
        token=os.environ.get('TG_KEY','')
    )
)