import json

import redis
from langchain.globals import set_llm_cache
from langchain_aws import BedrockEmbeddings
from langchain.schema import Generation
from langchain_community.cache import RedisSemanticCache
from langchain_community.embeddings import BedrockEmbeddings


class RedisRepository:
    def __init__(self):
        self.redis_url = "redis://localhost:6379"
        self.redis_cache = RedisSemanticCache(
            redis_url=self.redis_url, embedding=BedrockEmbeddings(), score_threshold=0.2
        )
        set_llm_cache(self.redis_cache)
        self.redis_client = redis.Redis.from_url(self.redis_url)
        
        

    async def get_cache(self, prompt: str, llm: BedrockEmbeddings) -> str:
        try:
            llm_string = str(llm)
            cached_response = self.redis_cache.lookup(prompt, llm_string)
            if cached_response:
                print(f"Resposta encontrada no cache: {cached_response}")
                return cached_response
        except Exception as e:
            print(f"Erro ao buscar no cache: {e}")
        return None
    
    
    async def update_cache(self, prompt: str, llm: BedrockEmbeddings, response: str) -> None:
        try:
            llm_string = str(llm)
            gen = Generation(text=response)
            await self.redis_cache.aupdate(prompt, llm_string, [gen])
            print(f"Cache atualizado com sucesso para o prompt: {prompt}")
        except Exception as e:
            print(f"Erro ao atualizar cache: {e}")
            
    
    async def get_all_cache(self) -> dict:
        """
        Retorna todas as entradas armazenadas no Redis, agrupando por tipo de estrutura.
        :return: Dict com chave sendo o nome da chave no Redis e valor sendo o conteúdo armazenado.
        """
        all_entries = {}
        try:
            # Lista todas as chaves
            keys = self.redis_client.keys("*")
            for raw_key in keys:
                key = raw_key.decode('utf-8')
                # Identifica tipo de dado
                dtype = self.redis_client.type(key)
                if dtype == b'hash':
                    # Hash: retorna todos os campos e valores
                    raw_vals = self.redis_client.hgetall(key)
                    all_entries[key] = {k.decode('utf-8'): v.decode('utf-8') for k, v in raw_vals.items()}
                else:
                    # String, list, set, etc.
                    val = self.redis_client.get(key)
                    all_entries[key] = val.decode('utf-8') if val is not None else None
        except Exception as e:
            print(f"Erro ao listar todas as chaves no cache: {e}")
        return all_entries

