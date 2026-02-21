"""Memory system for persistent agent memory."""

from pathlib import Path

from minibot.utils.helpers import ensure_dir


class MemoryStore:
    """雙層記憶體系統：MEMORY.md（長期事實）+ HISTORY.md（可搜尋日誌）。"""

    def __init__(self, workspace: Path):
        self.memory_dir = ensure_dir(workspace / "memory")
        self.memory_file = self.memory_dir / "MEMORY.md"
        self.history_file = self.memory_dir / "HISTORY.md"

    def read_long_term(self) -> str:
        """讀取長期記憶。"""
        if self.memory_file.exists():
            return self.memory_file.read_text(encoding="utf-8")
        return ""

    def write_long_term(self, content: str) -> None:
        """寫入長期記憶。"""
        self.memory_file.write_text(content, encoding="utf-8")

    def append_history(self, entry: str) -> None:
        """新增歷史記錄。"""
        with open(self.history_file, "a", encoding="utf-8") as f:
            f.write(entry.rstrip() + "\n\n")

    def get_memory_context(self) -> str:
        """取得記憶內容，供注入 system prompt 使用。"""
        long_term = self.read_long_term()
        return f"## Long-term Memory\n{long_term}" if long_term else ""
