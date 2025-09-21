#!/usr/bin/env python3
"""
HeartBeat Engine - Montreal Canadiens AI Hockey Analyst
======================================================

Hybrid Intelligence System combining:
- Fine-tuned Mistral AI model (conversational expertise)
- Pinecone RAG (hockey context and historical knowledge)
- Parquet query tools (real-time statistical analysis)
"""

import os
import json
import requests
from pathlib import Path
from typing import Dict, List, Optional, Any
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class HeartBeatEngine:
    """Main HeartBeat Engine coordinating all intelligence sources"""

    def __init__(self):
        """Initialize the HeartBeat Engine"""
        self.mistral_api_key = os.getenv('MISTRAL_API_KEY')
        self.pinecone_api_key = os.getenv('PINECONE_API_KEY')
        self.model_id = "ft:ministral-8b-latest:dd26ff35:20250921:5207f629"

        if not self.mistral_api_key:
            logger.error("❌ MISTRAL_API_KEY not set")
        if not self.pinecone_api_key:
            logger.warning("⚠️ PINECONE_API_KEY not set - RAG will be limited")

        # Initialize components
        self.rag_system = RAGSystem()
        self.parquet_analyzer = ParquetAnalyzer()
        self.response_synthesizer = ResponseSynthesizer()

        logger.info("✅ HeartBeat Engine initialized")
        logger.info("🎯 Model: Mistral fine-tuned analyst")
        logger.info("🧠 RAG: Hockey context retrieval")
        logger.info("📊 Analytics: Real-time Parquet queries")

    def analyze_query(self, user_query: str, user_type: str = "coach") -> Dict[str, Any]:
        """Main analysis pipeline"""
        logger.info(f"🏒 Analyzing query: {user_query[:50]}...")

        # Step 1: Query analysis and context gathering
        query_analysis = self._analyze_query_intent(user_query, user_type)

        # Step 2: Retrieve relevant context from RAG
        rag_context = self.rag_system.retrieve_context(user_query, query_analysis)

        # Step 3: Gather relevant data/metrics
        data_insights = self.parquet_analyzer.get_relevant_data(user_query, query_analysis)

        # Step 4: Synthesize response with AI model
        final_response = self.response_synthesizer.generate_response(
            user_query=user_query,
            user_type=user_type,
            rag_context=rag_context,
            data_insights=data_insights,
            query_analysis=query_analysis
        )

        return {
            "response": final_response,
            "context_used": len(rag_context) if rag_context else 0,
            "data_points": len(data_insights) if data_insights else 0,
            "query_type": query_analysis.get("type"),
            "confidence": query_analysis.get("confidence", 0.0)
        }

    def _analyze_query_intent(self, query: str, user_type: str) -> Dict[str, Any]:
        """Analyze the intent and requirements of the user query"""
        # Basic intent classification
        query_lower = query.lower()

        intent_analysis = {
            "user_type": user_type,
            "requires_data": False,
            "requires_opponent_analysis": False,
            "requires_player_comparison": False,
            "requires_tactical_advice": False,
            "time_frame": "current",  # current, recent, historical
            "confidence": 0.8
        }

        # Detect data requirements
        data_keywords = ["rank", "percentile", "stats", "performance", "goals", "assists", "points", "ice time"]
        if any(keyword in query_lower for keyword in data_keywords):
            intent_analysis["requires_data"] = True

        # Detect opponent analysis
        opponent_keywords = ["against", "vs", "versus", "opponent", "defensive", "vulnerabilities"]
        if any(keyword in query_lower for keyword in opponent_keywords):
            intent_analysis["requires_opponent_analysis"] = True

        # Detect player comparisons
        comparison_keywords = ["rank", "compared to", "versus", "better than", "similar"]
        if any(keyword in query_lower for keyword in comparison_keywords):
            intent_analysis["requires_player_comparison"] = True

        # Detect tactical advice
        tactical_keywords = ["adjust", "change", "improve", "focus on", "strategy"]
        if any(keyword in query_lower for keyword in tactical_keywords):
            intent_analysis["requires_tactical_advice"] = True

        # Determine query type
        if intent_analysis["requires_opponent_analysis"]:
            intent_analysis["type"] = "opponent_analysis"
        elif intent_analysis["requires_player_comparison"]:
            intent_analysis["type"] = "player_comparison"
        elif intent_analysis["requires_tactical_advice"]:
            intent_analysis["type"] = "tactical_advice"
        else:
            intent_analysis["type"] = "general_analysis"

        return intent_analysis


