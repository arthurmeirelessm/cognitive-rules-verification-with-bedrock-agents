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
            result = agent_executor.invoke(
                {
                    "input": user_input,
                    "chat_history": chat_history,
                }
            )
            print("Action escolhida:", result)
            print("Action escolhida:", result.get("action"))
            print("tool_input   :", result.get("tool_input"))
            
            chat_history.append(HumanMessage(content=user_input))
            output = result.get("output", "Resposta não gerada.")
            chat_history.append(AIMessage(content="Assistant: " + output))
            
            return output

        except Exception as e:
            print(f"Erro no service: {e}")
            return ServiceResponse.error(
                ServiceResponse.INTERNAL_ERROR, status_code=500
            )

    @log_execution
    @beartype
    async def setup_full_agent(self) -> AgentExecutor | ServiceResponse:
        try:
            llm = ChatBedrock(
                model_id="us.anthropic.claude-3-7-sonnet-20250219-v1:0",
                model_kwargs={"temperature": 0.3},
            )

            retrieve_and_generate = StructuredTool.from_function(
                name="retrieve_and_generate", 
                func=self.retrieve_and_generate_tool.retrieve_and_generate,
                description="Busca e gera resposta baseada em receitas e consultas de culinária"
            )

            chat_message_int = MessagesPlaceholder(variable_name="chat_history")
            memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

            agent_executor = initialize_agent(
                [retrieve_and_generate],
                llm,
                agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
                agent_kwargs={
                    "prefix": (
                        "Você é um assistente útil e objetivo. Ao receber uma pergunta do usuário:\n"
                        "- Perguntas gerais → responda direto (Final Answer).\n"
                        "- Perguntas de culinária → use retrieve_and_generate.\n\n"
                        "Sempre retorne **exatamente** um bloco JSON com action + action_input."
                    ),
                    "suffix": (
                        "\nAction:\n```json\n"
                        "{{\n"
                        "  \"action\": \"Final Answer\",  \n"
                        "  \"action_input\": \"<resposta aqui>\"\n"
                        "}}\n"
                        "```\n"
                    ),
                    "memory_prompts": [chat_message_int],
                    "input_variables": ["input", "agent_scratchpad", "chat_history"],
                },
                memory=memory,
                verbose=True,
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
