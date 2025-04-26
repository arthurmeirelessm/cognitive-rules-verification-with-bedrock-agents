import asyncio
import random
from typing import Union, Tuple
from langchain_aws import ChatBedrock
from langchain.agents import initialize_agent, AgentType
from langchain.agents.agent import AgentExecutor  
from langchain.schema.messages import BaseMessage
from beartype import beartype
from src.auth import JWTAuth, require_jwt
from src.tools.tool_factory import get_all_tools
from src.logger import log_execution
from langchain.tools import StructuredTool
import boto3
from botocore.exceptions import ClientError
from langchain.agents import AgentType, initialize_agent
from langchain.memory import ConversationBufferMemory
from langchain.prompts import MessagesPlaceholder
from langchain.schema.messages import AIMessage, HumanMessage
from src.tools.agent_tools import RetrieveAndGenerateTool
from src.utils.response_utils import ServiceResponse
from langchain_aws import ChatBedrockConverse


class CognitiveRulesVerificationAppServices:
    def __init__(self):
        self.jwt_auth = JWTAuth()
        self.retrieve_and_generate_tool = RetrieveAndGenerateTool()

    @log_execution
    @beartype
    @require_jwt(jwt_auth=JWTAuth())
    async def agent_orchestrator_service(
        self, 
        auth_header: str, 
        user_input: str
    ) -> ServiceResponse:
        try:
            agent_executor = await self.setup_full_agent()
            chat_history = []
            response = await self.interact_with_agent(agent_executor, user_input, chat_history)
            
            return ServiceResponse.success(response)
            
        except Exception as e:
            print(f"Erro no service: {e}")
            return ServiceResponse.error(
                ServiceResponse.INTERNAL_ERROR, status_code=500
            )

    @log_execution
    @beartype
    async def interact_with_agent(
        self, 
        agent_executor: AgentExecutor, 
        user_input: str, 
        chat_history: list) -> str | ServiceResponse:
        try:
            """Interact with the agent and store chat history. Return the response."""
            print(f"INPUT NO interact_with_agent: {user_input}")
            print("preview result AAA")
            result = await agent_executor.arun(user_input)
            print("result AAA:", result)
 
        
            chat_history.append(HumanMessage(content=user_input))
            chat_history.append(AIMessage(content="Assistant: " + result))
            
            
            return result

        except Exception as e:
            print(f"Erro no service: {e}")
            return ServiceResponse.error(
                ServiceResponse.INTERNAL_ERROR, status_code=500
            )

    @log_execution
    @beartype
    async def setup_full_agent(self) -> AgentExecutor | ServiceResponse:
        try:
            llm = ChatBedrockConverse(model="us.amazon.nova-pro-v1:0")

            retrieve_and_generate = StructuredTool.from_function(
                name="retrieve_and_generate", 
                func=self.retrieve_and_generate_tool.retrieve_and_generate,
                description="Gera resposta baseada em receitas e consultas de culinária"
            )

            memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

            agent_executor = initialize_agent(
                [retrieve_and_generate],
                llm,
                agent="zero-shot-react-description",
                agent_kwargs={
                    "system_message": (
                        "Você é um assistente educado e útil. Sempre responda em português, "
                        "use os recursos disponíveis de forma eficiente e evite repetir ações. "
                        "Dê uma única resposta clara e objetiva para o usuário."
                    )
                },
                memory=memory,
                verbose=True,
                handle_parsing_errors=True,
            )

            print(f"SETUP: {type(agent_executor)}")
            return agent_executor

        except Exception as e:
            print(f"Erro no setup_full_agent: {e}")
            return ServiceResponse.error(
                ServiceResponse.INTERNAL_ERROR,
                status_code=500
            )

    @log_execution
    @beartype
    async def get_jwt_service(
        self, 
        username: str, 
        password: str) -> ServiceResponse:
        try:
            if username == "admin" and password == "1234":
                token = await self.jwt_auth.generate_jwt(user_id=1)
                return ServiceResponse.success(token)

            return ServiceResponse.error(
                ServiceResponse.TOKEN_NOT_GENERATED, status_code=401
            )

        except Exception as e:
            print(f"Erro ao gerar token: {e}")
            return ServiceResponse.error(
                ServiceResponse.INTERNAL_ERROR, status_code=500
            )
