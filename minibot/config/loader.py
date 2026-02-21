"""Config loading."""

import json
from pathlib import Path
from minibot.config.schema import Config


def get_config_path() -> Path:
    """取得設定檔路徑（~/.minibot/config.json）。"""
    return Path.home() / ".minibot" / "config.json"


def load_config(config_path: Path | None = None) -> Config:
    """載入設定檔，若不存在則回傳預設值。"""
    path = config_path or get_config_path()
    if path.exists():
        try:
            with open(path, encoding="utf-8") as f:
                data = json.load(f)
            return Config.model_validate(data)
        except Exception as e:
            print(f"Warning: Config load failed: {e}")
    return Config()


def save_config(config: Config, config_path: Path | None = None) -> None:
    """儲存設定至磁碟。"""
    path = config_path or get_config_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(config.model_dump(by_alias=True), f, indent=2, ensure_ascii=False)
