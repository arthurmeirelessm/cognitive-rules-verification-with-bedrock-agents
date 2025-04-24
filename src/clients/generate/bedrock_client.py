from langchain_aws import ChatBedrockConverse
from langchain_core.messages import SystemMessage, HumanMessage
from beartype import beartype
from src.logger import log_execution

class BedrockLangchainClient:
    def __init__(self):
        self.llm = ChatBedrockConverse(
            model="us.anthropic.claude-3-7-sonnet-20250219-v1:0",
            temperature=1.0,
            top_p=0.9,
            max_tokens=5000,
            region_name="us-east-1",
            disable_streaming=True,
            cache=False
        )

    @log_execution
    @beartype
    async def bedrock_with_langchain_client(self, input: str) -> str:
        try:
            messages = [
                HumanMessage(content=input),
            ]
            response = await self.llm.ainvoke(messages)
            return response.content
        except Exception as e:
            print(f"Erro ao chamar Bedrock: {e}")
            return "Erro interno no servidor"
