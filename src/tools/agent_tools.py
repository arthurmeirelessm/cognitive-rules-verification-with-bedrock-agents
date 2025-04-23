from langchain.agents import Tool
import asyncio
import random
from typing import Union

from langchain_aws import BedrockEmbeddings
from src.clients.generate.bedrock_client import BedrockLangchainClient
from src.logger import log_execution
from beartype import beartype
from src.repositories.dynamodb_cliente_repository import DynamoDbClientRepository
from src.repositories.redis_repository import RedisRepository


class RetrieveAndGenerateAgentTolls: 
    def __init__(self):
        self.dynamo_client = DynamoDbClientRepository()
        self.bedrock_with_langchain_client = BedrockLangchainClient()
        self.llm_embeddings = BedrockEmbeddings(
            model_id="amazon.titan-text-express-v1", region_name="us-east-1"
        )
        self.redis_semantic_cache_repository = RedisRepository()
        
    
    async def RetrieveAndGenerateToll(self, user_input: str) -> str:
        try:
            cached_response = await self.redis_semantic_cache_repository.get_cache(
                user_input, self.llm_embeddings
            )

            if cached_response:
                text = cached_response[0].text if isinstance(cached_response, list) else cached_response
                return text, 200

            bedrockClientResponse = (
                await self.bedrock_with_langchain_client.bedrock_with_langchain_client(user_input)
            )

            await self.redis_semantic_cache_repository.update_cache(
                user_input, self.llm_embeddings, bedrockClientResponse
            )

            return bedrockClientResponse, 200
        except Exception as e:
            print(f"Erro ao criar item: {e}")
            return "Erro interno no servidor", 500
        
        
    def to_tool(self):
        return Tool(
            name="RetrieveAndGenerateTool",
            func=lambda x: asyncio.run(self.RetrieveAndGenerateToll(x)),
            description="Recupera dados do cache e, se não existir, gera uma nova resposta com o Bedrock"
        )