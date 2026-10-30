import json
import os
from agents import scope_agent, risk_agent, blocker_agent

os.makedirs("outputs", exist_ok=True)

print("Detective 1: Scope and Deliverables...")
scope = scope_agent.run()
print("Detective 2: Risk and Forecast...")
risk = risk_agent.run()
print("Detective 3: Blockers and Action Items...")
blockers = blocker_agent.run()

report = {"scope": scope, "risk": risk, "blockers": blockers}

with open("outputs/results.json", "w", encoding="utf-8") as f:
    json.dump(report, f, indent=2, ensure_ascii=False)

print(json.dumps(report, indent=2, ensure_ascii=False))
print("\nSaved to outputs/results.json")