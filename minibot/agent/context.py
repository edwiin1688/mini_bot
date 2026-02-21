"""Context builder (minimal)."""

import platform
from datetime import datetime
from pathlib import Path
from minibot.agent.memory import MemoryStore


class ContextBuilder:
    """建立 LLM 所需的 system prompt 及對話訊息串列。"""

    def __init__(self, workspace: Path):
        self.workspace = workspace
        self.memory = MemoryStore(workspace)

    def build_system_prompt(self) -> str:
        """建立 system prompt，包含基本資訊、workspace 指引與長期記憶。"""
        parts = [
            "You are mini_bot 🤖, a personal AI assistant.",
            f"Platform: {platform.system()} {platform.release()}",
            f"Working directory: {self.workspace}",
            f"Current time: {datetime.now().isoformat()}",
        ]
        # 載入 workspace 引導檔
        for name in ("AGENTS.md", "SOUL.md"):
            f = self.workspace / name
            if f.exists():
                parts.append(f"\n## {name}\n{f.read_text(encoding='utf-8')}")
        # 載入長期記憶
        mem = self.memory.get_memory_context()
        if mem:
            parts.append(f"\n{mem}")
        return "\n\n".join(parts)

    def build_messages(self, history: list[dict], current_message: str) -> list[dict]:
        """組合完整的訊息串列（system + 歷史 + 目前訊息）。"""
        messages = [{"role": "system", "content": self.build_system_prompt()}]
        messages.extend(history)
        messages.append({"role": "user", "content": current_message})
        return messages
