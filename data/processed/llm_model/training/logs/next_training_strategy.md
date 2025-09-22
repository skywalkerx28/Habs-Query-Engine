# AWS SageMaker Training Dataset Strategy
## Advanced Tool Integration & LangGraph Preparation for Llama-3.3-70B-Instruct

### Training Session 2 Objectives

Building on enterprise-grade training infrastructure with AWS SageMaker, this training phase prepares the Llama-3.3-70B-Instruct model for sophisticated LangGraph orchestrator integration with enterprise-grade tool usage and identity-aware analytics.

## Core Training Focus Areas

### 1. Tool Orchestration Training (40% of Dataset)
**Goal**: Teach the model WHEN and HOW to use analytical tools in complex workflows

**Example Format**:
```json
{
  "messages": [
    {"role": "system", "content": "Enhanced system prompt with tool awareness..."},
    {"role": "user", "content": "Compare Hutson's zone exit success when paired with Guhle vs Savard over the last 10 games, and explain what this means for our upcoming series against Boston"},
    {"role": "assistant", "content": "I need to analyze this multi-step question by:\n\n1. [TOOL: parquet_query] Retrieving Hutson's zone exit data with Guhle pairing over last 10 games\n2. [TOOL: parquet_query] Retrieving Hutson's zone exit data with Savard pairing over last 10 games\n3. [TOOL: calculate_zone_stats] Computing success rates and situational effectiveness\n4. [TOOL: vector_search] Retrieving Boston's forechecking patterns and defensive tendencies\n5. [TOOL: matchup_analysis] Strategic implications for series planning\n\nBased on the analysis:\n- Hutson-Guhle pairing: 68% zone exit success (league average: 61%)\n- Hutson-Savard pairing: 59% zone exit success\n- Key insight: Guhle's mobility complements Hutson's vision under pressure\n- Boston implication: Their aggressive forecheck (3rd in league) will test zone exits heavily\n- Recommendation: Deploy Hutson-Guhle in high-pressure situations vs Boston"}
  ]
}
```

### 2. Multi-Turn Conversation Mastery (25% of Dataset)
**Goal**: Complex analytical discussions with context building and follow-up handling

**Example Chain**:
```json
[
  {
    "messages": [
      {"role": "system", "content": "..."},
      {"role": "user", "content": "How has our power play evolved since the coaching change?"},
      {"role": "assistant", "content": "[TOOL: parquet_query + time_analysis] Our power play has shown marked improvement since the coaching transition:\n\nPre-change (Oct-Dec): 18.2% efficiency, 47% zone entry success\nPost-change (Jan-Mar): 24.1% efficiency, 63% zone entry success\n\nKey tactical shifts:\n- Increased net-front presence (+31% screening plays)\n- Improved puck movement (avg pass time reduced by 0.8s)\n- Better personnel deployment (Hutson QB time +40%)\n\nThe data suggests the new system maximizes our skilled players' capabilities while maintaining structure."}
    ]
  },
  {
    "messages": [
      {"role": "system", "content": "..."},
      {"role": "user", "content": "Which specific opponents have we struggled against on the power play, and why?"},
      {"role": "assistant", "content": "[TOOL: opponent_analysis + penalty_kill_study] Based on our power play performance by opponent:\n\nStruggling Against:\n1. Boston (11.1% vs them): Elite penalty kill pressure disrupts our entries\n2. Tampa Bay (13.8% vs them): Strong goaltending + aggressive shot blocking\n3. Toronto (15.2% vs them): Quick transition defense limits our setup time\n\nSuccess Stories:\n1. Ottawa (31.2% vs them): Weak penalty kill structure we exploit effectively\n2. Detroit (28.7% vs them): Our speed advantage creates mismatches\n\nPattern: We excel vs. passive penalty kills but struggle against aggressive pressure systems that disrupt our zone entries and puck movement timing."}
    ]
  }
]
```

### 3. Identity-Aware & Role-Based Responses (20% of Dataset)
**Goal**: Understanding user roles and providing appropriately scoped insights

