# HeartBeat Engine - Training Logs

This directory contains comprehensive training logs for all Mistral fine-tuning sessions used in the HeartBeat Engine project.

## Directory Structure

```
logs/
├── README.md                              # This file - logging system documentation
├── training_index.json                    # Master index of all training sessions
├── mistral_training_session_YYYYMMDD.log  # Detailed training logs for each session
└── [future session logs]                  # Additional training session logs
```

## File Descriptions

### training_index.json
- **Purpose**: Master index tracking all training sessions
- **Format**: JSON with comprehensive session metadata
- **Content**: Session IDs, model info, performance metrics, costs
- **Usage**: Quick reference for session comparison and tracking

### Session Log Files
- **Naming**: `mistral_training_session_YYYYMMDD.log`
- **Purpose**: Detailed technical logs for individual training sessions
- **Content**: Complete training progression, metrics, configuration details
- **Format**: Human-readable structured text format

## Current Training Sessions

### Session 1 (2025-09-21)
- **Model**: `ft:mistral-large-latest:dd26ff35:20250921:af45b5ef`
- **Status**: SUCCESS 
- **Performance**: Exceptional (72% loss improvement, minimal overfitting)
- **Cost**: $15.76 USD
- **Purpose**: Montreal Canadiens hockey analytics expertise

## Usage Guidelines

### For Developers
- Check `training_index.json` for quick session overview
- Review detailed logs for debugging or analysis
- Use session IDs to correlate with Mistral AI platform records

### For Model Performance Analysis  
- Compare training/validation loss trends across sessions
- Track cost efficiency and resource utilization
- Monitor overfitting and generalization quality

### For Production Deployment
- Verify training completion status before deployment
- Confirm quality assurance checkmarks in logs
- Reference model IDs for API integration

## Quality Standards

All training sessions logged here meet HeartBeat Engine quality standards:
- Professional hockey terminology learning
- Minimal overfitting (validation loss ≈ training loss)
- Cost-efficient resource utilization
- Montreal Canadiens domain expertise
- Production-ready performance metrics

## Integration Notes

These logs integrate with:
- **Mistral AI Platform**: Session IDs correlate with platform records
- **HeartBeat Engine**: Model IDs used in production deployment
- **Monitoring Systems**: Performance metrics for ongoing evaluation
- **Cost Management**: Resource utilization tracking and optimization

## Maintenance

- Logs are automatically generated after each training session
- Index file updated with each new training completion
- Historical logs preserved for performance comparison
- Regular backup recommended for production environments

---

**HeartBeat Engine v1.0**  
Montreal Canadiens Hockey Analytics Platform  
Generated: September 21, 2025
