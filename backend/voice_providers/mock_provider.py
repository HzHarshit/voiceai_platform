import uuid
from typing import Dict, Any
from .base import VoiceProvider


class MockVoiceProvider(VoiceProvider):
    """Mock implementation of VoiceProvider for testing and development."""

    def __init__(self, api_key: str = "mock_key", config: Dict[str, Any] = None):
        super().__init__(api_key, config)
        self.calls = {}  # In-memory storage for mock calls

    def make_call(self, phone_number: str, message: str, **kwargs) -> Dict[str, Any]:
        """Simulate making a voice call."""
        call_id = str(uuid.uuid4())
        self.calls[call_id] = {
            'id': call_id,
            'phone_number': phone_number,
            'message': message,
            'status': 'initiated',
            'created_at': '2023-01-01T00:00:00Z',
            'duration': 0,
            'cost': 0.05,  # Mock cost
        }
        # Simulate call completion after some time (in real implementation, this would be async)
        self.calls[call_id]['status'] = 'completed'
        self.calls[call_id]['duration'] = 30  # Mock 30 seconds
        return self.calls[call_id]

    def get_call_status(self, call_id: str) -> Dict[str, Any]:
        """Get the status of a mock call."""
        if call_id not in self.calls:
            raise ValueError(f"Call {call_id} not found")
        return self.calls[call_id]

    def hangup_call(self, call_id: str) -> bool:
        """Simulate hanging up a call."""
        if call_id not in self.calls:
            return False
        if self.calls[call_id]['status'] == 'in_progress':
            self.calls[call_id]['status'] = 'completed'
            return True
        return False

    def get_supported_languages(self) -> list:
        """Get list of supported languages."""
        return ['en-US', 'es-ES', 'fr-FR', 'de-DE']

    def get_supported_voices(self) -> list:
        """Get list of supported voices."""
        return [
            {'id': 'voice1', 'name': 'Alice', 'language': 'en-US', 'gender': 'female'},
            {'id': 'voice2', 'name': 'Bob', 'language': 'en-US', 'gender': 'male'},
            {'id': 'voice3', 'name': 'Maria', 'language': 'es-ES', 'gender': 'female'},
        ]
