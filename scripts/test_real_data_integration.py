#!/usr/bin/env python3
"""
HeartBeat Engine - Real Data Integration Test
Montreal Canadiens Advanced Analytics Assistant

Test script to validate real Pinecone and Parquet data integration.
"""

import asyncio
import logging
from orchestrator.tools.pinecone_mcp_client import PineconeMCPClient
from orchestrator.tools.parquet_data_client import ParquetDataClient

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

async def test_pinecone_integration():
    """Test real Pinecone MCP integration"""
    
    print("=== Testing Pinecone MCP Integration ===\n")
    
    client = PineconeMCPClient()
    
    # Test searches in different namespaces
    test_queries = [
        {
            "query": "Montreal Canadiens Suzuki performance",
            "namespace": "events",
            "description": "Player performance in events namespace"
        },
        {
            "query": "hockey analytics expected goals",
            "namespace": "prose", 
            "description": "Hockey knowledge in prose namespace"
        },
        {
            "query": "powerplay statistics Montreal",
            "namespace": "events",
            "description": "Team statistics in events namespace"
        }
    ]
    
    for i, test in enumerate(test_queries, 1):
        print(f"--- Test {i}: {test['description']} ---")
        print(f"Query: {test['query']}")
        print(f"Namespace: {test['namespace']}")
        
        try:
            results = await client.search_hockey_context(
                query=test["query"],
                namespace=test["namespace"],
                top_k=3
            )
            
            print(f"Results found: {len(results)}")
            
            for j, result in enumerate(results, 1):
                print(f"  {j}. Score: {result.get('relevance_score', 0):.3f}")
                print(f"     Content: {result.get('content', '')[:100]}...")
                print(f"     Source: {result.get('source', 'unknown')}")
            
        except Exception as e:
            print(f"Error: {str(e)}")
        
        print()

async def test_parquet_integration():
    """Test real Parquet data integration"""
    
    print("=== Testing Parquet Data Integration ===\n")
    
    client = ParquetDataClient("data/processed")
    
    # Test different data access methods
    tests = [
        {
            "method": "get_available_data_sources",
            "args": {},
            "description": "Available data sources"
        },
        {
            "method": "get_player_performance", 
            "args": {"player_names": ["Suzuki", "Caufield"], "timeframe": "current_season"},
            "description": "Player performance data"
        },
        {
            "method": "get_team_analytics",
            "args": {"team": "MTL", "analysis_type": "general"},
            "description": "Team analytics data"
        },
        {
            "method": "get_advanced_metrics",
            "args": {"metric_type": "xg", "team": "MTL"},
            "description": "Advanced metrics (xG)"
        },
        {
            "method": "get_line_combinations",
            "args": {"unit_type": "forwards"},
            "description": "Line combinations"
        }
    ]
    
    for i, test in enumerate(tests, 1):
        print(f"--- Test {i}: {test['description']} ---")
        
        try:
            method = getattr(client, test["method"])
            
            if asyncio.iscoroutinefunction(method):
                result = await method(**test["args"])
            else:
                result = method(**test["args"])
            
            print(f"Success: {not ('error' in result)}")
            
            if "error" in result:
                print(f"Error: {result['error']}")
            else:
                # Show key result information
                if "data_source" in result:
                    print(f"Data source: {result['data_source']}")
                if "total_records" in result:
                    print(f"Total records: {result['total_records']}")
                if "columns" in result:
                    print(f"Columns: {len(result['columns'])} ({', '.join(result['columns'][:5])}...)")
                if "sample_data" in result and result["sample_data"]:
                    print(f"Sample records: {len(result['sample_data'])}")
            
        except Exception as e:
            print(f"Error: {str(e)}")
        
        print()

async def test_end_to_end_integration():
    """Test end-to-end integration with orchestrator"""
    
    print("=== Testing End-to-End Integration ===\n")
    
    try:
        from orchestrator import orchestrator, UserContext, UserRole
        
        # Create test user
        test_user = UserContext(
            user_id="integration_test",
            role=UserRole.ANALYST,
            name="Integration Tester",
            team_access=["MTL"]
        )
        
        # Test query with real data
        test_query = "How is Suzuki performing this season with advanced metrics?"
        
        print(f"Processing query: {test_query}")
        
        result = await orchestrator.process_query(
            query=test_query,
            user_context=test_user
        )
        
        print(f"Success: {result.get('success', True)}")
        print(f"Query type: {result.get('query_type', 'unknown')}")
        print(f"Processing time: {result.get('processing_time_ms', 0)}ms")
        print(f"Tools used: {len(result.get('tool_results', []))}")
        
        # Show tool results
        for tool_result in result.get('tool_results', []):
            print(f"  - {tool_result.get('tool', 'unknown')}: {tool_result.get('success', False)}")
        
        print(f"Response: {result.get('response', 'No response')[:200]}...")
        
    except Exception as e:
        print(f"End-to-end test failed: {str(e)}")

async def main():
    """Main test function"""
    
    print("HeartBeat Engine - Real Data Integration Tests\n")
    
    # Test Pinecone integration
    await test_pinecone_integration()
    
    # Test Parquet integration  
    await test_parquet_integration()
    
    # Test end-to-end integration
    await test_end_to_end_integration()
    
    print("=== All Tests Complete ===")

if __name__ == "__main__":
    asyncio.run(main())
