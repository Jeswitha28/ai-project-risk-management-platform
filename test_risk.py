import json
from agents import risk_agent

print(json.dumps(risk_agent.run(), indent=2, ensure_ascii=False))