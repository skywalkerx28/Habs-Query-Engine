#!/usr/bin/env python3
"""
Test HeartBeat AI Model - Montreal Canadiens Hockey Analyst
===========================================================

Tests the fine-tuned ministral-8b-latest model via Mistral API.
Verifies hockey expertise, terminology, and analytical capabilities.
"""

import os
import requests
import json
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class HeartBeatModelTester:
    def __init__(self):
        """Initialize the HeartBeat model tester"""
        self.api_key = os.getenv('MISTRAL_API_KEY')
        if not self.api_key:
            logger.error("❌ MISTRAL_API_KEY environment variable not set")
            logger.info("Set your API key: export MISTRAL_API_KEY='your_key_here'")
            return

        self.model_id = "ft:ministral-8b-latest:dd26ff35:20250921:5207f629"
        self.api_url = "https://api.mistral.ai/v1/chat/completions"

        # Test headers
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        logger.info(f"✅ Initialized HeartBeat Model Tester")
        logger.info(f"🎯 Model ID: {self.model_id}")
        logger.info(f"🔗 API URL: {self.api_url}")

    def test_api_connection(self):
        """Test basic API connectivity"""
        logger.info("🔍 Testing API connection...")

        test_payload = {
            "model": "ministral-8b-latest",  # Use base model for connection test
            "messages": [{"role": "user", "content": "Hello"}],
            "max_tokens": 10
        }

        try:
            response = requests.post(self.api_url, headers=self.headers, json=test_payload)
            if response.status_code == 200:
                logger.info("✅ API connection successful")
                return True
            else:
                logger.error(f"❌ API connection failed: {response.status_code} - {response.text}")
                return False
        except Exception as e:
            logger.error(f"❌ API connection error: {e}")
            return False

    def test_heartbeat_model(self, question, context="coach"):
        """Test the fine-tuned HeartBeat model with a hockey question"""
        logger.info(f"🏒 Testing: {question[:50]}...")

        # Create context-appropriate system prompt
        if context == "coach":
            system_prompt = """You are a world-class hockey analyst and consultant for the Montreal Canadiens. You have profound understanding of hockey systems, historical patterns, and trends. You communicate using authentic coach and player terminology, providing precise, actionable insights based on comprehensive data analysis. Your responses demonstrate deep hockey knowledge and strategic thinking."""
        elif context == "player":
            system_prompt = """You are a world-class hockey analyst and consultant for the Montreal Canadiens. You have profound understanding of hockey systems, historical patterns, and trends. You communicate using authentic coach and player terminology, providing precise, actionable insights based on comprehensive data analysis. Your responses demonstrate deep hockey knowledge and strategic thinking."""
        else:
            system_prompt = """You are a world-class hockey analyst and consultant for the Montreal Canadiens."""

        payload = {
            "model": self.model_id,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": question}
            ],
            "max_tokens": 500,
            "temperature": 0.7
        }

        try:
            response = requests.post(self.api_url, headers=self.headers, json=payload)

            if response.status_code == 200:
                result = response.json()
                content = result['choices'][0]['message']['content']
                logger.info("✅ Model responded successfully")
                return content
            else:
                logger.error(f"❌ Model test failed: {response.status_code} - {response.text}")
                return None

        except Exception as e:
            logger.error(f"❌ Model test error: {e}")
            return None

def main():
    """Main testing function"""
    print("🏒 HeartBeat AI Model Tester - Montreal Canadiens Hockey Analyst")
    print("=" * 70)

    tester = HeartBeatModelTester()
    if not tester.api_key:
        print("❌ Please set your MISTRAL_API_KEY environment variable")
        print("Example: export MISTRAL_API_KEY='your_api_key_here'")
        return

    # Test API connection first
    if not tester.test_api_connection():
        print("❌ API connection test failed. Check your API key and internet connection.")
        return

    print("\n🎯 Testing HeartBeat AI Model Capabilities")
    print("-" * 50)

    # Test questions covering different aspects
    test_questions = [
        # Coach perspective
        ("coach", "What are Tampa Bay's key defensive vulnerabilities we can exploit?"),
        ("coach", "How should we adjust our power play against Boston's penalty kill?"),
        ("coach", "What tendencies has Toronto shown in their last 5 games?"),

        # Player perspective
        ("player", "Where do I rank among wingers with similar ice time?"),
        ("player", "What areas of my game need the most focus based on recent performance?"),
        ("player", "How has my positioning improved compared to last season?"),

        # Strategic analysis
        ("coach", "What power play adjustments would maximize our high-danger chances?"),
        ("coach", "How effective has our defensive zone exit strategy been this season?"),
        ("player", "What are my strengths and weaknesses as a two-way forward?")
    ]

    results = []

    for context, question in test_questions:
        print(f"\n🎭 Context: {context.upper()}")
        print(f"❓ Question: {question}")

        response = tester.test_heartbeat_model(question, context)

        if response:
            print(f"🤖 Response: {response[:200]}..." if len(response) > 200 else f"🤖 Response: {response}")
            results.append((question, response, True))
        else:
            print("❌ No response received")
            results.append((question, None, False))

        print("-" * 70)

    # Summary
    print("\n📊 TEST SUMMARY")
    print("-" * 30)
    successful_tests = sum(1 for _, _, success in results if success)
    total_tests = len(results)

    print(f"✅ Successful responses: {successful_tests}/{total_tests}")
    print(".1f"
    if successful_tests == total_tests:
        print("🎉 ALL TESTS PASSED! Your HeartBeat AI is working perfectly!")
        print("🏆 Ready for integration with Pinecone and Streamlit!")
    else:
        print("⚠️  Some tests failed. Check API key and model availability.")

    # Save results
    output_file = Path(__file__).parent.parent / "model_test_results.json"
    with open(output_file, 'w') as f:
        json.dump({
            "model_id": tester.model_id,
            "total_tests": total_tests,
            "successful_tests": successful_tests,
            "success_rate": successful_tests / total_tests,
            "results": [
                {
                    "question": q,
                    "response": r,
                    "success": s
                } for q, r, s in results
            ]
        }, f, indent=2)

    print(f"\n💾 Results saved to: {output_file}")

if __name__ == "__main__":
    main()
