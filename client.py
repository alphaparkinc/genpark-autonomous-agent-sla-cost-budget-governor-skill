"""Autonomous Agent SLA Cost & Budget Governor.
100% Python Standard Library.
"""

class AgentSLACostGovernor:
    """Dynamically monitors accumulated token consumption and financial spend to trigger model downgrade or throttling."""

    @staticmethod
    def evaluate_budget_governance(current_spend_usd: float, max_budget_usd: float, current_latency_ms: float, sla_max_latency_ms: float = 3000.0) -> dict:
        spend_ratio = current_spend_usd / max(0.01, max_budget_usd)
        latency_exceeded = current_latency_ms > sla_max_latency_ms

        if spend_ratio >= 1.0:
            action = "TERMINATE_BUDGET_EXCEEDED"
            model_tier = "NONE"
        elif spend_ratio >= 0.8:
            action = "DOWNGRADE_TO_FAST_MODEL"
            model_tier = "ECONOMY_FLASH"
        elif latency_exceeded:
            action = "DEGRADE_REASONING_STEPS"
            model_tier = "BALANCED_TURBO"
        else:
            action = "NORMAL_EXECUTION"
            model_tier = "PREMIUM_PRO"

        return {
            "current_spend_usd": round(current_spend_usd, 4),
            "budget_usage_pct": round(spend_ratio * 100.0, 1),
            "governance_action": action,
            "assigned_model_tier": model_tier
        }
