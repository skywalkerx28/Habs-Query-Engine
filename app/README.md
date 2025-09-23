# HeartBeat Engine - Streamlit Application

**Stanley - Montreal Canadiens Advanced Analytics Assistant**

Professional web interface for the HeartBeat hockey analytics platform with role-based access control and real-time data integration.

## Features

### Enterprise Authentication
- **Role-Based Access Control**: Coach, Player, Analyst, Staff, Scout permissions
- **Session Management**: Secure session handling with timeout protection
- **User Context Integration**: Seamless integration with orchestrator permissions

### Hockey Analytics Interface
- **Natural Language Queries**: Ask questions in plain English
- **Real-Time Processing**: Live integration with Pinecone RAG and Parquet analytics
- **Role-Specific Suggestions**: Tailored query suggestions based on user role
- **Query History**: Track and reuse previous queries

### Advanced Visualizations
- **Interactive Charts**: Plotly-powered visualizations for player and team data
- **Evidence Display**: Clear source attribution and citation management
- **Export Options**: Download results as JSON or formatted reports
- **Performance Metrics**: Real-time processing time and success rate tracking

### Production Features
- **SageMaker Integration**: Seamless connection to fine-tuned DeepSeek-R1-Distill-Qwen-32B model
- **Auto-Scaling**: Responsive design with performance optimization
- **Error Handling**: Graceful degradation and user-friendly error messages
- **Montreal Canadiens Branding**: Team colors and professional styling

## Quick Start

### Prerequisites
- Python 3.11+
- Access to HeartBeat orchestrator
- AWS credentials (for SageMaker integration)
- Pinecone API key (for RAG functionality)

### Installation

```bash
# Install dependencies
pip install -r app/requirements.txt

# Set environment variables
export PINECONE_API_KEY="your-pinecone-key"
export OPENAI_API_KEY="your-openai-key"  # Optional fallback

# Launch application
python run_app.py
```

### Access Application

1. Open browser to `http://localhost:8501`
2. Login with demo credentials or create account
3. Start asking hockey analytics questions

## User Roles and Access

### Coach (Martin St-Louis)
- **Username**: `coach_martin`
- **Password**: `coach2024`
- **Access**: Full tactical analysis, strategy planning, lineup decisions
- **Quick Actions**: Line combinations, matchup analysis, tactical insights

### Analyst (Kent Hughes)
- **Username**: `analyst_hughes` 
- **Password**: `analyst2024`
- **Access**: Comprehensive data analysis, advanced metrics, league comparisons
- **Quick Actions**: Advanced metrics, trend analysis, statistical deep dives

### Player (Nick Suzuki)
- **Username**: `player_suzuki`
- **Password**: `player2024`
- **Access**: Personal performance, team context, improvement focus
- **Quick Actions**: Personal stats, improvement areas, team role analysis

### Scout (Martin Lapointe)
- **Username**: `scout_lapointe`
- **Password**: `scout2024`
- **Access**: Player evaluation, opponent analysis, draft insights
- **Quick Actions**: Prospect evaluation, opponent scouting, draft analysis

### Staff (Geoff Molson)
- **Username**: `staff_molson`
- **Password**: `staff2024`
- **Access**: High-level summaries, operational insights
- **Quick Actions**: Team summary, performance overview

## Application Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Streamlit Frontend                       │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │    Auth     │  │   Query     │  │      Response       │  │
│  │  Manager    │  │ Interface   │  │     Display         │  │
│  └─────────────┘  └─────────────┘  └─────────────────────┘  │
├─────────────────────────────────────────────────────────────┤
│                HeartBeat Orchestrator                       │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │  Pinecone   │  │   Parquet   │  │   Fine-tuned        │  │
│  │    RAG      │  │ Analytics   │  │   DeepSeek-R1-Distill-Qwen-32B     │  │
│  └─────────────┘  └─────────────┘  └─────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

## Component Details

### Authentication System (`app/auth/`)
- **Role-based permissions**: Integrated with orchestrator user roles
- **Session security**: Timeout protection and secure session management
- **Demo accounts**: Development accounts for testing different roles

### Query Interface (`app/components/query_interface.py`)
- **Natural language input**: Free-form hockey analytics questions
- **Smart suggestions**: Role-specific query suggestions
- **Processing indicators**: Real-time progress display
- **History management**: Query history and favorites

### Response Display (`app/components/response_display.py`)
- **Formatted responses**: Professional response formatting with citations
- **Data visualizations**: Interactive charts and tables
- **Evidence tracking**: Clear source attribution
- **Export capabilities**: JSON and text report downloads

### SageMaker Integration (`app/utils/sagemaker_endpoint.py`)
- **Endpoint management**: Automated deployment and configuration
- **Inference calls**: Real-time model invocation
- **Health monitoring**: Endpoint status and performance tracking
- **Auto-scaling**: Dynamic resource management

## Usage Examples

### Basic Query Processing

