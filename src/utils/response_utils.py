# src/utils/service_response.py

from beartype import beartype

@beartype
class ServiceResponse:
    INTERNAL_ERROR: str = "Erro interno no servidor"
    TOKEN_NOT_GENERATED: str = "Token não foi gerado!"

    def __init__(self, message: str, status_code: int) -> None:
        self.message = message
        self.status_code = status_code

    @classmethod
    def success(
        cls, 
        data: str, 
        status_code: int = 200) -> "ServiceResponse":
        """Resposta de sucesso com payload em `message`."""
        return cls(message=data, status_code=status_code)

    @classmethod
    def error(cls, message: str, status_code: int) -> "ServiceResponse":
        """Resposta de erro."""
        return cls(message=message, status_code=status_code)

    def to_dict(self) -> dict:
        """Retorna o dict {'message': ..., 'status_code': ...}."""
        return {"message": self.message, "status_code": self.status_code}
