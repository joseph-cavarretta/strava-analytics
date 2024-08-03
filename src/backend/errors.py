class APIError(Exception):
    """All custom API Exceptions"""
    pass

class MessageError(APIError):
    """Raise when POST request does not include a message key"""
    code = 400
    description = "Request must contain a 'message' key"