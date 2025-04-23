from src.tools.agent_tools import RetrieveAndGenerateAgentTolls

def get_all_tools():
    retrieve_tool = RetrieveAndGenerateAgentTolls()
    return [
        retrieve_tool.to_tool(),
        # Aqui você pode adicionar outras tools futuramente
    ]
