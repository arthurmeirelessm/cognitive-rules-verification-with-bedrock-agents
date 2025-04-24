import asyncio
import random
from typing import Union
from langchain_aws.llms.bedrock import BedrockLLM
from langchain_aws import ChatBedrock
from langchain.agents import initialize_agent, AgentType
from beartype import beartype
from src.auth import JWTAuth, require_jwt
from src.tools.tool_factory import get_all_tools
from src.logger import log_execution


class CognitiveRulesVerificationAppServices:
    def __init__(self):
        self.jwt_auth = JWTAuth()
        
    @log_execution
    @beartype
    @require_jwt(jwt_auth=JWTAuth())
    async def agent_orchestrator_service(self, 
        auth_header: str, user_input: str
    ) -> tuple[str, int]:
        try:
            print(f"USER INPUT NO SERVICE: {user_input}")

            tools = get_all_tools()

            llm = ChatBedrock(
                model_id="us.anthropic.claude-3-7-sonnet-20250219-v1:0",
                region_name="us-east-1",
                model_kwargs={"temperature": 0.3},
            )

            agent = initialize_agent(
                tools=tools,
                llm=llm,
                agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
                verbose=True,
                max_iterations=1,
                early_stopping_method="generate",
            )

            result = await agent.arun(user_input)
            print(f"RESULT NO SERVICE: {result}")
            return result, 200

        except Exception as e:
            print(f"Erro no service: {e}")
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
