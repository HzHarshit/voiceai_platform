from abc import ABC, abstractmethod
from typing import Dict, Any


class VoiceProvider(ABC):
    """Abstract base class for voice providers."""

    def __init__(self, api_key: str, config: Dict[str, Any] = None):
        self.api_key = api_key
        self.config = config or {}

    @abstractmethod
    def make_call(self, phone_number: str, message: str, **kwargs) -> Dict[str, Any]:
        """Make a voice call to the specified phone number with the given message."""
        pass

    @abstractmethod
    def get_call_status(self, call_id: str) -> Dict[str, Any]:
        """Get the status of a call by its ID."""
        pass

    @abstractmethod
    def hangup_call(self, call_id: str) -> bool:
        """Hang up an ongoing call."""
        pass

    @abstractmethod
    def get_supported_languages(self) -> list:
        """Get list of supported languages."""
        pass

    @abstractmethod
    def get_supported_voices(self) -> list:
        """Get list of supported voices."""
        pass
