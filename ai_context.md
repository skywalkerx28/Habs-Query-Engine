# AI Context: HabsAI Query Engine Development Guide

## Project Mission
**HeartBeat Engine** is an AI-powered analytics platform tailored exclusively for the Montreal Canadiens. At its core, it's a semantic search and analysis "AI index" that transforms Montreal Canadiens NHL play-by-play data and archived game footage (millions of events total) into an intelligent, conversational knowledge base.

Coaches, players, scouts, analysts, and authorized personnel can ask natural-language questions (e.g., "Analyze the Habs power play efficiency against Toronto's last season" or "What's the impact of pairing Hutson with Dobson on xGF ?") and receive dynamic, data-grounded responses: aggregated stats, visualizations, trend breakdowns, and prescriptive recommendations.

## Core Development Philosophy

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

## Major Development Phases

### Phase 1: Data Preparation & Ingestion Pipeline (Week 1) - COMPLETED
**Goal**: Clean, unified, query-ready dataset with optimized storage formats
**Key Tasks**:
- [COMPLETED] Audit & concatenate CSVs for schema consistency (82 games + 32 matchups)
- [COMPLETED] Data cleaning, enrichment, and feature derivation
- [COMPLETED] Chunking for RAG (500-event summaries, JSON formatted)
- [COMPLETED] Initial SQLite/Parquet database setup (90% compression, 10x faster queries)
**Efficiency Focus**: Vectorized pandas operations, chunked processing, compressed storage

### Phase 2: Vectorization & Retrieval System (Weeks 1-2) - IN PROGRESS
**Goal**: Enable semantic search over hockey events with multi-tier retrieval
**Key Tasks**:
- [IN PROGRESS] Embedding generation for semantic search (Sentence-BERT optimization)
- [IN PROGRESS] FAISS vector database implementation (HNSW indexing)
- [IN PROGRESS] Hybrid search (semantic + keyword filtering)
- [IN PROGRESS] MTL-specific embedding fine-tuning (Habs terminology)
**Efficiency Focus**: Batch processing, memory-efficient embeddings, sub-second retrieval

### Phase 3: LangGraph Orchestrator & Analysis Engine (Weeks 2-3) - IN PROGRESS
**Goal**: Implement a production-ready LangGraph agent orchestrator with fine-tuned Llama-3.3-70B-Instruct core, enabling sophisticated hockey analytics through intelligent tool orchestration, identity-aware data access, and enterprise-grade performance.

#### Architecture Decision: LangGraph Orchestrator
**Primary Framework**: LangGraph-based agent system with AWS SageMaker-trained models
**Reasoning**: Maximum flexibility for complex routing, stateful workflows, identity management, and hybrid data integration while leveraging enterprise-grade ML infrastructure for model training and deployment.

#### Core Implementation Objectives:
- **LangGraph Agent Core**: Fine-tuned `Llama-3.3-70B-Instruct` trained on AWS SageMaker as central reasoning engine
- **Node-based Orchestration**: Intent → Router → Vector Search → Parquet SQL → Analytics Tools → Visualization → Synthesis
- **Identity-Aware Processing**: User role enforcement with data scoping and permission-based filtering
- **Enterprise Security**: Resource guards, caching, timeout handling, and audit trails
- **Hybrid Data Intelligence**: Seamless RAG + live analytics with intelligent routing decisions

#### Critical Architecture Principles:
1. **Tool Orchestration**: LangGraph manages complex multi-step workflows with deterministic routing and error handling
2. **Identity Integration**: Every query scoped by `resolve_current_user` with role-based data access enforcement  
3. **Performance Optimization**: Intelligent caching, resource limits, and sub-3s p95 latency targets
4. **Evidence-Based Responses**: All insights backed by cited sources from RAG chunks or live query results

#### Technical Implementation Strategy:

##### 3.1 LangGraph Node Orchestration System
```
LangGraph Processing Flow:
User Query → Intent Node → Router Node → Tool Execution → Synthesis Node → Response
     ↓             ↓            ↓              ↓               ↓
Identity Check  Classify &   RAG/Parquet   Analytics &    Evidence-based
& Permissions  Extract Params  Selection   Visualization   Response Gen
```

