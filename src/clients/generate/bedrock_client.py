from beartype import beartype
from langchain_aws import ChatBedrock
from langchain_core.messages import HumanMessage

from src.logger import log_execution


class BedrockLangchainClient:
    def __init__(self):
        self.llm = ChatBedrock(
            model="us.anthropic.claude-3-7-sonnet-20250219-v1:0",
            region="us-east-1",
            max_tokens=1500,
            model_kwargs={"thinking": {"type": "enabled", "budget_tokens": 1024}},
        )

    @log_execution
    @beartype
    async def bedrock_with_langchain_client(self, input: str) -> str:
        print("TO AQUI NO CLIENT BEDROCK")
        try:
            human_msg = HumanMessage(content=input)
            ai_msg = self.llm.invoke([human_msg])
            print(ai_msg.additional_kwargs["thinking"]["text"])
            print(f"TYPEOF {type(ai_msg)}")
            return ai_msg.content
        except Exception as e:
            print(f"Erro ao criar item: {e}")
            return "Erro interno no servidor", 500
