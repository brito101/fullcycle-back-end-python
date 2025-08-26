from django.utils.deprecation import MiddlewareMixin
from src.core._shared.infra.storage.in_memory_storage import InMemoryStorage
from src.core._shared.events.message_bus import MessageBus


class ServiceInjectionMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # Inject storage service
        request.storage_service = InMemoryStorage()
        
        # Inject message bus
        request.message_bus = MessageBus()
        
        return None
