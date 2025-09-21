#!/usr/bin/env python3
"""
HeartBeat Engine Environment Setup
=================================

Sets up API keys and validates the complete HeartBeat Engine system.
"""

import os
import sys
from pathlib import Path

def setup_environment():
    """Setup environment variables for HeartBeat Engine"""
    
    print("🏒 HeartBeat Engine - Environment Setup")
    print("=" * 50)
    
    # Set API keys
    mistral_key = "BBCr4na8MIUkBxdy1FV0dBoPGR8d8wya"
    pinecone_key = "pcsk_44JqgP_2oVeUVWd9Lk8MRrinaoKoZEYjJueDm1kEXhpJQiWCruWvJ58oyQVWSq5h7Cd3po"
    
    # Set environment variables
    os.environ['MISTRAL_API_KEY'] = mistral_key
    os.environ['PINECONE_API_KEY'] = pinecone_key
    
    print(f"✅ MISTRAL_API_KEY set: {mistral_key[:10]}...")
    print(f"✅ PINECONE_API_KEY set: {pinecone_key[:10]}...")
    print()
    
    return True

def test_heartbeat_system():
    """Test the complete HeartBeat Engine system"""
    
    try:
        # Import HeartBeat Engine
        script_dir = Path(__file__).parent
        sys.path.append(str(script_dir))
        
        from heartbeat_engine import HeartBeatEngine
        
        print("🔍 Testing HeartBeat Engine Components...")
        
        # Initialize engine
        engine = HeartBeatEngine()
        
        # Test query
        test_query = "Where do I rank among wingers with similar ice time?"
        result = engine.analyze_query(test_query, "player")
        
        # Validate results
        rag_working = result.get('context_used', 0) > 0
        data_working = result.get('data_points', 0) > 0
        model_working = 'error' not in result.get('response', '').lower()
        
        print(f"📊 Test Query: {test_query}")
        print(f"🤖 Response Preview: {result.get('response', '')[:100]}...")
        print()
        
        print("🔍 Component Status:")
        print(f"{'✅' if rag_working else '❌'} RAG System (Pinecone): {result.get('context_used', 0)} chunks retrieved")
        print(f"{'✅' if data_working else '❌'} Data System (Parquet): {result.get('data_points', 0)} metrics provided")  
        print(f"{'✅' if model_working else '❌'} AI Model (Mistral): Response generated successfully")
        print()
        
        if rag_working and data_working and model_working:
            print("🎉 HeartBeat Engine Status: FULLY OPERATIONAL")
            print("🚀 Ready for Montreal Canadiens hockey analytics!")
            return True
        else:
            print("⚠️  HeartBeat Engine Status: Partial functionality")
            print("🔧 Some components need attention")
            return False
            
    except Exception as e:
        print(f"❌ Error testing HeartBeat Engine: {e}")
        return False

def main():
    """Main setup function"""
    
    print("🏒 HeartBeat Engine - Complete System Setup")
    print("=" * 60)
    
    # Setup environment
    setup_success = setup_environment()
    
    if setup_success:
        print("🔧 Environment configured successfully!")
        print()
        
        # Test system
        system_success = test_heartbeat_system()
        
        if system_success:
            print()
            print("=" * 60) 
            print("🎯 SETUP COMPLETE!")
            print("✅ API keys configured")
            print("✅ All systems operational")
            print("✅ Ready for hockey analytics")
            print()
            print("🚀 To use HeartBeat Engine:")
            print("   from scripts.heartbeat_engine import HeartBeatEngine")
            print("   engine = HeartBeatEngine()")
            print("   result = engine.analyze_query('Your hockey question', 'coach')")
            print("=" * 60)
        else:
            print("❌ System test failed - check component status above")
    else:
        print("❌ Environment setup failed")

if __name__ == "__main__":
    main()
