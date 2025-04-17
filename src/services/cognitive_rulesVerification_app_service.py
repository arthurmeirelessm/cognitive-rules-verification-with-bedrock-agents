import asyncio
import random
from typing import Union
from beartype import beartype
from langchain_core.messages import AIMessage
from src.auth import JWTAuth
from src.logger import log_execution
from src.repositories.dynamodb_cliente_repository import DynamoDbClientRepository
from src.clients.bedrock_client import BedrockLangchainClient


class CognitiveRulesVerificationAppServices:
    def __init__(self):
        self.jwt_auth = JWTAuth()
        self.dynamo_client = DynamoDbClientRepository()
        self.bedrock_with_langchain_client = BedrockLangchainClient()
        

    @log_execution
    @beartype
    async def get_all_items_service(self, auth_header: str) -> list[str] | tuple[str, int]:
        try:
            auth_validation = await self.jwt_auth.verify_jwt(auth_header)
            if auth_validation is True:
                get_all_items_response = await self.dynamo_client.get_all()
                print(get_all_items_response)
                return get_all_items_response, 200
            else:
                return auth_validation, 403
        except Exception as e:
            print(f"Erro ao obter itens: {e}")
            return "Erro interno no servidor", 500

    @log_execution
    @beartype
    async def create_item_service(
        self, auth_header: str, cpf: str, email: str, nome: str, celular: str
    ) -> tuple[str, int]:
        try:
            auth_validation = await self.jwt_auth.verify_jwt(auth_header)
            if auth_validation is True:
                create_user_response = await self.dynamo_client.create_item(
                    cpf, email, nome, celular
                )
                print(f"create_User_r: {create_user_response}")
                if create_user_response is True:
                    return "Usuario criado com sucesso!", 200
                else:
                    return "Erro ao criar usuario", 500
            else:
                return auth_validation, 403
        except Exception as e:
            print(f"Erro ao criar item: {e}")
            return "Erro interno no servidor", 500
        
    
    @log_execution
    @beartype
    async def agent_orchestrator_service(
        self, auth_header: str, input: str
    ) -> tuple[str, int]:
        try:
            auth_validation = await self.jwt_auth.verify_jwt(auth_header)
            if auth_validation is True:
               bedrockClient = await self.bedrock_with_langchain_client.bedrock_with_langchain_client(input)
               print(f'Bedrock CLIENT: {bedrockClient}')
               return bedrockClient, 200
            else:
                return auth_validation, 403
        except Exception as e:
            print(f"Erro ao criar item: {e}")
            return "Erro interno no servidor", 500
        

    @log_execution
    @beartype
    async def get_jwt_service(self, username: str, password: str) -> tuple[str, int]:
        try:
            if username == "admin" and password == "1234":
                token = await self.jwt_auth.generate_jwt(user_id=1)
                return token, 200
            return "Token Não foi gerado!", 401
        except Exception as e:
            print(f"Erro ao gerar token: {e}")
            return "Erro interno no servidor", 500
