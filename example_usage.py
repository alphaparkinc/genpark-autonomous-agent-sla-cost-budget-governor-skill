"""Example usage for Autonomous Agent SLA Cost & Budget Governor."""
from client import AgentSLACostGovernor

if __name__ == "__main__":
    res = AgentSLACostGovernor.evaluate_budget_governance(8.5, 10.0, 1200.0)
    print("Action:", res["governance_action"], "Model Tier:", res["assigned_model_tier"])
