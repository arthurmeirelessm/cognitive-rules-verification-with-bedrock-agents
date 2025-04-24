from typing import List
from langchain_core.tools import StructuredTool
from src.tools.agent_tools import RetrieveAndGenerateTool

def get_all_tools() -> List[StructuredTool]:
    retrieve_tool = RetrieveAndGenerateTool()
    return [retrieve_tool.to_tool()]
