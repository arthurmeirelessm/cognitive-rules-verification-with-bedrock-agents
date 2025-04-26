from beartype import beartype
from quart import Response, jsonify, request
from src.utils.response_utils import ServiceResponse
from src.logger import log_execution
from src.services.cognitive_rulesVerification_app_service import (
    CognitiveRulesVerificationAppServices,
)


class CognitiveRulesVerificationAppController:
    def __init__(self):
        self.run_test_service = CognitiveRulesVerificationAppServices()


    @log_execution
    @beartype
    async def agent_orchestrator_controller(self) -> Response:
        auth_header = request.headers.get("Authorization", "")
        data = await request.get_json()
        user_input = data.get("input", "")

        resp: ServiceResponse = await self.run_test_service.agent_orchestrator_service(
            auth_header, user_input
        )

        payload = {
            "message": resp.message,
            "status":  "success" if resp.status_code == 200 else "error"
        }

        response: Response = jsonify(payload)
        response.status_code = resp.status_code
        return response
        
        
        
        
    @log_execution
    @beartype
    async def get_jwt_controller(self) -> Response:
        username = request.args.get("username", "")
        password = request.args.get("password", "")

        resp: ServiceResponse = await self.run_test_service.get_jwt_service(
            username, password
        )

        payload = {
            "message": resp.message,
            "status":  "success" if resp.status_code == 200 else "error"
        }

        response: Response = jsonify(payload)
        response.status_code = resp.status_code
        return response
        
        