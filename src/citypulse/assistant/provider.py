from __future__ import annotations

from abc import ABC, abstractmethod


class LLMProvider(ABC):
    @abstractmethod
    def generate(self, prompt: str) -> str:
        raise NotImplementedError


class UnavailableProvider(LLMProvider):
    def generate(self, prompt: str) -> str:
        raise RuntimeError("AI assistant provider is not configured")
