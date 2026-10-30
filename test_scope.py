import json
from agents import scope_agent

result = scope_agent.run()
print(json.dumps(result, indent=2, ensure_ascii=False))