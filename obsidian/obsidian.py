from pathlib import Path
from datetime import datetime

obsidian_path = Path("/Users/bianders/MorphyMobile/")


# Get today's date in YYYY-MM-DD format
def get_today_date() -> str:
    return datetime.now().strftime("%Y-%m-%d")


def get_today_doc() -> Path:
    """
    Get the path to the daily note for today.
    """
    return obsidian_path / f"{get_today_date()}.md"


if __name__ == "__main__":
    print(get_today_doc().read_text())
