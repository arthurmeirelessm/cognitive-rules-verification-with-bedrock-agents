import json

import redis
from langchain.globals import set_llm_cache
from langchain_aws import BedrockEmbeddings, BedrockLLM
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

    def get_all_cache(self):
        cache_entries = []
        keys = self.redis_client.keys("semantic:cache:*")
        for key in keys:
            try:
                raw_value = self.redis_client.get(key)
                if raw_value:
                    decoded = json.loads(raw_value)
                    cache_entries.append(
                        {
                            "key": key.decode(),
                            "prompt": decoded.get("prompt"),
                            "response": decoded.get("response"),
                        }
                    )
            except Exception as e:
                print(f"Erro ao ler chave {key}: {e}")
        return cache_entries