```python
# Example queries by role:

# Coach queries
"Analyze our powerplay effectiveness against Boston's penalty kill"
"What line combinations work best in the third period?"
"How should we adjust our defensive strategy?"

# Player queries  
"How is my faceoff percentage compared to other centers?"
"What areas should I focus on for improvement?"
"How does my performance impact our powerplay success?"

# Analyst queries
"Show me xG trends for our top line over the last 10 games"
"Compare our possession metrics to league average"
"Analyze correlation between zone entries and scoring chances"

# Scout queries
"Evaluate this prospect's NHL readiness"
"Scout upcoming opponent's key players and tendencies"
"Analyze potential trade targets and system fit"
```

### Data Integration

The application seamlessly integrates:
- **Real Pinecone Data**: 100 records of game recaps and hockey knowledge
- **NHL Player Stats**: Comprehensive statistics for all 30 teams (2024-25 season)
- **Montreal Canadiens Analytics**: 176+ specialized analytics files
- **Advanced Metrics**: xG, Corsi, line combinations, tactical analysis

## Configuration

### Environment Variables

```bash
# Required
export PINECONE_API_KEY="your-pinecone-api-key"

# Optional
export OPENAI_API_KEY="your-openai-api-key"  # Fallback model
export HEARTBEAT_DEBUG="true"  # Enable debug mode
export HEARTBEAT_LOG_LEVEL="INFO"  # Logging level

# AWS (for SageMaker)
export AWS_ACCESS_KEY_ID="your-aws-access-key"
export AWS_SECRET_ACCESS_KEY="your-aws-secret-key"
export AWS_DEFAULT_REGION="ca-central-1"
```

### Application Settings

Update `app/config/app_config.py`:

```python
# Customize application settings
app_config.app_title = "Your Custom Title"
app_config.primary_color = "#AF1E2D"  # Montreal Canadiens red
app_config.session_timeout_minutes = 60

# Authentication settings
auth_config.enable_authentication = True
auth_config.session_duration_days = 7
```

## Development

### Project Structure

```
app/
├── __init__.py                 # Main app module
├── main.py                     # Main Streamlit application
├── requirements.txt            # Application dependencies
├── README.md                  # This documentation
├── auth/                      # Authentication system
│   ├── __init__.py
│   └── authentication.py
├── components/                # UI components
│   ├── __init__.py
│   ├── query_interface.py
│   └── response_display.py
├── config/                    # Configuration management
│   ├── __init__.py
│   └── app_config.py
├── pages/                     # Additional Streamlit pages
└── utils/                     # Utility functions
    ├── __init__.py
    ├── session_manager.py
    └── sagemaker_endpoint.py
```

### Adding New Features

1. **New UI Components**: Add to `app/components/`
2. **New Pages**: Add to `app/pages/` (auto-discovered by Streamlit)
3. **Configuration**: Update `app/config/app_config.py`
4. **Authentication**: Extend `app/auth/authentication.py`

### Testing

```bash
# Test application components
python -m pytest app/tests/

# Test orchestrator integration
python test_real_data_integration.py

# Manual testing
python run_app.py
```

## Deployment

### Local Development

```bash
# Quick start
python run_app.py

# Manual start
streamlit run app/main.py --server.port 8501
```

### Production Deployment

#### Docker Deployment

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Copy requirements and install
COPY app/requirements.txt ./app/
RUN pip install --no-cache-dir -r app/requirements.txt

# Copy application code
COPY app/ ./app/
COPY orchestrator/ ./orchestrator/
COPY data/ ./data/

# Expose Streamlit port
EXPOSE 8501

# Set environment
ENV PYTHONPATH=/app

# Run application
CMD ["streamlit", "run", "app/main.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

#### Cloud Deployment

```bash
# Build and deploy to cloud platform
docker build -t heartbeat-app .
docker run -p 8501:8501 heartbeat-app

# Or deploy to cloud service (AWS ECS, Google Cloud Run, etc.)
```

## Security Considerations

### Authentication Security
- **Password Protection**: Secure password handling (upgrade to hashed passwords in production)
- **Session Management**: Automatic timeout and secure session tokens
- **Role Enforcement**: Strict role-based access control throughout application

### Data Security
- **API Key Protection**: Secure environment variable handling
- **Session Isolation**: User data isolation between sessions
- **Audit Logging**: Complete user action tracking

### Network Security
- **HTTPS**: Enable HTTPS for production deployment
- **CORS**: Proper cross-origin request handling
- **Rate Limiting**: Prevent abuse and ensure fair usage

## Performance Optimization

### Caching Strategy
- **Query Results**: Intelligent caching of frequent queries
- **Data Loading**: Efficient data loading and processing
- **Session State**: Optimized session state management

### Monitoring
- **Performance Metrics**: Real-time performance tracking
- **Error Monitoring**: Comprehensive error logging and alerting
- **Usage Analytics**: User behavior and system usage analysis

---

**HeartBeat Engine Application Team**  
**Montreal Canadiens Advanced Analytics**  
Version 1.0.0