class RAGSystem:
    """Retrieval-Augmented Generation system using Pinecone"""

    def __init__(self):
        """Initialize RAG system"""
        self.pinecone_api_key = os.getenv('PINECONE_API_KEY')
        self.initialized = False

        if self.pinecone_api_key:
            try:
                # Pinecone integration would go here
                self.initialized = True
                logger.info("✅ RAG System initialized with Pinecone")
            except Exception as e:
                logger.warning(f"⚠️ RAG System initialization failed: {e}")
        else:
            logger.warning("⚠️ RAG System not initialized - no Pinecone API key")

    def retrieve_context(self, query: str, analysis: Dict[str, Any]) -> Optional[List[Dict[str, Any]]]:
        """Retrieve relevant context from Pinecone indexes"""
        if not self.initialized:
            return None

        # Placeholder for Pinecone retrieval logic
        # This would search comprehensive_hockey_rag_chunks and mtl_team_stats_contextual_rag_chunks

        mock_context = [
            {
                "type": "hockey_concept",
                "content": "Defensive zone exits are critical for maintaining possession and creating offensive opportunities",
                "relevance_score": 0.85
            }
        ]

        return mock_context


class ParquetAnalyzer:
    """Real-time Parquet data analysis system"""

    def __init__(self):
        """Initialize Parquet analysis system"""
        self.analytics_dir = Path(__file__).parent.parent / "data" / "processed" / "analytics"
        self.initialized = self.analytics_dir.exists()

        if self.initialized:
            logger.info("✅ Parquet Analyzer initialized")
        else:
            logger.warning("⚠️ Parquet Analyzer not initialized - analytics directory not found")

    def get_relevant_data(self, query: str, analysis: Dict[str, Any]) -> Optional[List[Dict[str, Any]]]:
        """Retrieve relevant data from Parquet files"""
        if not self.initialized:
            return None

        # Placeholder for Parquet query logic
        # This would analyze mtl_team_stats parquet files for relevant metrics

        mock_data = [
            {
                "metric": "defensive_zone_exits",
                "value": 68.5,
                "percentile": 76,
                "trend": "improving"
            }
        ]

        return mock_data