**LangGraph Node Architecture:**
- **Intent Node**: Query classification, parameter extraction, and user identity resolution
- **Router Node**: Intelligent routing between RAG chunks, Parquet queries, or hybrid approaches
- **Vector Search Node**: Semantic retrieval from hockey knowledge chunks with metadata filtering
- **Parquet SQL Node**: Real-time analytics queries with user-scoped data access
- **Analytics Tools Node**: xG calculations, zone entry/exit stats, matchup comparisons
- **Visualization Node**: Dynamic heatmap and chart generation based on query results
- **Synthesis Node**: Context-aware response generation with source attribution

**Enterprise Features:**
- **Identity Management**: `resolve_current_user` with role-based data filtering
- **Resource Guards**: Row/byte limits, query timeouts, retry logic, intelligent caching
- **Security Layer**: Permission enforcement at each node with audit trail logging
- **Performance Optimization**: Parallel tool execution where possible, result caching

##### 3.2 RAG Chain Architecture
```
RAG Pipeline:
Query Processing → Retrieval (FAISS/Chroma) → Context Enhancement → Generation (Fine-tuned LLM)
     ↓                    ↓                           ↓                        ↓
Tokenization +       Semantic search +           Multi-source synthesis +   Prompt engineering +
Embedding           Hybrid filtering             Fact checking             Structured output
```

**Vector Database Implementation:**
- **Embedding Model**: Sentence-BERT optimized for sports analytics domain
- **Index Strategy**: HNSW (Hierarchical Navigable Small World) for sub-second retrieval
- **Hybrid Search**: Combines semantic similarity with keyword-based filtering
- **Metadata Filtering**: Game date, opponent, player, situation-specific retrieval

##### 3.3 Dynamic Analysis Tool Ecosystem for LLM
**Key Tasks**:
- Design MTL-specific prompts and system messages (Canadiens terminology)
- Implement hybrid RAG + tool chains with LangChain (context + live data integration)
- Create dynamic analysis tools enabling LLM to process any query combination
- Build real-time calculation capabilities (Corsi, zone entries, advanced metrics)

**LLM Tool Arsenal:**
```python
class HabsAnalysisTools:
    def query_team_stats(self, filters: dict, metrics: list):
        """Real-time team statistics with contextual explanations"""
        # Dynamic filtering: opponent, period, situation, date range
        
    def analyze_player_performance(self, player: str, context: dict):
        """Multi-dimensional player analysis with live calculations"""
        # Zone performance, line combinations, situational effectiveness
        
    def compare_scenarios(self, scenario_a: dict, scenario_b: dict):
        """Dynamic comparative analysis across any dimensions"""
        # Team vs team, player vs player, situation vs situation
        
    def calculate_advanced_metrics(self, data_source: str, metric_type: str):
        """On-demand calculation of complex hockey analytics"""
        # Corsi, expected goals, possession metrics, zone analysis
```

**Dynamic Tool Categories:**
- **Query Tools**: Real-time parquet data filtering and aggregation with hockey context
- **Analytics Tools**: Advanced metric calculation (Corsi, xG, zone analysis, possession)
- **Comparison Tools**: Multi-dimensional performance analysis and benchmarking
- **Visualization Tools**: Dynamic chart and heatmap generation from live query results
- **Context Tools**: Integrate RAG hockey knowledge with real-time data calculations

**CRITICAL REQUIREMENT**: LLM must be equipped with tools to answer ANY query combination dynamically, not limited to pre-computed static responses

##### 3.3.1 Tool Architecture Implementation
**Real-World Query Examples Requiring Dynamic Tools:**
- *"Montreal's shot blocking vs Toronto in 3rd periods this season"* → Requires filtering + context
- *"Compare Hutson's zone exits when paired with different defensemen"* → Requires joins + calculations  
- *"Show power play efficiency trends over last 10 games"* → Requires temporal analysis + visualization
- *"How does Montreal's penalty kill perform against teams with >25% power play?"* → Requires cross-dataset analysis

