from typing import Annotated
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

    async def retrieve_and_generate(self, action_group: Annotated[str, "Texto original do usuário"]) -> str:
        try:
            print(f"ACTION_GROUP NO retrieve_and_generate: {action_group}")
            
            cached = await self.redis_cache.get_cache(action_group, self.llm_embeddings)
            print(f"CACHE RETORNADO: {cached}")

            if cached:
                resultado = cached[0].text if isinstance(cached, list) else cached
                print(f"RETORNANDO DO CACHE: {resultado}")
                return resultado

            response = await self.bedrock_client.bedrock_with_langchain_client(action_group)
            print(f"RESPOSTA BEDROCK: {response}")
            
            await self.redis_cache.update_cache(action_group, self.llm_embeddings, response)
            print("CACHE ATUALIZADO")
            
            return response
        except Exception as e:
            print(f"Erro no retrieve_and_generate: {e}")
            return "Erro interno no servidor"

    def to_tool(self) -> StructuredTool:
        return StructuredTool.from_function(
            coroutine=self.retrieve_and_generate,
            name="RetrieveAndGenerateTool",
            description=(
                "Use esta ferramenta para responder diretamente com base no texto original do usuário. "
                "O parâmetro de entrada deve ser chamado 'action_group'."
            ),
        )
