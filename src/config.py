import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass(frozen=True)
class Settings:
    openai_api_key: str
    notion_token: str
    notion_daily_database_id: str
    notion_macro_database_id: str | None
    notion_earnings_database_id: str | None
    notion_thesis_database_id: str | None
    openai_model: str = "gpt-4o-mini"
    timezone: str = "Asia/Taipei"

def get_settings() -> Settings:
    required = {
        "OPENAI_API_KEY": os.getenv("OPENAI_API_KEY"),
        "NOTION_TOKEN": os.getenv("NOTION_TOKEN"),
        "NOTION_DAILY_DATABASE_ID": os.getenv("NOTION_DAILY_DATABASE_ID"),
    }
    missing = [name for name, value in required.items() if not value]
    if missing:
        raise RuntimeError(f"Missing required environment variables: {', '.join(missing)}")

    return Settings(
        openai_api_key=required["OPENAI_API_KEY"],
        notion_token=required["NOTION_TOKEN"],
        notion_daily_database_id=required["NOTION_DAILY_DATABASE_ID"],
        notion_macro_database_id=os.getenv("NOTION_MACRO_DATABASE_ID"),
        notion_earnings_database_id=os.getenv("NOTION_EARNINGS_DATABASE_ID"),
        notion_thesis_database_id=os.getenv("NOTION_THESIS_DATABASE_ID"),
        openai_model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        timezone=os.getenv("TIMEZONE", "Asia/Taipei"),
    )