**Tool Implementation Strategy:**
```python
class HabsQueryEngine:
    def __init__(self):
        self.rag_chunks = load_contextual_chunks()  # Hockey knowledge
        self.parquet_tools = ParquetQueryTools()    # Live data access
        self.hockey_context = HockeyContextProvider()  # Domain expertise
        
    def process_query(self, query: str):
        # 1. Get hockey context from RAG
        context = self.rag_chunks.retrieve(query)
        
        # 2. Determine required tools
        tools_needed = self.analyze_query_requirements(query)
        
        # 3. Execute with tools + context
        return self.llm.generate(
            query=query,
            context=context,
            tools=tools_needed  # Real-time calculation capabilities
        )
```

##### 3.4 Structured Output Generation
**Key Tasks**:
- **Dynamic Visualization Engine**: Interactive shot heatmaps, performance charts, statistical tables
- **Response Formatting Pipeline**: Context-aware templates, data-to-narrative conversion
- **Source Attribution**: Clear indication of data sources and calculation methods

##### 3.5 Fine-Tuning & Optimization
**Domain-Specific Training:**
- **Custom Dataset**: 2,198 QA pairs focused on hockey analytics terminology
- **Montreal Context**: Fine-tuning on Canadiens-specific language and references
- **Statistical Literacy**: Training on proper interpretation of advanced metrics
- **Conversational Flow**: Optimization for multi-turn analytical conversations
- **SageMaker Infrastructure**: Enterprise-grade model training on AWS platform with Llama-3.3-70B-Instruct

**Performance Optimization:**
- **Query Caching**: Intelligent caching of frequent queries and calculations
- **Batch Processing**: Optimized batch operations for complex multi-game analysis
- **Memory Management**: Efficient handling of large datasets during analysis
- **Response Time Targets**: <2 seconds for basic queries, <5 seconds for complex analysis

##### 3.6 Testing & Validation Framework
**Automated Testing Suite:**
- **Unit Tests**: Individual component functionality (retrieval accuracy, calculation precision)
- **Integration Tests**: End-to-end query processing and response generation
- **Performance Benchmarks**: Query response times, retrieval accuracy metrics

**Human Evaluation Protocol:**
- **Expert Review**: Validation by hockey analysts and coaches
- **User Testing**: Real-world query testing with target user groups

#### Success Metrics:
- **Query Accuracy**: >90% statistically correct responses
- **Response Time**: <3 seconds average for complex queries
- **User Satisfaction**: >4.5/5 rating on response quality and relevance
- **Retrieval Precision**: >85% relevant information retrieval
- **Contextual Understanding**: >80% accurate interpretation of analytical intent

**Efficiency Focus**: Lightweight models, cached responses, minimal API calls, intelligent data routing

### Phase 4: UI & Deployment (Weeks 3-4) - PLANNED
**Goal**: Intuitive chat-based analytics platform with professional deployment
**Key Tasks**:
- [PLANNED] Streamlit chat interface with real-time query processing
- [PLANNED] Visualization integration (interactive rink plots, heatmaps, performance charts)
- [PLANNED] Query history, export features, and user session management
- [PLANNED] Docker containerization and Hugging Face Spaces deployment
**Efficiency Focus**: Fast loading, responsive design, minimal dependencies, offline-capable

### Phase 5: Testing & Launch (Weeks 4-6) - PLANNED
**Goal**: Production-ready, high-performance system with validated quality
**Key Tasks**:
- [PLANNED] Comprehensive testing suite (unit, integration, performance)
- [PLANNED] User testing and iteration with target user groups (coaches, analysts)
- [PLANNED] Performance optimization and security hardening
- [PLANNED] MVP launch preparation and documentation completion
**Efficiency Focus**: Benchmark everything, optimize bottlenecks, ensure reliability

## Code Development Guidelines

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

## Query Types to Support

### Basic Analytics
- Player performance: "How did Suzuki perform vs Toronto?"
- Team stats: "Habs power play efficiency this season"
- Game analysis: "What happened in the 3rd period vs Boston?"

### Advanced Analysis
- Comparative: "Compare youth pairings effectiveness"
- Trend analysis: "Zone exit success by lineup combination"
- Predictive: "Which matchups create best scoring chances?"

