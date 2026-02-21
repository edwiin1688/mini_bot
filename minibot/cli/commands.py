"""CLI commands (minimal)."""

import asyncio
import sys
from pathlib import Path

# Windows 終端機同步設定 UTF-8，避免 emoji 編碼錯誤
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

import typer
from rich.console import Console
from rich.markdown import Markdown
from prompt_toolkit import PromptSession

from minibot import __version__
from minibot.bus.queue import MessageBus
from minibot.config.loader import load_config, save_config, get_config_path
from minibot.providers.litellm_provider import LiteLLMProvider
from minibot.session.manager import SessionManager
from minibot.utils.helpers import ensure_dir, get_data_path

app = typer.Typer(help="minibot - Personal AI Assistant (powered by mini_bot)")
console = Console()


@app.command()
def onboard():
    """初始化 minibot 設定與 workspace。"""
    config_path = get_config_path()
    if not config_path.exists():
        config_path.parent.mkdir(parents=True, exist_ok=True)
        config_path.write_text(
            '{\n  "providers": {\n    "minimax": {\n      "apiKey": "",\n      "apiBase": "https://api.minimax.io/v1"\n    }\n  }\n}'
        )
        console.print(f"✅ Config created: {config_path}")
    else:
        console.print(f"Config already exists: {config_path}")

    ws = Path("~/.minibot/workspace").expanduser()
    ensure_dir(ws)
    ensure_dir(ws / "memory")
    agents_file = ws / "AGENTS.md"
    if not agents_file.exists():
        agents_file.write_text("# Agent Instructions\n\nYou are a helpful AI assistant.\n")
    console.print(f"✅ Workspace: {ws}")
    console.print("\n📝 Edit ~/.minibot/config.json to add your API key, then run: minibot agent")


def _make_provider(config):
    """根據 config 建立 LLM Provider。優先順序：minimax > openrouter > anthropic > openai > deepseek > gemini。"""
    model = config.agents.defaults.model

    # 依序檢查哪個 provider 有 API key
    providers_map = {
        "minimax": ("MINIMAX_API_KEY", "minimax", "https://api.minimax.io/v1"),
        "openrouter": ("OPENROUTER_API_KEY", "openrouter", None),
        "anthropic": ("ANTHROPIC_API_KEY", "", None),
        "openai": ("OPENAI_API_KEY", "", None),
        "deepseek": ("DEEPSEEK_API_KEY", "deepseek", None),
        "gemini": ("GEMINI_API_KEY", "gemini", None),
    }

    for name, (env_key, prefix, default_api_base) in providers_map.items():
        prov_cfg = getattr(config.providers, name)
        if prov_cfg.api_key:
            api_base = prov_cfg.api_base or default_api_base
            return LiteLLMProvider(
                api_key=prov_cfg.api_key,
                model=model,
                api_base=api_base,
                env_key=env_key,
                litellm_prefix=prefix,
            )

    console.print("[red]Error: No API key configured. Edit ~/.minibot/config.json[/red]")
    raise typer.Exit(1)


@app.command()
def agent(
    message: str = typer.Option(None, "--message", "-m", help="Single message mode"),
    markdown: bool = typer.Option(True, "--markdown/--no-markdown"),
):
    """與 mini_bot Agent 互動聊天。"""
    config = load_config()
    provider = _make_provider(config)
    workspace = Path(config.agents.defaults.workspace).expanduser()
    ensure_dir(workspace)

    bus = MessageBus()
    from minibot.agent.loop import AgentLoop
    agent_loop = AgentLoop(
        bus=bus,
        provider=provider,
        workspace=workspace,
        model=config.agents.defaults.model,
        max_iterations=config.agents.defaults.max_tool_iterations,
        temperature=config.agents.defaults.temperature,
        max_tokens=config.agents.defaults.max_tokens,
        memory_window=config.agents.defaults.memory_window,
    )

    def _print_response(text: str):
        if markdown:
            console.print(Markdown(text))
        else:
            console.print(text)

    # 單次訊息模式
    if message:
        result = asyncio.run(agent_loop.process_direct(message))
        _print_response(result)
        return

    # 互動模式
    console.print(f"[bold cyan]🤖 minibot v{__version__}[/bold cyan]")
    console.print("Type 'exit' to quit.\n")

    session = PromptSession()

    async def run_interactive():
        while True:
            try:
                user_input = await session.prompt_async("You> ")
            except (EOFError, KeyboardInterrupt):
                break

            if user_input.strip().lower() in ("exit", "quit", "/exit", ":q"):
                break
            if not user_input.strip():
                continue

            console.print("[dim]Thinking...[/dim]")
            result = await agent_loop.process_direct(user_input)
            console.print()
            _print_response(result)
            console.print()

    asyncio.run(run_interactive())
    console.print("\n[dim]Goodbye! 🤖[/dim]")


@app.command()
def status():
    """顯示 minibot 目前狀態。"""
    config = load_config()
    console.print(f"[bold]🤖 minibot v{__version__}[/bold]")
    console.print(f"Config: {get_config_path()}")
    console.print(f"Model: {config.agents.defaults.model}")

    # 檢查 provider 設定
    for name in ("minimax", "openrouter", "anthropic", "openai", "deepseek", "gemini"):
        prov = getattr(config.providers, name)
        if prov.api_key:
            masked = prov.api_key[:8] + "..." + prov.api_key[-4:]
            console.print(f"Provider: {name} ✅ ({masked})")

    # 檢查 Telegram 設定
    tg_token = config.channels.telegram.bot_token
    if tg_token:
        masked = tg_token[:8] + "..." + tg_token[-4:]
        console.print(f"Telegram: ✅ ({masked})")
    else:
        console.print("Telegram: ❌ (未設定)")


@app.command()
def telegram():
    """啟動 Telegram Bot（Polling 模式）。"""
    config = load_config()
    bot_token = config.channels.telegram.bot_token

    if not bot_token:
        console.print("[red]Error: Telegram bot token not configured.[/red]")
        console.print("Edit ~/.minibot/config.json and add channels.telegram.botToken")
        raise typer.Exit(1)

    provider = _make_provider(config)
    workspace = Path(config.agents.defaults.workspace).expanduser()
    ensure_dir(workspace)

    console.print(f"[bold cyan]🤖 minibot Telegram Bot v{__version__}[/bold cyan]")
    console.print("Starting Polling mode... Press Ctrl+C to stop.\n")

    from minibot.channels.telegram import TelegramChannel
    channel = TelegramChannel(
        bot_token=bot_token,
        provider=provider,
        workspace=workspace,
        model=config.agents.defaults.model,
        max_iterations=config.agents.defaults.max_tool_iterations,
        temperature=config.agents.defaults.temperature,
        max_tokens=config.agents.defaults.max_tokens,
        memory_window=config.agents.defaults.memory_window,
    )
    channel.run()

