"""Configuration schema (minimal)."""

from pydantic import BaseModel, Field, ConfigDict
from pydantic.alias_generators import to_camel
from pydantic_settings import BaseSettings


class Base(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)


class AgentDefaults(Base):
    """Agent 預設設定。"""
    workspace: str = "~/.minibot/workspace"
    model: str = "minimax/MiniMax-M2.5"
    max_tokens: int = 8192
    temperature: float = 0.7
    max_tool_iterations: int = 20
    memory_window: int = 50


class AgentsConfig(Base):
    defaults: AgentDefaults = Field(default_factory=AgentDefaults)


class ProviderConfig(Base):
    api_key: str = ""
    api_base: str | None = None


class ProvidersConfig(Base):
    minimax: ProviderConfig = Field(default_factory=ProviderConfig)
    openrouter: ProviderConfig = Field(default_factory=ProviderConfig)
    anthropic: ProviderConfig = Field(default_factory=ProviderConfig)
    openai: ProviderConfig = Field(default_factory=ProviderConfig)
    deepseek: ProviderConfig = Field(default_factory=ProviderConfig)
    gemini: ProviderConfig = Field(default_factory=ProviderConfig)


class TelegramConfig(Base):
    """Telegram Bot 設定。"""
    bot_token: str = ""


class ChannelsConfig(Base):
    """頻道設定。"""
    telegram: TelegramConfig = Field(default_factory=TelegramConfig)


class Config(BaseSettings):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)
    agents: AgentsConfig = Field(default_factory=AgentsConfig)
    providers: ProvidersConfig = Field(default_factory=ProvidersConfig)
    channels: ChannelsConfig = Field(default_factory=ChannelsConfig)

