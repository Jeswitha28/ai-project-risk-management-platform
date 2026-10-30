import json
from agents import blocker_agent

print(json.dumps(blocker_agent.run(), indent=2, ensure_ascii=False))