import asyncio
from langchain.agents import Tool
from langchain_core.tools import StructuredTool
from langchain_aws import BedrockEmbeddings
from src.clients.generate.bedrock_client import BedrockLangchainClient
from src.repositories.dynamodb_cliente_repository import DynamoDbClientRepository
from src.repositories.redis_repository import RedisRepository

class RetrieveAndGenerateTool:
    def __init__(self):
        self.dynamo_client = DynamoDbClientRepository()
        self.bedrock_client = BedrockLangchainClient()
        self.llm_embeddings = BedrockEmbeddings(
            model_id="amazon.titan-text-express-v1",
            region_name="us-east-1"
        )
        self.redis_cache = RedisRepository()
        

    async def retrieve_and_generate(self, user_input: str) -> str:
        try:
            response = await self.bedrock_client.bedrock_with_langchain_client(user_input)
            print(f"RESPOSTA BEDROCK: {response}")  # <-- Linha 4: resposta da LLM Bedrock
            return response
        except Exception as e:
            print(f"Erro no retrieve_and_generate: {e}")  # <-- Linha 6: erro no processo
            return "Erro interno no servidor"


    