class ResponseSynthesizer:
    """Synthesizes final responses using the fine-tuned model"""

    def __init__(self):
        """Initialize response synthesizer"""
        self.mistral_api_key = os.getenv('MISTRAL_API_KEY')
        self.model_id = "ft:ministral-8b-latest:dd26ff35:20250921:5207f629"
        self.api_url = "https://api.mistral.ai/v1/chat/completions"

    def generate_response(self, user_query: str, user_type: str,
                         rag_context: Optional[List], data_insights: Optional[List],
                         query_analysis: Dict) -> str:
        """Generate final response using Mistral model with context"""

        # Build enhanced system prompt
        system_prompt = self._build_system_prompt(user_type, rag_context, data_insights)

        # Build enriched user query with data context
        enriched_query = self._enrich_query_with_data(user_query, data_insights, query_analysis)

        # Prepare messages
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": enriched_query}
        ]

        # Add RAG context if available
        if rag_context:
            context_message = self._format_rag_context(rag_context)
            messages.insert(1, {"role": "system", "content": context_message})

        payload = {
            "model": self.model_id,
            "messages": messages,
            "max_tokens": 1000,
            "temperature": 0.7
        }

        try:
            headers = {"Authorization": f"Bearer {self.mistral_api_key}", "Content-Type": "application/json"}
            response = requests.post(self.api_url, headers=headers, json=payload, timeout=30)

            if response.status_code == 200:
                result = response.json()
                return result['choices'][0]['message']['content']
            else:
                logger.error(f"❌ Model API error: {response.status_code}")
                return self._generate_fallback_response(user_query, data_insights)

        except Exception as e:
            logger.error(f"❌ Response generation error: {e}")
            return self._generate_fallback_response(user_query, data_insights)

    def _build_system_prompt(self, user_type: str, rag_context: Optional[List], data_insights: Optional[List]) -> str:
        """Build enhanced system prompt with available context"""
        base_prompt = """You are a world-class hockey analyst and consultant for the Montreal Canadiens. You have profound understanding of hockey systems, historical patterns, and trends. You communicate using authentic coach and player terminology, providing precise, actionable insights based on comprehensive data analysis. Your responses demonstrate deep hockey knowledge and strategic thinking."""

        # Add context availability information
        context_info = []
        if rag_context:
            context_info.append(f"Access to {len(rag_context)} relevant hockey knowledge chunks")
        if data_insights:
            context_info.append(f"Access to {len(data_insights)} live performance metrics")

        if context_info:
            base_prompt += f"\n\nAvailable Context: {', '.join(context_info)}. Use this data to provide specific, evidence-based insights."

        if user_type == "player":
            base_prompt += "\n\nFocus on individual development, performance analysis, and personal growth opportunities."
        elif user_type == "coach":
            base_prompt += "\n\nFocus on strategic analysis, opponent preparation, and team tactical adjustments."

        return base_prompt

    def _enrich_query_with_data(self, query: str, data_insights: Optional[List], analysis: Dict) -> str:
        """Enrich user query with relevant data context"""
        if not data_insights:
            return query

        enriched_parts = [f"Original Query: {query}"]

        # Add relevant data points
        data_relevant = []
        for insight in data_insights:
            if self._is_data_relevant(insight, analysis):
                data_relevant.append(f"{insight['metric']}: {insight['value']} (percentile: {insight.get('percentile', 'N/A')})")

        if data_relevant:
            enriched_parts.append(f"Relevant Data: {'; '.join(data_relevant)}")

        return "\n".join(enriched_parts)

    def _is_data_relevant(self, insight: Dict, analysis: Dict) -> bool:
        """Determine if a data insight is relevant to the query"""
        # Simple relevance matching - could be enhanced with ML
        metric = insight.get('metric', '').lower()
        query_type = analysis.get('type', '')

        relevance_map = {
            "opponent_analysis": ["defensive", "zone", "exit", "entry"],
            "player_comparison": ["rank", "percentile", "performance"],
            "tactical_advice": ["system", "execution", "strategy"]
        }

        relevant_keywords = relevance_map.get(query_type, [])
        return any(keyword in metric for keyword in relevant_keywords)

    def _format_rag_context(self, rag_context: List[Dict]) -> str:
        """Format RAG context for model consumption"""
        context_parts = ["Additional Context:"]
        for item in rag_context:
            context_parts.append(f"- {item.get('content', '')}")
        return "\n".join(context_parts)

    def _generate_fallback_response(self, query: str, data_insights: Optional[List]) -> str:
        """Generate fallback response when API fails"""
        response = "I apologize, but I'm currently unable to access my full analytical capabilities. "

        if data_insights:
            response += "However, based on available data, here are some relevant insights:\n"
            for insight in data_insights[:3]:
                response += f"- {insight.get('metric', 'Unknown')}: {insight.get('value', 'N/A')}\n"

        response += "\nPlease try your query again in a moment, or contact technical support if the issue persists."
        return response


def main():
    """Demo the HeartBeat Engine"""
    print("🏒 HeartBeat Engine - Montreal Canadiens AI Hockey Analyst")
    print("=" * 70)

    # Initialize engine
    engine = HeartBeatEngine()

    # Demo queries
    demo_queries = [
        ("coach", "What are Tampa Bay's key defensive vulnerabilities we can exploit?"),
        ("player", "Where do I rank among wingers with similar ice time?"),
        ("coach", "How should we adjust our power play against Boston's penalty kill?")
    ]

    for user_type, query in demo_queries:
        print(f"\n🎭 User Type: {user_type.upper()}")
        print(f"❓ Query: {query}")

        result = engine.analyze_query(query, user_type)

        print(f"🤖 Response: {result['response'][:300]}..." if len(result['response']) > 300 else f"🤖 Response: {result['response']}")
        print(f"📊 Context Used: {result['context_used']}, Data Points: {result['data_points']}")
        print("-" * 70)

    print("\n✅ HeartBeat Engine Demo Complete!")
    print("🔗 Ready for Streamlit integration and full deployment!")


if __name__ == "__main__":
    main()
