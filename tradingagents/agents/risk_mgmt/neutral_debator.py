import time
import json


def create_neutral_debator(llm, config):
    def neutral_node(state) -> dict:
        risk_debate_state = state["risk_debate_state"]
        history = risk_debate_state.get("history", "")
        neutral_history = risk_debate_state.get("neutral_history", "")

        current_risky_response = risk_debate_state.get("current_risky_response", "")
        current_safe_response = risk_debate_state.get("current_safe_response", "")

        market_research_report = state["market_report"]
        sentiment_report = state["sentiment_report"]
        news_report = state["news_report"]
        fundamentals_report = state["fundamentals_report"]

        trader_decision = state["trader_investment_plan"]

        # Get language instruction from config
        lang_instruction = config.get("language_instruction", "IMPORTANT: Always respond in English.")

        task_prompt = f"""As the Neutral Risk Analyst, your role is to provide a balanced perspective, weighing both the potential benefits and risks of the trader's decision or plan. You prioritize a comprehensive approach, evaluating the pros and cons while considering broader market trends, potential economic shifts, and diversification strategies. Here is the trader's decision:

{trader_decision}

Your task is to challenge both the Aggressive and Conservative Analysts, pointing out where each perspective may be too optimistic or overly cautious. Use insights from the following data sources to support a moderate, sustainable strategy for adjusting the trader's decision:

Market Research Report: {market_research_report}
Social Media Sentiment Report: {sentiment_report}
Latest World Affairs Report: {news_report}
Company Fundamentals Report: {fundamentals_report}
Here is the current conversation history: {history} Here is the latest response from the aggressive analyst: {current_risky_response} Here is the latest response from the conservative analyst: {current_safe_response}. If there are no responses from the other viewpoints, do not hallucinate and just present your point.

Actively engage by analyzing both sides critically, addressing weaknesses in the aggressive and conservative arguments to advocate for a more balanced approach. Challenge each of their points to illustrate why a moderate-risk strategy might offer the best of both worlds, providing growth potential while protecting against extreme volatility. Focus on debating rather than just presenting data, aiming to show that a balanced view can lead to the most reliable outcomes. Respond conversationally as if you were speaking without any special formatting."""

        prompt = f"{lang_instruction}\n{task_prompt}"

        response = llm.invoke(prompt)

        argument = f"Analista Neutral: {response.content}"

        new_risk_debate_state = {
            "history": history + "\n" + argument,
            "risky_history": risk_debate_state.get("risky_history", ""),
            "safe_history": risk_debate_state.get("safe_history", ""),
            "neutral_history": neutral_history + "\n" + argument,
            "latest_speaker": "Neutral",
            "current_risky_response": risk_debate_state.get(
                "current_risky_response", ""
            ),
            "current_safe_response": risk_debate_state.get("current_safe_response", ""),
            "current_neutral_response": argument,
            "count": risk_debate_state["count"] + 1,
        }

        return {"risk_debate_state": new_risk_debate_state}

    return neutral_node