### Visual Analysis
- Spatial: "Shot heatmap for Caufield vs eastern conference"
- Temporal: "Scoring opportunities by period"
- Network: "Player passing connections in OZ"

## Data Schema Understanding

### **Multi-Tier Data Architecture**

#### **Primary Analytics Layer (Parquet)**
**Location**: `/data/processed/analytics/`
**Format**: Compressed Parquet files (90% smaller than CSV)
**Use Case**: High-performance analytics and complex queries

**Core Fields in Play-by-Play Data (315K+ events):**
- `gameReferenceId`: Unique game identifier
- `id`: Sequential event ID within game
- `period`: Game period (1, 2, 3, OT)
- `periodTime`: Time elapsed in period
- `gameTime`: Total game time elapsed
- `xCoord`, `yCoord`: Spatial coordinates on rink
- `xAdjCoord`, `yAdjCoord`: Adjusted coordinates for rink orientation
- `type`: Event type (shot, pass, faceoff, etc.)
- `playerReferenceId`: Player identifier
- `playerJersey`: Jersey number
- `playerPosition`: Player position (C, LW, RW, D, G)
- `team`: Team abbreviation
- `expectedGoalsOnNet`: xG value for shots
- `game_id`: Processed game identifier
- `source_file`: Original CSV filename for traceability

#### **LLM Context Layer (JSON)**
**Location**: `/data/processed/llm_model/`
**Format**: Structured JSON for LLM consumption
**Use Case**: Fast retrieval and contextual responses

**Available JSON Files:**
- `rag_chunks_2024_2025.json`: 1,152 text chunks for semantic search
- `qa_pairs_2024_2025.json`: 2,528 Q&A pairs for fine-tuning
- `matchup_analysis_2024_2025.json`: Statistical matchup data
- `game_summaries_2024_2025.json`: Narrative game summaries

#### **Backup Layer (CSV)**
**Location**: `/data/processed/backups/`
**Format**: Original CSV files for compatibility
**Use Case**: Data recovery and legacy system integration

### **Derived Features (Automatically Generated)**
- `shot_distance`: Distance from center (sqrt(x² + y²))
- `shot_angle`: Angle from goal in degrees
- `possession_duration`: Time between consecutive events
- `is_habs_event`: Boolean flag for Canadiens actions
- `zone`: Offensive/Defensive/Neutral zone classification
- `playZone`: Specific rink zone (center, left, right, etc.)
- `playSection`: Detailed zone section for advanced analysis

## Technical Constraints & Optimizations

### Memory Management (ACHIEVED)
- Process large CSVs in chunks (automated ETL pipeline)
- Use Parquet format for 90% compressed storage
- Implement data type optimization and memory-efficient processing
- Clear memory after processing large datasets
- Handle 315K+ events efficiently without memory errors

### Performance Targets (CURRENT STATUS)
- Data loading: <60 seconds for all CSV files (achieved in ~30 seconds)
- Query response: <3 seconds for complex analysis (Parquet enables this)
- Embedding generation: <15 minutes for full dataset (Phase 2 target)
- Memory usage: <8GB during processing (achieved with chunked processing)
- 10x query performance improvement over CSV

### Scalability Considerations (IMPLEMENTED)
- Enterprise-grade data architecture with multi-tier storage
- Season-based file naming for easy expansion
- Modular architecture supporting cloud migration
- Intelligent caching strategy for LLM responses
- Lazy loading capabilities for large datasets
- Support for both CSV and archived game footage integration
- Real-time data ingestion pipeline ready for NHL API

### Current Performance Metrics
- **Storage Efficiency**: 90% compression (143MB → 14MB)
- **Query Performance**: 10x faster than CSV baseline
- **Data Integrity**: Zero data loss during ETL processing
- **Scalability**: Supports multiple seasons with consistent naming
- **Backup Reliability**: Automated CSV backups for data safety

## Success Metrics

### Technical KPIs
- [COMPLETED] Data processing completes without memory errors (315K+ events processed)
- [COMPLETED] Enterprise-grade data architecture (Parquet + JSON multi-tier system)
- [COMPLETED] 90% storage compression with 10x query performance gains
- [COMPLETED] Optimized ETL pipeline with automated quality validation
- [TARGET] Query accuracy >90% statistically correct responses
- [TARGET] Response time <3 seconds average for complex queries (<5s max)
- [TARGET] Memory usage stays under 8GB during processing

