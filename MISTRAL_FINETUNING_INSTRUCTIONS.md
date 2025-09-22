# Mistral AI Fine-Tuning Instructions
## HeartBeat Engine - Montreal Canadiens Hockey Analyst

## UPGRADED TO MISTRAL-LARGE-LATEST
**Model**: `mistral-large-latest` (Enhanced for AI Agent Development)
**Status**: Ready for advanced fine-tuning
**Enhanced Capabilities**: Superior reasoning, AI agent compatibility, advanced analytics
**Previous Model**: `ft:ministral-8b-latest:dd26ff35:20250921:5207f629` (deprecated)

### Dataset Details
- **Training File**: mistral_training_dataset_2024_2025.jsonl (1,586 examples)
- **Validation File**: mistral_validation_dataset_2024_2025.jsonl (396 examples)
- **Total Examples**: 1,982 conversation pairs (80/20 train/validation split)
- **Format**: JSONL with messages array
- **Dataset Size**: 1.7MB total (optimal for instruction tuning)
- **Quality**: High-quality, domain-specific Q&A pairs with enhanced system prompts
- **Target Model**: mistral-large-latest (optimized for AI agent development)
- **Enhanced Features**: Dynamic tool integration, hybrid RAG architecture support
- **Split Strategy**: Randomized 80/20 split for optimal overfitting prevention

### Why This Approach Works for mistral-large-latest
- **Instruction Tuning**: 1K-5K examples optimal for large model fine-tuning
- **Domain Expertise**: Quality hockey analytics patterns with professional terminology
- **Advanced Base Model**: mistral-large-latest provides superior reasoning and agent capabilities
- **AI Agent Ready**: Enhanced model supports future autonomous agent development
- **Enterprise Scale**: Large model handles complex multi-turn conversations and tool integration

### Benefits of Validation Dataset for Hockey Analytics
- **Overfitting Prevention**: Ensures model generalizes to new hockey scenarios beyond training examples
- **Performance Monitoring**: Real-time validation loss tracking during training prevents wasted compute
- **Quality Assurance**: Validates model's ability to analyze diverse hockey situations accurately
- **Early Stopping**: Automatically stops training when validation performance plateaus
- **Professional Reliability**: Ensures consistent performance for coaches, players, and analysts
- **Hyperparameter Optimization**: Helps fine-tune learning rate and training steps for optimal results

### Optimal Training Duration for Hockey Analytics
- **Recommended Epochs**: 3-4 epochs for 1,586 training examples
- **Formula**: Epochs = Training Steps ÷ Dataset Size (MB) = 10 ÷ 3.3 ≈ 3.0 epochs
- **Conservative Approach**: Start with 3 epochs to prevent overfitting on specialized hockey terminology
- **Domain Considerations**: Hockey analytics requires generalization, not memorization of specific games
- **Quality Focus**: Professional hockey staff need reliable insights across diverse scenarios
- **Early Stopping**: Use validation loss monitoring to determine optimal stopping point

### Mistral AI Platform Steps

#### Option 1: Web Platform (Recommended for Beginners)
1. **Access Platform**: Visit https://mistral.ai/products/la-plateforme
2. **Create Account**: Sign up for Mistral AI platform access
3. **Upload Datasets**:
   - Choose "Fine-tuning" section
   - Upload training file: `mistral_training_dataset_2024_2025.jsonl`
   - Upload validation file: `mistral_validation_dataset_2024_2025.jsonl`
   - Select base model: `mistral-large-latest`

#### Option 2: Programmatic API (Enterprise Approach)
```python
from mistralai import Mistral
import os

# Initialize Mistral Client
api_key = os.environ["MISTRAL_API_KEY"]
client = Mistral(api_key=api_key)

# Upload Training Dataset
training_data = client.files.upload(
    file={
        "file_name": "mistral_training_dataset_2024_2025.jsonl",
        "content": open("data/processed/llm_model/training/fine_tuning/mistral_training_dataset_2024_2025.jsonl", "rb"),
    }
)

# Upload Validation Dataset
validation_data = client.files.upload(
    file={
        "file_name": "mistral_validation_dataset_2024_2025.jsonl",
        "content": open("data/processed/llm_model/training/fine_tuning/mistral_validation_dataset_2024_2025.jsonl", "rb"),
    }
)

# Create Fine-Tuning Job with Validation
created_jobs = client.fine_tuning.jobs.create(
    model="mistral-large-latest",
    training_files=[{"file_id": training_data.id, "weight": 1}],
    validation_files=[validation_data.id],  # Enable overfitting prevention
    hyperparameters={
        "training_steps": 10,
        "learning_rate": 0.0001
    },
    auto_start=False,
)

# Start Training
client.fine_tuning.jobs.start(job_id=created_jobs.id)

# Monitor Progress
job_status = client.fine_tuning.jobs.get(job_id=created_jobs.id)
print(f"Training Status: {job_status.status}")
```

