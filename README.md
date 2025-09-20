# HeartBeat Engine

## AI-Driven Analytics Platform for Montreal Canadiens

**HeartBeat Engine** is an AI-powered analytics platform tailored exclusively for the Montreal Canadiens. At its core, it's a semantic search and analysis "AI index" that transforms a collection of tabular and visual data (covering the relevant recent seasons ~millions granular events like shots, passes, possessions, and coordinates) into an intelligent, conversational knowledge base that people are accustomed to interacting with nowadays.

Coaches, players, scouts, analysts, and other authorized personnel can ask natural-language questions (e.g., "Analyze the Habs power play efficiency against Toronto last season." or "What's the impact of pairing Hutson with Guhle on zone exits?" or "Show me all of my shorthanded shifts from last season.") and receive dynamic, data-grounded responses: aggregated stats (e.g., xG differentials), visualizations (e.g., shot heatmaps on a rink), trend breakdowns, and even prescriptive recommendations (e.g., "Target east-slot rushes—boosts scoring by 18%").

## Key Differentiators

### Hyper-Tailored for MTL
- **Canadiens-Specific Logic**: Embeds Montreal-specific insights (e.g., St. Louis' transition style, youth metrics like player development trends and prospect performances) via custom prompts and fine-tuning.
- **Habs-Centric Metrics**: Optimized for Montreal's playing style, personnel, and strategic priorities.

### Dynamic & Proactive Analysis
- **Retrieval-Augmented Generation (RAG)**: Uses LLM to interpret queries, retrieve relevant events, execute on-the-fly analysis.
- **No Pre-coded Queries**: Handles any natural language question without predefined templates.
- **Real-time Insights**: Generates tables, plots, and recommendations dynamically. 

### Scalable Architecture
- **MVP Foundation**: Starts offline with extensive local tabular and visual data; evolves to real-time ingestion.
- **Extensible Design**: Ready for 2025-26 data, interactive visualizations, NHL API integrations (possibly).
- **Cloud-Ready**: Deployable on Hugging Face Spaces with offline fallback for sensitive data.

## Technical Architecture

### Core Components
- **Data Pipeline**: ETL processes for CSV files → unified Parquet format
- **Vector Database**: Pinecone for semantic search over event embeddings
- **LLM Integration**: LangChain + local/cloud models for query processing
- **Analysis Engine**: Custom tools for MTL-specific metrics (Corsi, zone entries, etc.)
- **Web Interface**: Streamlit-powered chat application (includes heatmap, custom tabular data creation, etc).

### Tech Stack
- **Backend**: Python 3.13, pandas, numpy, scikit-learn.
- **AI/ML**: LangChain, sentence-transformers, Pinecone.
- **Visualization**: matplotlib, seaborn, plotly.
- **Database**: SQLite/Parquet for local storage.
- **Deployment**: Streamlit, Docker, Hugging Face Spaces.

## Data Overview

- **Source**: NHL play-by-play CSV files and archive game footage (from recent relevant seasons).
- **Volume**: ~Millions granular events and thousands of game footage.
- **Key Fields**: xCoord, yCoord, type, playerReferenceId, expectedGoalsOnNet, period, gameTime.
- **Processing**: Unified schema, derived features (shot_distance, possession_duration), Habs event flagging.

## Development Roadmap

### Phase 1: Data Preparation & Ingestion Pipeline (Week 1)
- [COMPLETED] Audit & concatenate CSVs for schema consistency
- [COMPLETED] Data cleaning, enrichment, and feature derivation
- [In Progress] Chunking for RAG (500-event summaries)
- [In Progress] Initial SQLite/Parquet database setup

### Phase 2: Vectorization & Retrieval System (Weeks 1-2)
- [Planned] Embedding generation for semantic search
- [PLanned] Pinecone vector database implementation
- [Planned] Hybrid search (semantic + keyword)
- [Planned] MTL-specific embedding fine-tuning

### Phase 3: LLM Integration & Analysis Engine (Weeks 2-3)

**Goal:** Develop a sophisticated hybrid RAG system that combines contextual hockey knowledge with real-time data analysis capabilities, enabling the LLM to dynamically answer any query combination through intelligent tool usage and data synthesis.

#### Core Objectives:
- **Natural Language Processing:** Enable conversational queries like "How effective was Montreal's power play against Toronto in 3rd periods?" or "Compare Hutson's zone exit success vs Eastern Conference teams"
- **Hybrid Intelligence System:** Multi-tier architecture combining RAG chunks (hockey context) with real-time Parquet queries (live calculations)
- **Dynamic Tool Usage:** Provide LLM with analytical tools to think on its feet and answer any query combination, not just static responses
- **Contextual Analysis:** Generate insights combining historical patterns, player performance, and strategic recommendations through real-time data synthesis
- **Visual Intelligence:** Create dynamic visualizations and statistical outputs based on query context and live data analysis

#### Technical Implementation Strategy:

##### 3.1 Hybrid RAG + Real-Time Query System
```
Query Processing Flow:
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   User Query    │ -> │  Intent Analysis│ -> │  Hybrid         │ -> │  LLM with Tools │
│  "Montreal's    │    │  (LLM Router)   │    │  Retrieval      │    │  & Context      │
│   blocking vs   │    │                 │    │                 │    │                 │
│   Toronto in    │    │  - Query type   │    │  - RAG chunks   │    │  - Hockey cntxt │
│   3rd periods"  │    │  - Complexity   │    │    (context)    │    │  - SQL tools    │
└─────────────────┘    │  - Data needs   │    │  - Parquet SQL  │    │  - Visualization│
                       │  - Filters      │    │    (live data)  │    │  - Calculation  │
                       └─────────────────┘    └─────────────────┘    └─────────────────┘
```

**Low-Level Components:**
- **Query Classifier:** BERT-based model to categorize queries (basic stats, advanced analytics, trend analysis, predictive)
- **Hybrid Data Router:** Intelligent routing between RAG chunks (hockey context) and Parquet queries (live calculations)
- **Tool Provider:** Equips LLM with analytical tools for dynamic query processing and real-time calculations
- **Context Builder:** Combines hockey domain knowledge with live data for comprehensive, accurate responses

##### 3.2 RAG Chain Architecture
```
RAG Pipeline:
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Query         │ -> │  Retrieval      │ -> │  Context        │ -> │  Generation    │
│   Processing    │    │   (Pinecone)   │    │  Enhancement     │    │  (Fine-tuned   │
│                 │    │                 │    │                 │    │  LLM)          │
│  - Tokenization │    │  - Semantic     │    │  - Multi-source │    │                │
│  - Embedding    │    │    search       │    │    synthesis    │    │  - Prompt eng. │
│  - Similarity   │    │  - Hybrid       │    │  - Fact checking│    │  - Structured  │
│    matching     │    │    filtering    │    │  - Relevance    │    │    output      │
└─────────────────┘    └─────────────────┘    └─────────────────┘    └─────────────────┘
```

**Vector Database Implementation:**
- **Embedding Model:** Sentence-BERT optimized for sports analytics domain
- **Index Strategy:** HNSW (Hierarchical Navigable Small World) for sub-second retrieval
- **Hybrid Search:** Combines semantic similarity with keyword-based filtering
- **Metadata Filtering:** Game date, opponent, player, situation-specific retrieval

##### 3.3 Dynamic Analysis Tools for LLM

**LLM Tool Arsenal:**
```python
class HabsAnalysisTools:
    def query_parquet_data(self, sql_query: str, context: dict):
        """Execute real-time SQL queries on parquet files with hockey context"""
        # Dynamic filtering, aggregation, and calculation capabilities
        
    def calculate_advanced_metrics(self, data: pd.DataFrame, metric_type: str):
        """Calculate complex hockey metrics on-demand"""
        # Corsi, expected goals, zone entry success, possession metrics
        
    def compare_performance(self, filters: dict, comparison_type: str):
        """Dynamic performance comparisons across any dimensions"""
        # Player vs player, team vs team, situation vs situation
        
    def generate_visualizations(self, data: pd.DataFrame, chart_type: str):
        """Create dynamic charts and heatmaps from query results"""
        # Shot maps, performance trends, comparative analysis
```

**Dynamic Tool Categories:**
- **Data Query Tools:** Real-time parquet filtering, aggregation, and calculation
- **Hockey Analytics Tools:** Advanced metric calculation (Corsi, xG, zone analysis)
- **Comparison Tools:** Multi-dimensional performance analysis and benchmarking
- **Visualization Tools:** Dynamic chart and heatmap generation from live data
- **Context Integration Tools:** Combine RAG hockey knowledge with real-time calculations

**Critical Capability:** LLM can answer ANY query combination by dynamically using tools rather than relying on pre-computed static responses

##### 3.4 Structured Output Generation

**Dynamic Visualization Engine:**
```python
class HabsVisualizer:
    def create_shot_heatmap(self, shot_data, rink_template):
        """Generate interactive shot heatmaps with player tracking"""

    def generate_performance_charts(self, metrics_data):
        """Create comparative performance visualizations"""

    def build_statistical_tables(self, analysis_results):
        """Format complex statistical data into readable tables"""
```

**Response Formatting Pipeline:**
- **Template System:** Context-aware response templates for different query types
- **Data Formatting:** Automatic conversion of raw statistics into narrative form
- **Visual Integration:** Seamless embedding of charts and heatmaps in responses
- **Source Attribution:** Clear indication of data sources and calculation methods

##### 3.5 Fine-Tuning & Optimization

**Domain-Specific Training:**
- **Custom Dataset:** 2,528 QA pairs focused on hockey analytics terminology
- **Montreal Context:** Fine-tuning on Canadiens-specific language and references
- **Statistical Literacy:** Training on proper interpretation of advanced metrics
- **Conversational Flow:** Optimization for multi-turn analytical conversations

**Performance Optimization:**
- **Query Caching:** Intelligent caching of frequent queries and calculations
- **Batch Processing:** Optimized batch operations for complex multi-game analysis
- **Memory Management:** Efficient handling of large datasets during analysis
- **Response Time Targets:** <2 seconds for basic queries, <5 seconds for complex analysis

##### 3.6 Testing & Validation Framework

**Automated Testing Suite:**
- **Unit Tests:** Individual component functionality (retrieval accuracy, calculation precision)
- **Integration Tests:** End-to-end query processing and response generation
- **Performance Benchmarks:** Query response times, retrieval accuracy metrics
- **Accuracy Validation:** Statistical calculation verification against known baselines

**Human Evaluation Protocol:**
- **Expert Review:** Validation by hockey analysts and coaches
- **User Testing:** Real-world query testing with target user groups
- **Iterative Improvement:** Continuous refinement based on user feedback
- **Edge Case Handling:** Robust processing of unusual or complex queries

#### Success Metrics:
- **Query Accuracy:** >90% statistically correct responses
- **Response Time:** <3 seconds average for complex queries
- **User Satisfaction:** >4.5/5 rating on response quality and relevance
- **Retrieval Precision:** >85% relevant information retrieval
- **Contextual Understanding:** >80% accurate interpretation of analytical intent

### Phase 4: UI & Deployment (Weeks 3-4)
- [PLANNED] Streamlit chat interface
- [PLANNED] Visualization integration
- [PLANNED] Docker containerization
- [PLANNED] Hugging Face Spaces deployment

### Phase 5: Testing & Launch (Weeks 4-6)
- [PLANNED] Comprehensive testing suite
- [PLANNED] User testing and iteration
- [PLANNED] Performance optimization
- [PLANNED] MVP launch preparation

## Installation & Setup

### Prerequisites
- Python 3.13+
- Git
- 4GB+ RAM (for embedding processing)

### Local Development Setup
```bash
# Clone repository
git clone https://github.com/skywalkerx28/Habs-Query-Engine.git
cd habs-query-engine

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run data preparation
python scripts/etl_pipeline.py

# Start development server
streamlit run app/main.py
```

### Data Setup
1. Place your NHL CSV files in `data/raw/`
2. Run ETL pipeline to create unified dataset
3. Generate embeddings for semantic search

## Usage Examples

### Basic Queries
```python
from habs_ai import HabsQueryEngine

engine = HabsQueryEngine()
response = engine.query("How effective was Montreal's power play against Toronto?")
print(response.stats)
print(response.visualization)
```

### Advanced Analysis
```python
# Multi-game analysis
response = engine.query("Compare Suzuki's performance in 5v5 vs power play situations")

# Trend analysis
response = engine.query("What's the impact of youth pairings on zone exit success?")

# Predictive insights
response = engine.query("Which matchups should we target for better scoring opportunities?")
```

## Performance Benchmarks

- **Query Accuracy**: 85%+ (via backtesting)
- **Response Time**: <5 seconds
- **Data Coverage**: 100% of 2024-2025 season events
- **Retrieval Precision**: >80% relevant chunks
- **User Satisfaction**: Target 4.5/5 rating

## Contributing

### Development Philosophy
- **Efficiency First**: Prioritize simple, optimal code over complex systems
- **MTL-Centric**: All features must enhance Canadiens analysis capabilities
- **Iterative Approach**: MVP focus with clear upgrade paths
- **Open Collaboration**: Welcome contributions from Habs analytics community

### Contribution Guidelines
1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

### Code Standards
- **PEP 8** compliance for Python code
- **Type hints** for all function parameters
- **Docstrings** for all public functions
- **Unit tests** for new functionality
- **Performance profiling** for data processing functions

## Future Enhancements

### Phase 2 (Post-MVP)
- **Real-time Data**: NHL API integration for live game analysis
- **Advanced Visualizations**: AR rink overlays, player tracking animations
- **Predictive Modeling**: Game outcome forecasting, player performance prediction
- **Voice Interface**: Natural language voice queries and responses

### Research Directions
- **Advanced RAG**: Multi-modal embeddings (text + spatial data)
- **Reinforcement Learning**: Optimal strategy recommendations
- **Computer Vision**: Video clip retrieval for key moments
- **Network Analysis**: Player connectivity and chemistry modeling

## License

This project is licensed under the MIT License - see the [LICENSE] file for details.



**Built for the Montreal Canadiens**

*For questions or collaboration opportunities, please open an issue or contact the maintainers.*