**Coach Perspective Example**:
```json
{
  "messages": [
    {"role": "system", "content": "You are responding to a Montreal Canadiens coach. Provide strategic insights with tactical depth suitable for game planning and lineup decisions."},
    {"role": "user", "content": "Should we adjust our defensive pairings against Tampa Bay's top line?"},
    {"role": "assistant", "content": "[TOOL: matchup_analysis + user_role_scope] Coach, here's my tactical assessment:\n\n**Opponent Analysis:**\n- Kucherov-Point-Hagel line: 62% offensive zone start efficiency, 2.1 xGF/60\n- They exploit weak-side cycles and quick east-west movement\n\n**Our Current Pairings vs Their Effectiveness:**\n- Guhle-Savard: 45% success rate suppressing their line (below team avg)\n- Matheson-Barron: 67% success rate (our best option)\n\n**Tactical Recommendation:**\n- Deploy Matheson-Barron as primary matchup pairing\n- Use Guhle-Savard in offensive zone starts to maximize their transition game\n- Consider 11F/7D if we need extra defensive depth for extended shifts\n\n**Personnel Note:** Matheson's gap control neutralizes Kucherov's speed, while Barron's reach disrupts their cross-ice passes."}
  ]
}
```

**Player Perspective Example**:
```json
{
  "messages": [
    {"role": "system", "content": "You are responding to a Montreal Canadiens player. Provide personal performance insights with actionable development focus areas."},
    {"role": "user", "content": "How can I improve my faceoff performance in the defensive zone?"},
    {"role": "assistant", "content": "[TOOL: player_analysis + development_focus] Based on your recent performance data:\n\n**Current Stats:**\n- Defensive zone FO%: 52.1% (team avg: 49.8%)\n- High-danger situations: 47.3% (room for improvement)\n\n**Key Improvement Areas:**\n1. **Timing Against Speed**: You're 8% less effective vs quick-draw centers\n2. **Body Position**: Strongest on tie-ups (63%) but inconsistent on clean wins\n3. **Situational Awareness**: 73% success when you initiate, 41% when reactive\n\n**Development Focus:**\n- Practice anticipation drills - watch opponent's stick position earlier\n- Strengthen core for better leverage in tie-up battles\n- Film study: You excel vs right-handed centers, struggle vs lefties\n\n**Next Game Target:** Focus on body positioning vs their top center - he favors forehand draws to his right side."}
  ]
}
```

### 4. Evidence-Based Analysis with Source Attribution (10% of Dataset)
**Goal**: Always cite sources and back insights with specific data points

**Example**:
```json
{
  "messages": [
    {"role": "system", "content": "Always provide evidence-based responses with clear source attribution from tools and data queries."},
    {"role": "user", "content": "Is our penalty kill actually improving or just facing weaker opposition?"},
    {"role": "assistant", "content": "[TOOL: penalty_kill_analysis + strength_of_schedule] **Quality-Adjusted Analysis:**\n\n**Raw Performance:**\n- Current PK%: 82.1% (6th in NHL)\n- January: 79.2%, February: 84.7%, March: 83.9%\n\n**Strength-Adjusted Performance:**\n[SOURCE: Opponent power play rankings + situational difficulty]\n- vs Top 10 PP teams: 80.3% (above league avg of 76.8%)\n- vs Bottom 10 PP teams: 85.1% (expected: 83.2%)\n- High-danger shot suppression: 31.2 per 60 (3rd best in league)\n\n**Key Evidence Points:**\n1. [SOURCE: Zone clear data] Improved D-to-D passing (89% completion vs 82% in Oct)\n2. [SOURCE: Personnel usage] Optimal line matching (+12% vs opposing PP1)\n3. [SOURCE: Goaltending metrics] Save% on PK has remained consistent (92.1%)\n\n**Conclusion:** Genuine improvement - we're outperforming expected results even against elite power plays, driven by systematic improvements rather than schedule luck."}
  ]
}
```

### 5. Error Handling & Edge Cases (5% of Dataset)
**Goal**: Graceful handling of incomplete data, tool failures, and ambiguous queries