4. **Recommended Training Parameters** (OPTIMIZED for mistral-large-latest):
   - **Learning Rate**: 1e-4 (Mistral recommended for large model LoRA fine-tuning)
   - **Training Steps**: 10 (results in ~3 epochs with 3.3MB training data - optimal for hockey analytics)
   - **Batch Size**: Auto (Mistral optimizes for large model efficiency)
   - **Validation Split**: 10%
   - **Learning Rate Schedule**: Linear warmup + cosine decay
   - **Hyperparameters**: Enhanced for large model stability and agent compatibility
   - **Allowed Invalid Lines**: 5% (tolerance for data quality issues)

5. **Training Duration**: 15-45 minutes for mistral-large-latest (enhanced capabilities require more compute)
   - **Note**: Large model + comprehensive dataset = superior performance
   - **Quality**: 1,982 high-quality examples with enhanced system prompts for professional hockey analytics
   - **Infrastructure**: Requires GPUs with minimum 40GB VRAM for efficient training
6. **Cost**: Premium pricing for mistral-large-latest fine-tuning (check Mistral AI pricing)
   - **Investment**: Higher cost justified by AI agent capabilities and enterprise-grade performance

### Enhanced Model Capabilities After Training
- **Advanced Analytics**: Strategic opponent analysis with professional terminology and statistical depth
- **Player Development**: Comprehensive guidance using coaching methodology and performance metrics
- **Real-Time Integration**: Performance analysis using live Montreal Canadiens statistics via dynamic tools
- **Strategic Intelligence**: Tactical recommendations based on comprehensive hockey knowledge and situational analysis
- **AI Agent Compatibility**: Enhanced reasoning capabilities for future autonomous agent development
- **Multi-Modal Integration**: Supports complex tool usage and hybrid RAG architecture
- **Enterprise Scalability**: Professional-grade responses suitable for coaches, players, and management

### Integration with HeartBeat Engine
Post-training deployment with LangGraph orchestrator:
1. **LangGraph Agent Core**: Deploy `ft:mistral-large-latest:dd26ff35:20250921:af45b5ef` as central reasoning engine
2. **Node Architecture Implementation**: Intent → Router → Vector Search → Parquet SQL → Analytics → Visualization → Synthesis
3. **Identity & Security Layer**: Implement `resolve_current_user` with role-based data scoping and permission enforcement
4. **Tool Orchestration**: Integrate Pinecone RAG, Parquet analytics, xG calculations, and dynamic visualization generation
5. **Enterprise Guards**: Deploy resource limits, caching, timeout handling, and audit trail logging
6. **Optional Mistral Agents**: Add specialized services for post-game reports, scouting analysis, and fallback endpoints
7. **Production Interface**: LangGraph-powered Streamlit chat with multi-step tool orchestration and evidence-based responses

**Architecture Benefits:**
- **Maximum Control**: Full workflow orchestration with deterministic routing and error handling
- **Enterprise Security**: Identity-aware data access with comprehensive audit trails  
- **Vendor Independence**: Offline capabilities and flexible model deployment options
- **Performance Optimization**: Intelligent caching and parallel tool execution where possible

### Quality Assurance & Enhanced Features
- **Professional Communication**: Authentic hockey terminology with coaching-level expertise
- **Data-Driven Insights**: Responses based on real statistical data and live analytics
- **Strategic Intelligence**: Advanced analysis capabilities for coaches, players, and management
- **Consultant-Grade Output**: Professional insights with actionable recommendations
- **AI Agent Foundation**: Enhanced reasoning suitable for autonomous agent development
- **Tool Integration**: Seamless integration with dynamic analysis tools and hybrid RAG system
- **Enterprise Standards**: No emojis, clean technical language, professional hockey communication

### Infrastructure Requirements for mistral-large-latest

#### Hardware Requirements
- **GPU Memory**: Minimum 40GB VRAM (A100, H100, or equivalent)
- **System RAM**: 32GB+ recommended for optimal performance
- **Storage**: High-speed SSD with sufficient space for model checkpoints
- **Network**: Stable internet connection for cloud-based training

#### Cloud Training Considerations
- **Mistral AI Platform**: Recommended for production fine-tuning
- **Alternative**: GPU cloud providers (AWS, GCP, Azure) with appropriate instance types
- **Cost Optimization**: Use spot instances for development, reserved for production

#### AI Agent Development Readiness
- **Enhanced Reasoning**: Superior logical inference and multi-step problem solving
- **Tool Integration**: Native support for function calling and external tool usage
- **Multi-Modal Capabilities**: Foundation for future integration with visual and audio data
- **Agent Architecture**: Compatible with LangChain, AutoGPT, and custom agent frameworks
- **Scalability**: Enterprise-grade performance for concurrent user sessions

### Future AI Agent Applications
1. **Autonomous Game Analysis**: AI agents that independently analyze games and generate reports
2. **Real-Time Coaching Assistance**: Live game situation analysis and strategic recommendations
3. **Player Development Tracking**: Autonomous monitoring and reporting of player progress
4. **Opponent Intelligence**: Automated scouting reports and strategic analysis
5. **Performance Optimization**: AI-driven recommendations for lineup and strategy adjustments

---
**HeartBeat Engine**: AI-Powered Montreal Canadiens Analytics Platform - Enhanced with AI Agent Capabilities
