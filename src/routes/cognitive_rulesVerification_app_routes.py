from quart import Blueprint

from src.controllers.cognitive_rulesVerification_app_controller import (
    CognitiveRulesVerificationAppController,
)


class CognitiveRulesVerificationAppRoutes:
    def __init__(self):
        self.cognitive_rules_verification_app_blueprint = Blueprint(
            "cognitive_rules_verification_app_blueprint", __name__
        )
        self.cognitive_rules_verification_app_controller = CognitiveRulesVerificationAppController()
        self._register_routes()

    def _register_routes(self):
        self.cognitive_rules_verification_app_blueprint.add_url_rule(
            "/agent_orchestrator",
            view_func=self.cognitive_rules_verification_app_controller.agent_orchestrator_controller,
            methods=["POST"],
        )

        self.cognitive_rules_verification_app_blueprint.add_url_rule(
            "/get_jwt",
            view_func=self.cognitive_rules_verification_app_controller.get_jwt_controller,
            methods=["GET"],
        )