**Example**:
```json
{
  "messages": [
    {"role": "system", "content": "Handle incomplete data gracefully and ask clarifying questions when needed."},
    {"role": "user", "content": "How did we do in that overtime game?"},
    {"role": "assistant", "content": "I'd be happy to analyze our overtime performance, but I need clarification to provide accurate insights:\n\n**Which specific game are you referring to?**\n- We've played 7 overtime games this season\n- Most recent: March 15 vs Toronto (3-2 OT win)\n- Highest stakes: February 22 vs Boston (2-3 OT loss)\n\n**Or would you prefer:**\n- Overall overtime performance analysis (7 games total)\n- Specific opponent or date range\n- Particular aspect (player performance, tactical execution, etc.)\n\nOnce you specify, I can use [TOOL: game_analysis] to pull detailed metrics and provide comprehensive insights about our overtime execution."}
  ]
}
```

## Dataset Composition Strategy

### Target Dataset Size: 2,000-2,200 Examples
- **Tool Integration Examples**: 800-900 (40%)
- **Multi-Turn Conversations**: 500-550 (25%)  
- **Role-Based Responses**: 400-440 (20%)
- **Evidence-Based Analysis**: 200-220 (10%)
- **Error Handling**: 100-110 (5%)

### Quality Standards (Aligned with Project Standards)
- **Professional Communication**: No emojis, coaching-level terminology
- **Technical Accuracy**: All metrics and calculations must be realistic and consistent
- **Montreal Focus**: Specific Canadiens players, opponents, and strategic contexts
- **Tool Integration**: Clear examples of WHEN and HOW to use each tool type
- **Source Attribution**: Always cite data sources and tool outputs

### Enhanced System Prompt for Session 2
```
You are an elite hockey analytics orchestrator for the Montreal Canadiens organization. You serve coaches, players, scouts, analysts, and staff with professional-grade insights by intelligently coordinating multiple analytical tools and data sources.

CORE CAPABILITIES:
- Orchestrate complex multi-step analysis workflows using RAG retrieval and real-time data tools
- Process natural language queries by determining optimal tool sequences and data requirements  
- Generate evidence-based insights with clear source attribution from all tool outputs
- Adapt communication style and data scope based on user role (coach/player/analyst/staff)
- Handle identity-aware data access and permission-based information filtering

TOOL ORCHESTRATION:
- Use [TOOL: vector_search] for hockey knowledge, rules, and strategic context
- Use [TOOL: parquet_query] for real-time player/team statistics and game data
- Use [TOOL: calculate_advanced_metrics] for xG, Corsi, zone analysis, and possession metrics
- Use [TOOL: matchup_analysis] for opponent analysis and tactical recommendations
- Use [TOOL: visualization] for heatmaps, charts, and statistical displays
- Always specify tool usage clearly and integrate results meaningfully

COMMUNICATION STANDARDS:
- Provide multi-step reasoning that shows your analytical workflow
- Back all insights with specific data points and source attribution
- Use authentic coach and player terminology appropriate for Montreal Canadiens personnel
- Structure responses with clear evidence chains and actionable recommendations
- Maintain professional communication standards with clean technical language

Your responses should demonstrate sophisticated analytical orchestration while remaining accessible to hockey personnel in operational and strategic contexts.
```

## Training Methodology

### Validation Split: 80/20 (Consistent with Session 1)
- **Training**: 1,600-1,760 examples  
- **Validation**: 400-440 examples
- **Quality Focus**: Each example teaches multiple skills simultaneously

### Success Metrics for Session 2
- **Tool Usage Accuracy**: Model correctly identifies appropriate tools >90% of time
- **Multi-Step Reasoning**: Coherent analytical workflows with proper sequencing
- **Role Awareness**: Appropriate response style based on user context
- **Evidence Integration**: Consistent source citation and data backing
- **Hockey Authenticity**: Professional terminology and realistic scenarios

This training dataset will transform your model from a foundational hockey analyst into a sophisticated orchestrator ready for your LangGraph architecture, capable of intelligent tool coordination and enterprise-grade analytical workflows.
