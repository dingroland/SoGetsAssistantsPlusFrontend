import openai

class BaseOpenAIManager:
    """
    Base class for managing OpenAI API interactions.
    Handles API initialization and error handling.
    """
    def __init__(self, api_key: str):
        """Initialize OpenAI API client."""
        self.client = openai.OpenAI(api_key=api_key)
    
    def handle_api_call(self, function, *args, **kwargs):
        """Wrapper for API calls to handle errors cleanly."""
        try:
            return function(*args, **kwargs)
        except Exception as e:
            return {"error": str(e), "status": "failure"}