### User Experience KPIs
- [TARGET] Handles natural language queries without predefined templates
- [TARGET] Provides actionable insights combining historical patterns and recommendations
- [TARGET] Generates dynamic visualizations and statistical outputs automatically
- [TARGET] User satisfaction >4.5/5 rating on response quality and relevance
- [TARGET] Retrieval precision >85% relevant information retrieval
- [TARGET] Contextual understanding >80% accurate interpretation of analytical intent
- [COMPLETED] Scales to handle full season analysis (82 games processed)

### Code Quality KPIs
- [TARGET] All functions have type hints and docstrings
- [TARGET] Unit test coverage >80% for core functionality
- [TARGET] Code follows PEP 8 standards with automated linting
- [TARGET] Performance profiled and optimized for production deployment
- [COMPLETED] Modular architecture with clear separation of concerns

## Deployment Strategy

### MVP Deployment (Phase 4)
- Local Streamlit app for initial testing with real-time query processing
- Hugging Face Spaces for easy sharing and collaboration
- Docker containerization for reproducibility and deployment consistency
- Offline-first design for data security and Montreal-specific requirements

### Production Considerations
- Cloud migration path (AWS/GCP/Azure) with Canadian data residency
- Database optimization for concurrent users (coaches, analysts, players)
- API rate limiting and intelligent caching for performance
- Monitoring, logging, and analytics infrastructure
- Security hardening for sensitive team data
- Scalable architecture supporting multiple seasons and real-time updates

## Collaboration Guidelines

### For AI Assistants
- Always prioritize efficiency and simplicity in implementation
- Ask for clarification rather than making assumptions about requirements
- Focus on delivering working, well-tested code rather than perfect code
- Document design decisions and trade-offs clearly in comments
- Test thoroughly and validate against real Montreal Canadiens data
- Maintain consistency with established patterns and architecture

### For Human Developers
- Review code for performance bottlenecks and optimization opportunities
- Ensure all features meet Montreal Canadiens-specific requirements
- Test with real Habs data scenarios and edge cases
- Focus on authorized personnel access and data security requirements
- Document any deviations from this guide with justification
- Validate that new features integrate properly with existing ETL pipeline

---

## **CURRENT PROJECT STATUS SUMMARY**

### **PHASE 1: COMPLETED (Data Foundation)**
- **82 NHL games processed** (315K+ events, 31 matchups)
- **Enterprise data architecture** (Parquet + JSON multi-tier system)
- **90% storage compression** with 10x query performance gains
- **Automated ETL pipeline** with quality validation
- **Scalable directory structure** ready for multiple seasons

### **PHASE 2: IN PROGRESS (Vector Search System)**
- **Infrastructure ready** for Sentence-BERT embeddings
- **FAISS vector database** implementation planned
- **Hybrid search architecture** designed for semantic + keyword
- **MTL-specific terminology** optimization prepared

### **PHASE 3: IN PROGRESS (Hybrid RAG + Tool Integration)**
- **Hybrid RAG architecture** implemented with contextual chunks + real-time tools
- **Dataset documentation integration** completed (71 contextual JSON files)
- **Enhanced RAG chunks** created with hockey domain knowledge
- **Dynamic tool framework** designed for LLM analytical capabilities
- **Performance targets** defined (<3s response time, >90% accuracy)
- **Fine-tuning datasets** prepared (2,528 QA pairs)

### **KEY ACHIEVEMENTS**
- **World-class data foundation** with industry-standard practices
- **Performance optimization** exceeding initial targets
- **Scalable architecture** supporting enterprise growth
- **Montreal Canadiens focus** with domain-specific optimizations
- **Production-ready ETL** with comprehensive error handling

---

**Remember**: This is a **world-class foundation** for a professional AI analytics platform. Our methodical approach ensures sustainable long-term success with enterprise-grade reliability and performance. The architecture we've built will support advanced AI capabilities for years to come!
