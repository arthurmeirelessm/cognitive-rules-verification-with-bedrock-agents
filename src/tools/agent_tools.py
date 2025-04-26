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
        

    def retrieve_and_generate(self, user_input: str) -> str:
         try:
            receitas_basicas = """
            🍳 Receita Pós-Treino: Omelete Proteico
            - Ingredientes: 2 ovos, sal, pimenta, 1 colher de sopa de leite, azeite.
            - Modo de preparo: Bata os ovos com sal, pimenta e leite. Aqueça o azeite em uma frigideira e despeje a mistura. Cozinhe até dourar dos dois lados. Ideal para recuperar os músculos com proteína de qualidade.

            🍰 Receita Doce: Brigadeiro Clássico
            - Ingredientes: 1 lata de leite condensado, 1 colher de sopa de manteiga, 2 colheres de sopa de chocolate em pó, chocolate granulado.
            - Modo de preparo: Misture o leite condensado, manteiga e chocolate em pó em uma panela. Cozinhe mexendo sempre até desgrudar do fundo. Modele em bolinhas e passe no granulado.

            🍝 Receita Italiana: Espaguete ao Alho e Óleo
            - Ingredientes: 200g de espaguete, 3 dentes de alho fatiados, azeite, sal, salsinha (opcional).
            - Modo de preparo: Cozinhe o espaguete com sal. Refogue o alho no azeite até dourar. Misture o espaguete cozido ao alho refogado e finalize com salsinha.
            """
            
            final_input = "Input do usuário: " + user_input + "\nContexto de receitas aqui em baixo: " + receitas_basicas
            
            return final_input
            
         except Exception as e:
            print(f"Erro no retrieve_and_generate: {e}")  # <-- Linha 6: erro no processo
            return "Erro interno no servidor"


    
