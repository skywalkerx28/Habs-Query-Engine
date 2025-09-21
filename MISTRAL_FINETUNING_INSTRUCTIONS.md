# Mistral AI Fine-Tuning Instructions
## HeartBeat Engine - Montreal Canadiens Hockey Analyst

### Dataset Details
- **File**: mistral_finetuning_dataset_2024_2025.jsonl
- **Total Examples**: 1,982 conversation pairs
- **Format**: JSONL with messages array
- **Base Model**: ministral-8b-latest (recommended for HeartBeat)

### Mistral AI Platform Steps

1. **Access Platform**: Visit https://mistral.ai/products/la-plateforme
2. **Create Account**: Sign up for Mistral AI platform access
3. **Upload Dataset**:
   - Choose "Fine-tuning" section
   - Upload `mistral_finetuning_dataset_2024_2025.jsonl`
   - Select base model: `ministral-8b-latest`

4. **Recommended Training Parameters** (UPDATED for ministral-8b-latest):
   - **Learning Rate**: 1e-4 (Mistral recommended for LoRA fine-tuning)
   - **Epochs**: 3 (optimal for 1.7MB dataset)
   - **Batch Size**: Auto (let Mistral optimize)
   - **Validation Split**: 10%
   - **Max Steps**: ~500 (calculated: epochs × dataset_size_MB)
   - **Learning Rate Schedule**: Linear warmup + cosine decay

5. **Training Duration**: 4-8 hours depending on parameters
6. **Cost**: Check Mistral AI pricing for ministral-8b fine-tuning

### Model Capabilities After Training
- Strategic opponent analysis with professional terminology
- Player development guidance with coaching methodology
- Performance analysis using real Montreal Canadiens statistics
- Tactical recommendations based on comprehensive hockey knowledge

### Integration with HeartBeat Engine
After training completion:
1. Download the fine-tuned model
2. Integrate with Pinecone vector database
3. Deploy in hybrid RAG + real-time query system
4. Connect to Streamlit interface for conversational analytics

### Quality Assurance
- Model will respond with authentic hockey terminology
- Responses based on real statistical data
- Strategic analysis capabilities for coaches and players
- Professional consultant-level insights

---
**HeartBeat Engine**: AI-Powered Montreal Canadiens Analytics Platform
