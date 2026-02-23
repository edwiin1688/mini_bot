"""Tests for config.schema module."""
import pytest
from minibot.config.schema import (
    AgentDefaults,
    AgentsConfig,
    ProviderConfig,
    ProvidersConfig,
    TelegramConfig,
    ChannelsConfig,
    Config,
)


class TestAgentDefaults:
    def test_default_values(self):
        defaults = AgentDefaults()
        assert defaults.workspace == "~/.minibot/workspace"
        assert defaults.model == "minimax/MiniMax-M2.5"
        assert defaults.max_tokens == 8192
        assert defaults.temperature == 0.7

    def test_custom_values(self):
        agent = AgentDefaults(model="gpt-4", temperature=0.5)
        assert agent.model == "gpt-4"
        assert agent.temperature == 0.5


class TestProvidersConfig:
    def test_default_providers(self):
        providers = ProvidersConfig()
        assert hasattr(providers, "minimax")
        assert hasattr(providers, "openai")
        assert providers.minimax.api_key == ""


class TestTelegramConfig:
    def test_default_token_empty(self):
        config = TelegramConfig()
        assert config.bot_token == ""


class TestConfig:
    def test_config_default_values(self):
        config = Config()
        assert config.agents is not None
        assert config.providers is not None
        assert config.channels is not None
