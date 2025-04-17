import asyncio
from quart import Quart
from src.routes.cognitive_rulesVerification_app_routes import CognitiveRulesVerificationAppRoutes


app = Quart(__name__)

cognitiveRulesVerificationAppRoutes = CognitiveRulesVerificationAppRoutes()
app.register_blueprint(cognitiveRulesVerificationAppRoutes.cognitive_rules_verification_app_blueprint)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)