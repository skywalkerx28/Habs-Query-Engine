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

### LangGraph Orchestrator Core
**Central Intelligence:** LangGraph-based agent orchestrator powered by fine-tuned `deepseek-ai/DeepSeek-R1-Distill-Qwen-32B`

**Processing Flow:**
```
User Query → Intent Classification → Router → Tools → Synthesis → Response
```

**Node Architecture:**
- **Intent Node**: Query classification and parameter extraction
- **Router Node**: Determines RAG vs Parquet vs hybrid data needs  
- **Vector Search**: Semantic retrieval from hockey knowledge chunks
- **Parquet SQL**: Real-time analytics queries on game/player data
- **Analytics Tools**: xG calculations, zone entry/exit stats, matchup comparisons
- **Visualization**: Dynamic heatmaps, charts, and statistical displays
- **Synthesis**: Context-aware response generation with evidence citation

### System Guards & Identity Management
- **User/Role Filters**: Identity-aware data scoping and permissions
- **Resource Guards**: Row/byte caps, query timeouts, retry logic
- **Caching Layer**: Intelligent caching for performance optimization
- **Security**: `resolve_current_user` with data access enforcement

### Hybrid Data Architecture
- **RAG System**: Hockey domain knowledge and contextual explanations
- **Live Analytics**: Real-time Parquet queries for current statistics
- **Tool Integration**: Seamless combination of historical and live data

### SageMaker Model Training & Deployment
- **Training Infrastructure**: AWS SageMaker for large-scale model fine-tuning
- **Model Registry**: Centralized model versioning and deployment management
- **Scalable Inference**: Auto-scaling endpoints for production workloads

### Tech Stack
- **Orchestration**: LangGraph agent workflows with custom node architecture
- **Core Model**: DeepSeek-R1-Distill-Qwen-32B (32.7B parameters, MIT licensed)
- **ML Platform**: AWS SageMaker for enterprise-grade training and inference
- **Vector Database**: Pinecone with hybrid semantic + keyword search
- **Analytics Backend**: Python 3.13, pandas, pyarrow for Parquet optimization
- **Video Processing**: FFmpeg integration for clip analysis and thumbnails
- **Visualization**: Dynamic matplotlib/seaborn charts with real-time generation
- **Frontend**: React + TypeScript interface with Tailwind CSS 
- **Backend**: FastAPI services with async processing capabilities
- **Security**: AWS IAM policies, Secrets Manager, and role-based access control
- **Infrastructure**: Terraform-ready AWS configurations and deployment scripts

## Data Overview

- **Source**: NHL play-by-play CSV files and archive game footage (from recent relevant seasons).
- **Volume**: ~Millions granular events and thousands of game footage.
- **Key Fields**: xCoord, yCoord, type, playerReferenceId, expectedGoalsOnNet, period, gameTime.
- **Processing**: Unified schema, derived features (shot_distance, possession_duration), Habs event flagging.

## Development Status

### Completed Infrastructure
- [x] **Model Migration**: Updated from Llama models to DeepSeek-R1-Distill-Qwen-32B
- [x] **AWS Integration**: SageMaker training infrastructure and endpoint management
- [x] **Project Reorganization**: Restructured codebase with proper separation of concerns
- [x] **Data Architecture**: Organized training assets and video clip storage
- [x] **Infrastructure Setup**: AWS policy files and deployment configurations

### Current Capabilities
- **LangGraph Orchestrator**: Agent-based workflow with intent analysis and routing
- **Hybrid Intelligence**: RAG + real-time Parquet SQL integration
- **Video Analytics**: Video clip retrieval and analysis capabilities
- **Multi-modal Interface**: React + TypeScript chat interface with analytics panels
- **Enterprise Security**: Role-based access control and data scoping

### Phase 3: Advanced LangGraph Orchestrator (In Progress)

**Goal:** Implement a sophisticated LangGraph-based agent orchestrator that seamlessly combines fine-tuned deepseek-ai/DeepSeek-R1-Distill-Qwen-32B with hybrid RAG + real-time analytics, enabling dynamic hockey analysis with enterprise-grade security and performance.

#### Architecture Implementation:
- **LangGraph Agent Core:** Fine-tuned `deepseek-ai/DeepSeek-R1-Distill-Qwen-32B` as central reasoning engine
- **Node-based Workflow:** Intent → Router → Vector Search → Parquet SQL → Analytics Tools → Visualization → Synthesis
- **Identity-Aware System:** User role enforcement with data scoping and permissions
- **Hybrid Intelligence:** RAG chunks for hockey context + live Parquet queries for current statistics
- **Tool Orchestration:** xG calculations, zone entry/exit analysis, matchup comparisons, dynamic visualizations

#### Core Objectives:
- **Conversational Analytics:** Enable complex queries like "How effective was Montreal's power play against Toronto in 3rd periods?" with multi-step tool usage
- **Smart Routing:** Intelligent decision-making between RAG knowledge, live data, or hybrid approaches based on query intent
- **Real-time Tool Integration:** Dynamic analytics capabilities with timeout handling, caching, and error recovery
- **Contextual Synthesis:** Evidence-based responses combining historical patterns with current performance data
- **Role-based Access:** User-specific data filtering and permission enforcement for coaches, players, analysts, and staff

