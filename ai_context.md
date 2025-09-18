# AI Context: HabsAI Query Engine Development Guide

## 🎯 Project Mission
You are developing **HabsAI Query Engine**, an AI-powered analytics platform specifically for Montreal Canadiens NHL data analysis. The goal is to create an intelligent, conversational knowledge base that transforms 82 play-by-play CSV files (~300,000 events) into actionable insights through natural language queries.

## 🔧 Core Development Philosophy

### **EFFICIENCY & SIMPLICITY FIRST**
- **Prioritize simple, optimal code over complex systems**
- **Avoid over-engineering** - solve problems with the minimal viable solution
- **Performance matters** - optimize for speed and memory usage
- **Maintainable code** - clear, readable, well-documented
- **Iterative development** - build MVP first, then enhance

### **MTL-Centric Focus**
- All features must enhance Canadiens analysis capabilities
- Embed Montreal-specific logic and metrics
- Optimize for Habs playing style and personnel
- Consider coach preferences and team priorities

## 📋 Major Development Phases

### Phase 1: Data Foundation (COMPLETED ✅)
**Goal**: Clean, unified, query-ready dataset
**Key Tasks**:
- ✅ Concatenate 82 CSVs into single Parquet file
- ✅ Handle schema inconsistencies and missing data
- ✅ Derive useful features (shot_distance, possession_duration)
- ✅ Create SQLite/Parquet database for fast queries
**Efficiency Focus**: Use pandas vectorized operations, avoid loops

### Phase 2: Vector Search System (IN PROGRESS 🔄)
**Goal**: Enable semantic search over hockey events
**Key Tasks**:
- Generate embeddings for event descriptions
- Implement FAISS vector database
- Create hybrid search (semantic + keyword)
- Fine-tune embeddings for hockey terminology
**Efficiency Focus**: Batch processing, memory-efficient embeddings, fast retrieval

### Phase 3: LLM Integration (UPCOMING 📋)
**Goal**: Dynamic query interpretation and analysis
**Key Tasks**:
- Design MTL-specific prompts and system messages
- Implement RAG chains with LangChain
- Create structured output formatting
- Build custom analysis tools (Corsi, zone analysis)
**Efficiency Focus**: Lightweight models, cached responses, minimal API calls

### Phase 4: User Interface (UPCOMING 🎨)
**Goal**: Intuitive chat-based analytics platform
**Key Tasks**:
- Build Streamlit web interface
- Integrate visualizations (rink plots, heatmaps)
- Add query history and export features
- Deploy to Hugging Face Spaces
**Efficiency Focus**: Fast loading, responsive design, minimal dependencies

### Phase 5: Testing & Optimization (UPCOMING 🧪)
**Goal**: Production-ready, high-performance system
**Key Tasks**:
- Comprehensive testing suite
- Performance profiling and optimization
- User testing and feedback integration
- Documentation and deployment prep
**Efficiency Focus**: Benchmark everything, optimize bottlenecks

## 💡 Code Development Guidelines

### **Performance Priorities**
1. **Data Processing**: Vectorized pandas operations over loops
2. **Memory Usage**: Process data in chunks, use appropriate data types
3. **Query Speed**: Optimize database queries, use indexing
4. **Model Inference**: Use efficient models, cache results
5. **File I/O**: Minimize disk reads, use compressed formats

### **Architecture Principles**
- **Modular Design**: Small, focused functions with single responsibilities
- **Configuration Management**: External config files for parameters
- **Error Handling**: Graceful failure with informative messages
- **Logging**: Comprehensive logging for debugging and monitoring
- **Testing**: Unit tests for all core functionality

### **Habs-Specific Considerations**
- **Player Mapping**: Efficient ID-to-name lookups
- **Game Context**: Include opponent, period, score differential
- **Team Logic**: Flag Habs events, calculate team-relative metrics
- **Strategic Insights**: Focus on transition, special teams, youth development

## 🔍 Query Types to Support

### **Basic Analytics**
- Player performance: "How did Suzuki perform vs Toronto?"
- Team stats: "Habs power play efficiency this season"
- Game analysis: "What happened in the 3rd period vs Boston?"

### **Advanced Analysis**
- Comparative: "Compare youth pairings effectiveness"
- Trend analysis: "Zone exit success by lineup combination"
- Predictive: "Which matchups create best scoring chances?"

### **Visual Analysis**
- Spatial: "Shot heatmap for Caufield vs eastern conference"
- Temporal: "Scoring opportunities by period"
- Network: "Player passing connections in OZ"

## 📊 Data Schema Understanding

### **Core Fields**
- `gameReferenceId`: Unique game identifier
- `id`: Sequential event ID within game
- `type`: Event type (shot, pass, regular, none, slot, south)
- `xCoord`, `yCoord`: Spatial coordinates on rink
- `playerReferenceId`: Player identifier (needs mapping to names)
- `expectedGoalsOnNet`: xG value for shots
- `period`: Game period (1, 2, 3, OT)
- `gameTime`: Time elapsed in period

### **Derived Features to Create**
- `shot_distance`: Distance from center (sqrt(x² + y²))
- `shot_angle`: Angle from goal
- `possession_duration`: Time between events
- `is_habs_event`: Boolean flag for Canadiens actions
- `zone`: Offensive/Defensive/Neutral zone classification

## 🛠️ Technical Constraints & Optimizations

### **Memory Management**
- Process large CSVs in chunks (5000 rows at a time)
- Use Parquet format for compressed storage
- Implement data type optimization (int32 vs int64)
- Clear memory after processing large datasets

### **Performance Targets**
- Data loading: <30 seconds for all 82 files
- Query response: <3 seconds for complex analysis
- Embedding generation: <10 minutes for full dataset
- Memory usage: <4GB during processing

### **Scalability Considerations**
- Start with local processing, design for cloud migration
- Implement caching for frequent queries
- Use lazy loading for large datasets
- Design modular architecture for easy extension

## 🎯 Success Metrics

### **Technical KPIs**
- ✅ Data processing completes without memory errors
- ✅ Query accuracy >85% on test set
- ✅ Response time <5 seconds for 95% of queries
- ✅ Memory usage stays under 4GB during processing

### **User Experience KPIs**
- ✅ Handles natural language queries without templates
- ✅ Provides actionable insights, not just raw stats
- ✅ Generates useful visualizations automatically
- ✅ Scales to handle full season analysis

### **Code Quality KPIs**
- ✅ All functions have type hints and docstrings
- ✅ Unit test coverage >80% for core functionality
- ✅ Code follows PEP 8 standards
- ✅ Performance profiled and optimized

## 🚀 Deployment Strategy

### **MVP Deployment**
- Local Streamlit app for initial testing
- Hugging Face Spaces for easy sharing
- Docker containerization for reproducibility
- Offline-first design for data security

### **Production Considerations**
- Cloud migration path (AWS/GCP)
- Database optimization for concurrent users
- API rate limiting and caching
- Monitoring and logging infrastructure

## 🤝 Collaboration Guidelines

### **For AI Assistants**
- Always prioritize efficiency and simplicity
- Ask for clarification rather than making assumptions
- Focus on delivering working code, not perfect code
- Document design decisions and trade-offs
- Test thoroughly before marking tasks complete

### **For Human Developers**
- Review code for performance bottlenecks
- Ensure MTL-specific requirements are met
- Test with real Habs data scenarios
- Document any deviations from this guide

---

**Remember**: This is a foundation for a much larger project. Focus on building a solid, efficient MVP that can scale. Efficiency and simplicity are your guiding principles - complex systems can come later if needed.
