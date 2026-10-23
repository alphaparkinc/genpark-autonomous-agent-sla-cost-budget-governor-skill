"""MCP server for Autonomous Agent SLA Cost & Budget Governor."""
import sys
import json
from client import AgentSLACostGovernor

def handle_request(req):
    method = req.get("method")
    if method == "tools/list":
        return {
            "tools": [{
                "name": "evaluate_agent_budget_governance",
                "description": "Evaluates spend and latency to decide model throttling or downgrade",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "current_spend_usd": {"type": "number"},
                        "max_budget_usd": {"type": "number"},
                        "current_latency_ms": {"type": "number"},
                        "sla_max_latency_ms": {"type": "number"}
                    },
                    "required": ["current_spend_usd", "max_budget_usd", "current_latency_ms"]
                }
            }]
        }
    elif method == "tools/call":
        params = req.get("params", {})
        if params.get("name") == "evaluate_agent_budget_governance":
            args = params.get("arguments", {})
            res = AgentSLACostGovernor.evaluate_budget_governance(
                float(args.get("current_spend_usd", 0.0)),
                float(args.get("max_budget_usd", 1.0)),
                float(args.get("current_latency_ms", 0.0)),
                float(args.get("sla_max_latency_ms", 3000.0))
            )
            return {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}
    return {"error": "Method not found"}

if __name__ == "__main__":
    for line in sys.stdin:
        if line.strip():
            print(json.dumps(handle_request(json.loads(line))))
            sys.stdout.flush()