#### Technical Implementation Strategy:

##### 3.1 Hybrid RAG + Real-Time Query System
```
Query Processing Flow:
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   User Query    │ -> │ Intent Analysis │ -> │  Hybrid         │ -> │  LLM with Tools │
│  "Montreal's    │    │  (LLM Router)   │    │  Retrieval      │    │  & Context      │
│   shots  vs     │    │                 │    │                 │    │                 │
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
│   Query         │ -> │  Retrieval      │ -> │  Context        │ -> │  Generation     │
│   Processing    │    │   (Pinecone)    │    │  Enhancement    │    │  (Fine-tuned    │
│                 │    │                 │    │                 │    │  LLM)           │
│  - Tokenization │    │  - Semantic     │    │  - Multi-source │    │                 │
│  - Embedding    │    │    search       │    │    synthesis    │    │  - Prompt eng.  │
│  - Similarity   │    │  - Hybrid       │    │  - Fact checking│    │  - Structured   │
│    matching     │    │    filtering    │    │  - Relevance    │    │    output       │
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
- **Custom Dataset:** 2,198 QA pairs focused on hockey analytics terminology
- **Montreal Context:** Fine-tuning on Canadiens-specific language and references
- **Statistical Literacy:** Training on proper interpretation of advanced metrics
- **Conversational Flow:** Optimization for multi-turn analytical conversations
- **SageMaker Training:** Enterprise-grade model training on AWS infrastructure

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

### Next Development Phases

#### Phase 4: Enhanced Analytics & Testing
- [ ] **Advanced Visualizations**: Interactive heatmaps and performance charts
- [ ] **Video Integration**: Seamless video clip embedding in responses
- [ ] **Performance Optimization**: Query caching and response time improvements
- [ ] **Comprehensive Testing**: Unit tests, integration tests, and user validation

#### Phase 5: Production Deployment
- [ ] **Containerization**: Docker deployment with optimized environments
- [ ] **Cloud Deployment**: AWS SageMaker endpoints and scalable infrastructure
- [ ] **Monitoring**: Performance metrics and error tracking
- [ ] **User Training**: Documentation and onboarding materials

## Installation & Setup

### Prerequisites
- Python 3.13+
- Git
- 8GB+ RAM (for ML model processing)
- AWS CLI configured (for SageMaker integration)

### Local Development Setup
```bash
# Clone repository
git clone https://github.com/skywalkerx28/HeartBeat.git
cd HeartBeat

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
export OPENAI_API_KEY="your-openai-key"  # For fallback model

# Run data preparation (if needed)
python scripts/etl_pipeline.py

# Start development servers
# Frontend (React/TypeScript)
cd frontend && npm run dev

# Backend (FastAPI)
cd backend && python main.py
```

### Project Structure
```
HeartBeat/
├── app/                          # Streamlit application (legacy)
├── backend/                      # FastAPI backend services
├── frontend/                     # Next.js React frontend
├── orchestrator/                 # LangGraph agent orchestration
├── data/                         # Data processing and storage
│   ├── processed/
│   │   └── llm_model/
│   │       └── training/         # ML training assets
│   └── clips/                    # Video clip storage
├── infrastructure/               # AWS infrastructure files
├── scripts/                      # Utility and deployment scripts
└── venv/                         # Virtual environment (gitignored)
```

### Data Setup
1. Place NHL CSV files in `data/raw/` (if available)
2. Configure AWS credentials for SageMaker access
3. Set up Pinecone vector database credentials
4. Initialize training data in `data/processed/llm_model/training/`

## Usage Examples

### Basic Queries
```python
from app.main import initialize_system

# Initialize the HeartBeat system
system = initialize_system()

# Query the analytics engine
response = system.query("How effective was Montreal's power play against Toronto?")
print(response.content)
print(response.analytics)
```

### Advanced Analysis
```python
# Multi-game performance analysis
response = system.query("Compare Suzuki's performance in 5v5 vs power play situations")

# Trend analysis with video clips
response = system.query("What's the impact of youth pairings on zone exit success?")

# Predictive insights with visualizations
response = system.query("Which matchups should we target for better scoring opportunities?")
```

### API Usage
```python
import requests

# Query via REST API
response = requests.post("http://localhost:8000/api/query",
    json={"query": "Analyze Montreal's shot distribution patterns"}
)
result = response.json()
```

## Performance Benchmarks

- **Model**: DeepSeek-R1-Distill-Qwen-32B (32.7B parameters, MIT licensed)
- **Query Accuracy**: Target 90%+ statistically correct responses
- **Response Time**: <3 seconds average for complex analytical queries
- **Training Data**: 2,198 hockey analytics QA pairs for fine-tuning
- **Retrieval Precision**: >85% relevant information retrieval
- **Tool Integration**: Dynamic RAG + Parquet SQL hybrid queries

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
