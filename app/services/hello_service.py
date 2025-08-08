from datetime import datetime
from app.models.user import MessageResponse

class HelloService:
    pass
    
    def hello_world(self, message: str = "Hello World!") -> MessageResponse:
        return MessageResponse(
            message=message,
            timestamp=datetime.now(),
            author="System",
            organization="Vibe Kanban"
        )