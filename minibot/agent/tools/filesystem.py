"""File system tools."""

from pathlib import Path
from minibot.agent.tools.base import Tool


class ReadFileTool(Tool):
    """讀取檔案內容。"""

    name = "read_file"
    description = "Read the contents of a file."
    parameters = {
        "type": "object",
        "properties": {"path": {"type": "string", "description": "File path"}},
        "required": ["path"]
    }

    async def execute(self, path: str) -> str:
        p = Path(path).expanduser()
        if not p.exists():
            return f"Error: File not found: {path}"
        return p.read_text(encoding="utf-8")[:50000]


class WriteFileTool(Tool):
    """寫入內容至檔案。"""

    name = "write_file"
    description = "Write content to a file."
    parameters = {
        "type": "object",
        "properties": {
            "path": {"type": "string"},
            "content": {"type": "string"}
        },
        "required": ["path", "content"]
    }

    async def execute(self, path: str, content: str) -> str:
        p = Path(path).expanduser()
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding="utf-8")
        return f"Written {len(content)} chars to {path}"


class ListDirTool(Tool):
    """列出目錄內容。"""

    name = "list_dir"
    description = "List contents of a directory."
    parameters = {
        "type": "object",
        "properties": {"path": {"type": "string", "description": "Directory path"}},
        "required": ["path"]
    }

    async def execute(self, path: str) -> str:
        p = Path(path).expanduser()
        if not p.is_dir():
            return f"Error: Not a directory: {path}"
        items = []
        for item in sorted(p.iterdir()):
            prefix = "[DIR] " if item.is_dir() else "[FILE]"
            items.append(f"{prefix} {item.name}")
        return "\n".join(items) or "(empty directory)"
