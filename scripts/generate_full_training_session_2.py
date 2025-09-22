#!/usr/bin/env python3
"""
Complete Training Session 2 Dataset Generation
HeartBeat Engine - Montreal Canadiens Analytics Platform

Generates full-scale sophisticated training dataset (2,000+ examples)
for advanced LangGraph integration with tool orchestration mastery.
"""

import json
import random
import datetime
from typing import Dict, List, Any
from dataclasses import dataclass
from pathlib import Path

@dataclass 
class TrainingExample:
    """Structure for training examples with metadata"""
    category: str
    user_role: str
    complexity: str
    tools_used: List[str]
    messages: List[Dict[str, str]]

class AdvancedSession2Generator:
    """Complete dataset generator for Mistral Training Session 2"""
    
    def __init__(self):
        self.enhanced_system_prompt = """You are an elite hockey analytics orchestrator for the Montreal Canadiens organization. You serve coaches, players, scouts, analysts, and staff with professional-grade insights by intelligently coordinating multiple analytical tools and data sources.

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

Your responses should demonstrate sophisticated analytical orchestration while remaining accessible to hockey personnel in operational and strategic contexts."""

        # Enhanced Montreal Canadiens roster and context
        self.mtl_players = {
            "forwards": ["Suzuki", "Caufield", "Slafkovsky", "Dach", "Newhook", "Evans", "Gallagher", "Anderson", "Armia", "Dvorak", "Pezzetta", "Beck", "Roy", "Kapanen"],
            "defensemen": ["Hutson", "Guhle", "Matheson", "Savard", "Barron", "Xhekaj", "Struble", "Carrier", "Reinbacher"],
            "goalies": ["Primeau", "Montembeault", "Dobes"]
        }
        
        self.opponents = [
            "Toronto", "Boston", "Tampa Bay", "Florida", "Buffalo", "Ottawa", "Detroit",
            "New York Rangers", "New Jersey", "Philadelphia", "Washington", "Carolina",
            "Pittsburgh", "Columbus", "Nashville", "Winnipeg", "Calgary", "Edmonton",
            "Vancouver", "Seattle", "Colorado", "Vegas", "Los Angeles", "Anaheim"
        ]
        
        # Advanced query templates by category
        self.tool_integration_queries = [
            "Compare {player}'s {metric} when paired with {other_player} vs {third_player} over the last {timeframe} games",
            "Analyze our {system} effectiveness against {opponent}'s {counter_system} this season",
            "What's the impact of {player}'s {role} on our {team_metric} in {situation} situations?",
            "How do our {line_combo} combinations perform against {opponent_style} teams?",
            "Evaluate {player}'s {development_area} progression since the {milestone}",
            "What tactical adjustments should we make for {player}'s {weakness} against {opponent}?",
            "Compare our {special_teams} success rate in {venue} vs {comparison_venue}",
            "How effective is {defensive_pairing} at suppressing {opponent_strength}?",
        ]
        
        self.multi_turn_starters = [
            "How has our {system} evolved since the coaching change?",
            "What are the patterns in our {performance_area} struggles this season?",
            "Which {combinations} are working best for us right now?",
            "How do we match up against {competition_tier} teams?",
            "What's driving our recent improvement in {metric}?",
            "Which players are exceeding expectations in {role}?",
            "How sustainable is our current {trend}?",
            "What adjustments have opponents made to counter our {strength}?"
        ]
        
        self.role_specific_queries = {
            "coach": [
                "How should we handle {opponent}'s {line} in our building?",
                "What {position} pairing adjustments should we make for the next game?",
                "Which {special_teams} units work best against different {opponent_systems}?",
                "How can we exploit {opponent}'s {weakness} in key game situations?",
                "What's our optimal lineup for a {game_type} against {opponent}?",
                "How should we deploy {player} to maximize impact vs {opponent_style}?",
                "What tactical wrinkles can we add for the {playoff_series}?",
                "Which matchups give us the best advantage in {venue}?"
            ],
            "player": [
                "How can I improve my {skill} performance in {situation} situations?",
                "What areas of my {game_aspect} need the most work?",
                "How effective am I in different {combinations}?",
                "What should I focus on to earn more {ice_time_type}?",
                "How does my {metric} compare to {comparison_group}?",
                "What specific adjustments will help me against {opponent_type}?",
                "How can I be more consistent in my {performance_area}?",
                "What development focus will help me reach the next level?"
            ],
            "analyst": [
                "What's our actual {advanced_metric} compared to league average?",
                "How do our underlying metrics compare in {situation}?",
                "Which {statistical_indicator} best predicts our future performance?",
                "What's the statistical significance of our {trend}?",
                "How much of our {performance} is due to {factor} vs {other_factor}?",
                "What methodology should we use to evaluate {complex_metric}?",
                "How do we adjust our {metric} for strength of schedule?",
                "What sample size do we need for reliable {measurement}?"
            ]
        }
        
        # Professional hockey terminology pools
        self.hockey_terms = {
            "metrics": ["xG differential", "Corsi", "zone exit success", "shot quality", "possession time", "faceoff percentage", "shot suppression", "scoring chance creation"],
            "situations": ["power play", "penalty kill", "even strength", "overtime", "late game", "back-to-back", "road games", "divisional matchups"],
            "systems": ["forecheck", "neutral zone trap", "cycle game", "rush offense", "defensive coverage", "breakout system", "power play entry", "penalty kill pressure"],
            "positions": ["center", "winger", "defenseman", "goaltender", "forward", "d-pairing", "line combination", "special teams unit"],
            "game_situations": ["offensive zone start", "defensive zone faceoff", "line change", "timeout situation", "pulled goalie", "delayed penalty", "scramble play", "transition"]
        }

    def generate_tool_integration_dataset(self, target_count: int) -> List[TrainingExample]:
        """Generate sophisticated tool orchestration examples"""
        examples = []
        
        print(f"Generating {target_count} tool integration examples...")
        
        for i in range(target_count):
            # Create realistic scenarios with varying complexity
            complexity_level = random.choices(
                ["basic", "intermediate", "advanced", "expert"],
                weights=[0.2, 0.3, 0.35, 0.15]
            )[0]
            
            # Generate contextual query
            query_template = random.choice(self.tool_integration_queries)
            query = self._populate_query_template(query_template)
            
            # Determine tools based on query complexity
            tools = self._select_tools_for_complexity(complexity_level)
            
            # Generate sophisticated response
            response = self._generate_tool_workflow_response(query, tools, complexity_level)
            
            examples.append(TrainingExample(
                category="tool_integration",
                user_role="mixed",
                complexity=complexity_level,
                tools_used=tools,
                messages=[
                    {"role": "system", "content": self.enhanced_system_prompt},
                    {"role": "user", "content": query},
                    {"role": "assistant", "content": response}
                ]
            ))
            
            if (i + 1) % 100 == 0:
                print(f"  Generated {i + 1}/{target_count} tool integration examples")
        
        return examples

    def generate_multi_turn_dataset(self, target_count: int) -> List[TrainingExample]:
        """Generate multi-turn conversation examples"""
        examples = []
        conversation_pairs = target_count // 2  # Each conversation generates 2 examples
        
        print(f"Generating {target_count} multi-turn conversation examples...")
        
        for i in range(conversation_pairs):
            # Initial question
            starter_template = random.choice(self.multi_turn_starters)
            starter_query = self._populate_query_template(starter_template)
            
            # Generate first response
            first_response = self._generate_analytical_baseline_response(starter_query)
            
            # Follow-up question
            follow_up = self._generate_contextual_followup(starter_query)
            follow_response = self._generate_analytical_deepdive_response(follow_up, starter_query)
            
            # First turn
            examples.append(TrainingExample(
                category="multi_turn_initial",
                user_role="analyst",
                complexity="baseline",
                tools_used=["parquet_query", "calculate_advanced_metrics"],
                messages=[
                    {"role": "system", "content": self.enhanced_system_prompt},
                    {"role": "user", "content": starter_query},
                    {"role": "assistant", "content": first_response}
                ]
            ))
            
            # Follow-up turn
            examples.append(TrainingExample(
                category="multi_turn_followup",
                user_role="analyst",
                complexity="deepdive",
                tools_used=["opponent_analysis", "tactical_breakdown", "comparison_analysis"],
                messages=[
                    {"role": "system", "content": self.enhanced_system_prompt},
                    {"role": "user", "content": follow_up},
                    {"role": "assistant", "content": follow_response}
                ]
            ))
            
            if (i + 1) % 50 == 0:
                print(f"  Generated {(i + 1) * 2}/{target_count} multi-turn examples")
        
        return examples

    def generate_role_based_dataset(self, target_count: int) -> List[TrainingExample]:
        """Generate role-specific response examples"""
        examples = []
        roles = ["coach", "player", "analyst"]
        examples_per_role = target_count // 3
        
        print(f"Generating {target_count} role-based examples...")
        
        for role in roles:
            role_system_prompt = self._get_role_system_prompt(role)
            queries = self.role_specific_queries[role]
            
            for i in range(examples_per_role):
                query_template = random.choice(queries)
                query = self._populate_query_template(query_template)
                response = self._generate_role_specific_response(query, role)
                
                examples.append(TrainingExample(
                    category="role_specific",
                    user_role=role,
                    complexity="targeted",
                    tools_used=self._get_role_specific_tools(role),
                    messages=[
                        {"role": "system", "content": role_system_prompt},
                        {"role": "user", "content": query},
                        {"role": "assistant", "content": response}
                    ]
                ))
        
        print(f"  Generated {len(examples)} role-based examples")
        return examples

    def generate_evidence_based_dataset(self, target_count: int) -> List[TrainingExample]:
        """Generate evidence-heavy analytical examples"""
        examples = []
        
        evidence_query_templates = [
            "Is our {performance_metric} actually sustainable based on underlying metrics?",
            "Are we genuinely better at {aspect} or just facing weaker {opposition_factor}?",
            "What's driving our {trend} - {factor1} or {factor2} changes?",
            "How much of our {success_metric} is due to {primary_factor} vs {secondary_factor}?",
            "What does the data actually show about our {controversial_topic}?",
            "How statistically significant is our improvement in {metric_area}?",
            "Which metrics best predict our performance in {situation_type}?",
            "What's the real story behind our {narrative} this season?"
        ]
        
        print(f"Generating {target_count} evidence-based examples...")
        
        for i in range(target_count):
            query_template = random.choice(evidence_query_templates)
            query = self._populate_query_template(query_template)
            response = self._generate_evidence_heavy_response(query)
            
            examples.append(TrainingExample(
                category="evidence_based",
                user_role="analyst",
                complexity="methodical",
                tools_used=["parquet_query", "statistical_analysis", "strength_adjustment"],
                messages=[
                    {"role": "system", "content": "Always provide evidence-based responses with clear source attribution from tools and data queries."},
                    {"role": "user", "content": query},
                    {"role": "assistant", "content": response}
                ]
            ))
        
        print(f"  Generated {target_count} evidence-based examples")
        return examples

    def generate_error_handling_dataset(self, target_count: int) -> List[TrainingExample]:
        """Generate error handling and clarification examples"""
        examples = []
        
        ambiguous_query_templates = [
            "How did we do in that {vague_reference} game?",
            "What about our {system} against {vague_opponent}?",
            "Can you check {unclear_player}'s {unspecified_stats}?",
            "How are we doing {temporal_vague}?",
            "What's the story with {ambiguous_topic}?",
            "How did {unclear_event} go?",
            "Any updates on {vague_situation}?",
            "What do you think about {open_ended_topic}?"
        ]
        
        print(f"Generating {target_count} error handling examples...")
        
        for i in range(target_count):
            query_template = random.choice(ambiguous_query_templates)
            query = self._populate_ambiguous_template(query_template)
            response = self._generate_clarification_response(query)
            
            examples.append(TrainingExample(
                category="error_handling",
                user_role="general",
                complexity="clarification",
                tools_used=["clarification_request"],
                messages=[
                    {"role": "system", "content": "Handle incomplete data gracefully and ask clarifying questions when needed."},
                    {"role": "user", "content": query},
                    {"role": "assistant", "content": response}
                ]
            ))
        
        print(f"  Generated {target_count} error handling examples")
        return examples

    # Helper methods for content generation
    def _populate_query_template(self, template: str) -> str:
        """Fill template with realistic hockey context"""
        replacements = {
            "player": random.choice(self.mtl_players["forwards"] + self.mtl_players["defensemen"]),
            "other_player": random.choice(self.mtl_players["forwards"] + self.mtl_players["defensemen"]),
            "third_player": random.choice(self.mtl_players["forwards"] + self.mtl_players["defensemen"]),
            "opponent": random.choice(self.opponents),
            "timeframe": str(random.randint(8, 20)),
            "metric": random.choice(self.hockey_terms["metrics"]),
            "system": random.choice(self.hockey_terms["systems"]),
            "counter_system": random.choice(self.hockey_terms["systems"]),
            "situation": random.choice(self.hockey_terms["situations"]),
            "role": random.choice(self.hockey_terms["positions"]),
            "team_metric": random.choice(self.hockey_terms["metrics"]),
            "line_combo": "line",
            "opponent_style": random.choice(["aggressive", "defensive", "high-tempo", "physical"]),
            "development_area": random.choice(["faceoffs", "shot selection", "positioning", "decision-making"]),
            "milestone": random.choice(["coaching change", "trade deadline", "all-star break"]),
            "weakness": random.choice(["neutral zone", "power play", "defensive coverage"]),
            "special_teams": random.choice(["power play", "penalty kill"]),
            "venue": random.choice(["home", "road"]),
            "comparison_venue": "road" if template.find("home") != -1 else "home",
            "defensive_pairing": "defensive pairing",
            "opponent_strength": random.choice(["cycle game", "rush offense", "power play"]),
            "performance_area": random.choice(self.hockey_terms["metrics"]),
            "combinations": random.choice(["line combinations", "defensive pairings"]),
            "competition_tier": random.choice(["playoff", "division rival", "top-10"]),
            "trend": random.choice(["winning streak", "power play success", "defensive improvement"]),
            "strength": random.choice(self.hockey_terms["systems"]),
            "position": random.choice(["forward", "defensive"]),
            "game_type": random.choice(["playoff game", "back-to-back", "divisional matchup"]),
            "opponent_style": random.choice(["aggressive", "defensive", "speed-based"]),
            "playoff_series": "playoff series",
            "skill": random.choice(["faceoff", "shot", "passing", "positioning"]),
            "game_aspect": random.choice(["offensive", "defensive", "special teams"]),
            "ice_time_type": random.choice(["power play time", "penalty kill time", "even strength minutes"]),
            "comparison_group": "similar players",
            "opponent_type": random.choice(["elite centers", "physical teams", "fast opponents"]),
            "performance_area": random.choice(self.hockey_terms["metrics"]),
            "advanced_metric": random.choice(self.hockey_terms["metrics"]),
            "statistical_indicator": random.choice(["Corsi", "xG differential", "shot quality"]),
            "performance": random.choice(["recent success", "improved defense"]),
            "factor": random.choice(["goaltending", "special teams", "depth scoring"]),
            "other_factor": random.choice(["coaching", "health", "schedule"]),
            "complex_metric": random.choice(["zone exit efficiency", "defensive impact"]),
            "measurement": random.choice(["performance trends", "player development"])
        }
        
        result = template
        for key, value in replacements.items():
            result = result.replace("{" + key + "}", value)
        return result

    def _populate_ambiguous_template(self, template: str) -> str:
        """Fill ambiguous templates with vague references"""
        replacements = {
            "vague_reference": random.choice(["overtime", "important", "recent", "big"]),
            "system": random.choice(["power play", "penalty kill", "defense"]),
            "vague_opponent": random.choice(["Boston", "Toronto", "them"]),
            "unclear_player": random.choice(["Smith", "Johnson", "the new guy"]),
            "unspecified_stats": random.choice(["numbers", "stats", "performance"]),
            "temporal_vague": random.choice(["lately", "recently", "these days"]),
            "ambiguous_topic": random.choice(["the situation", "what happened", "the changes"]),
            "unclear_event": random.choice(["the game", "that play", "the incident"]),
            "vague_situation": random.choice(["the injury", "the lineup", "the system"]),
            "open_ended_topic": random.choice(["our chances", "the team", "how we look"])
        }
        
        result = template
        for key, value in replacements.items():
            result = result.replace("{" + key + "}", value)
        return result

    def _select_tools_for_complexity(self, complexity: str) -> List[str]:
        """Select appropriate tools based on complexity level"""
        tool_pools = {
            "basic": ["parquet_query", "calculate_advanced_metrics"],
            "intermediate": ["parquet_query", "calculate_advanced_metrics", "matchup_analysis"],
            "advanced": ["parquet_query", "calculate_advanced_metrics", "matchup_analysis", "vector_search"],
            "expert": ["parquet_query", "calculate_advanced_metrics", "matchup_analysis", "vector_search", "visualization", "tactical_analysis"]
        }
        
        base_tools = tool_pools.get(complexity, tool_pools["intermediate"])
        return base_tools[:random.randint(2, min(4, len(base_tools)))]

    def _generate_tool_workflow_response(self, query: str, tools: List[str], complexity: str) -> str:
        """Generate sophisticated tool orchestration response"""
        steps = []
        
        for i, tool in enumerate(tools, 1):
            tool_desc = self._get_tool_description(tool)
            metrics = self._generate_realistic_metrics(tool)
            steps.append(f"**Step {i}: [TOOL: {tool}]** - {tool_desc}\n{metrics}")
        
        insights = self._generate_complexity_insights(complexity)
        recommendation = self._generate_strategic_recommendation(complexity)
        
        response_parts = [
            "I'll analyze this query using a multi-step approach:",
            "",
            "\n\n".join(steps),
            "",
            "**Key Insights:**",
            insights,
            "",
            f"**Recommendation**: {recommendation}"
        ]
        
        return "\n".join(response_parts)

    def _generate_realistic_metrics(self, tool: str) -> str:
        """Generate realistic metrics based on tool type"""
        metrics_map = {
            "parquet_query": [
                f"- {random.choice(['Shot attempts', 'Zone entries', 'Faceoff wins'])}: {random.randint(15, 45)} ({random.randint(45, 75)}% success rate)",
                f"- {random.choice(['Ice time', 'Possession time'])}: {random.uniform(12.5, 20.8):.1f} minutes per game",
                f"- {random.choice(['Goals', 'Assists', 'Points'])}: {random.randint(8, 25)} in {random.randint(15, 30)} games"
            ],
            "calculate_advanced_metrics": [
                f"- Expected Goals: {random.uniform(1.2, 4.8):.1f} (actual: {random.randint(2, 6)})",
                f"- Corsi For %: {random.randint(48, 62)}% at even strength",
                f"- High-danger chances: {random.uniform(1.8, 3.5):.1f} per 60 minutes"
            ],
            "matchup_analysis": [
                f"- Opponent success rate: {random.randint(35, 75)}% in similar situations",
                f"- Historical performance: {random.randint(3, 8)}-{random.randint(2, 6)} record",
                f"- Key matchup advantage: {random.choice(['Speed differential', 'Size mismatch', 'Tactical edge'])}"
            ],
            "vector_search": [
                f"- League best practice: {random.choice(['Elite teams maintain', 'Top performers achieve'])} {random.randint(65, 85)}% in this area",
                f"- Strategic context: {random.choice(['This approach', 'Similar systems'])} typically {random.choice(['improve', 'optimize'])} {random.choice(['performance', 'efficiency'])} by {random.randint(8, 25)}%",
                f"- Historical precedent: {random.choice(['Montreal', 'Similar teams'])} saw {random.randint(12, 28)}% improvement using this approach"
            ]
        }
        
        return "\n".join(random.sample(metrics_map.get(tool, ["- Analysis completed"]), min(3, len(metrics_map.get(tool, [])))))

    def _generate_complexity_insights(self, complexity: str) -> str:
        """Generate insights appropriate to complexity level"""
        insight_pools = {
            "basic": [
                "1. **Performance Trend**: Consistent improvement in key metrics over recent games",
                "2. **Statistical Context**: Numbers align with team averages and expectations", 
                "3. **Tactical Application**: Current approach shows positive correlation with success"
            ],
            "intermediate": [
                "1. **Multi-Dimensional Analysis**: Performance varies significantly by game situation and opponent",
                "2. **Correlation Patterns**: Strong relationship between positioning and effectiveness metrics",
                "3. **Systemic Impact**: Individual performance directly influences line and team success rates"
            ],
            "advanced": [
                "1. **Strategic Integration**: Performance patterns reveal systematic advantages in specific matchups",
                "2. **Predictive Indicators**: Underlying metrics suggest sustainable improvement trajectory", 
                "3. **Tactical Optimization**: Data supports refined deployment strategies for maximum impact"
            ],
            "expert": [
                "1. **Comprehensive Assessment**: Multi-layered analysis reveals complex interaction effects between variables",
                "2. **Predictive Modeling**: Advanced metrics indicate high probability of continued success with current approach",
                "3. **Strategic Synthesis**: Data convergence across multiple analysis dimensions supports tactical evolution"
            ]
        }
        
        return "\n".join(insight_pools.get(complexity, insight_pools["intermediate"]))

    def _generate_strategic_recommendation(self, complexity: str) -> str:
        """Generate recommendations based on complexity"""
        rec_pools = {
            "basic": [
                "Continue current approach while monitoring key performance indicators",
                "Maintain focus on fundamental execution with minor tactical adjustments",
                "Build on current success patterns while addressing identified weaknesses"
            ],
            "intermediate": [
                "Implement targeted adjustments based on situational performance analysis",
                "Optimize deployment strategies to maximize identified advantages", 
                "Develop contingency approaches for challenging matchup scenarios"
            ],
            "advanced": [
                "Execute comprehensive tactical evolution based on multi-dimensional analysis findings",
                "Implement sophisticated deployment matrix optimized for various game situations",
                "Develop advanced preparation protocols targeting identified strategic opportunities"
            ],
            "expert": [
                "Deploy integrated strategic framework combining all analysis dimensions for optimal performance",
                "Implement dynamic tactical system with real-time adjustments based on predictive indicators",
                "Establish comprehensive monitoring and optimization protocols for sustained competitive advantage"
            ]
        }
        
        return random.choice(rec_pools.get(complexity, rec_pools["intermediate"]))

    # Additional helper methods
    def _get_tool_description(self, tool: str) -> str:
        descriptions = {
            "parquet_query": "Retrieving real-time player statistics and game data",
            "calculate_advanced_metrics": "Computing xG, Corsi, and possession analytics",
            "matchup_analysis": "Opponent analysis and tactical breakdown",
            "vector_search": "Hockey knowledge and strategic context retrieval",
            "visualization": "Generating performance heatmaps and statistical displays",
            "tactical_analysis": "Advanced strategic assessment and recommendations"
        }
        return descriptions.get(tool, "Analytical tool execution")

    def _get_role_system_prompt(self, role: str) -> str:
        prompts = {
            "coach": "You are responding to a Montreal Canadiens coach. Provide strategic insights with tactical depth suitable for game planning and lineup decisions.",
            "player": "You are responding to a Montreal Canadiens player. Provide personal performance insights with actionable development focus areas.",
            "analyst": "You are responding to a Montreal Canadiens analyst. Provide detailed statistical insights with methodological rigor suitable for front office evaluation."
        }
        return prompts[role]

    def _get_role_specific_tools(self, role: str) -> List[str]:
        tool_map = {
            "coach": ["matchup_analysis", "tactical_breakdown", "deployment_optimization"],
            "player": ["player_analysis", "development_focus", "performance_comparison"],
            "analyst": ["statistical_analysis", "methodology_validation", "predictive_modeling"]
        }
        return tool_map[role]

    def _generate_analytical_baseline_response(self, query: str) -> str:
        return f"**[TOOL: parquet_query]** - Analyzing recent performance trends:\n\n{self._generate_performance_summary()}\n\n**[TOOL: calculate_advanced_metrics]** - Advanced statistical breakdown:\n{self._generate_advanced_summary()}\n\n**Key Findings:**\n{self._generate_findings()}"

    def _generate_contextual_followup(self, original_query: str) -> str:
        followups = [
            "Which specific opponents have we struggled against in this area?",
            "What tactical adjustments would you recommend based on this analysis?",
            "How does this compare to our performance last season?",
            "Which players are driving these trends?",
            "What's the underlying cause of these patterns?",
            "How sustainable are these improvements?",
            "What should we be concerned about going forward?",
            "Which metrics are most predictive of future success?"
        ]
        return random.choice(followups)

    def _generate_analytical_deepdive_response(self, followup: str, original: str) -> str:
        return f"**[TOOL: opponent_analysis]** - Detailed breakdown:\n\n{self._generate_opponent_details()}\n\n**[TOOL: tactical_breakdown]** - Strategic implications:\n{self._generate_tactical_details()}\n\n**Recommendation**: {self._generate_specific_advice()}"

    def _generate_role_specific_response(self, query: str, role: str) -> str:
        if role == "coach":
            return f"**[TOOL: matchup_analysis]** - Tactical assessment:\n\n{self._generate_coach_analysis()}\n\n**Strategic Game Plan:**\n{self._generate_game_plan()}"
        elif role == "player":
            return f"**[TOOL: player_analysis]** - Your performance breakdown:\n\n{self._generate_player_feedback()}\n\n**Development Focus:**\n{self._generate_development_recommendations()}"
        else:  # analyst
            return f"**[TOOL: statistical_analysis]** - Comprehensive analysis:\n\n{self._generate_statistical_breakdown()}\n\n**Methodology:**\n{self._generate_methodology_notes()}"

    def _generate_evidence_heavy_response(self, query: str) -> str:
        return f"**[TOOL: parquet_query]** - Comprehensive data analysis:\n\n{self._generate_evidence_data()}\n\n**[SOURCE: Statistical validation]** - Strength-adjusted metrics:\n{self._generate_source_citations()}\n\n**Statistical Significance:**\n{self._generate_significance_analysis()}\n\n**Conclusion**: {self._generate_evidence_conclusion()}"

    def _generate_clarification_response(self, query: str) -> str:
        return f"I'd be happy to help with that analysis, but I need clarification to provide accurate insights:\n\n**Which specific {self._get_clarification_element()} are you referring to?**\n- {self._generate_clarification_option()}\n- {self._generate_clarification_option()}\n- {self._generate_clarification_option()}\n\n**Or would you prefer:**\n- {self._generate_alternative_option()}\n- {self._generate_alternative_option()}\n\nOnce you specify, I can use the appropriate tools to provide comprehensive insights with specific metrics and analysis."

    # Placeholder methods for realistic content generation
    def _generate_performance_summary(self) -> str:
        return f"Recent performance shows {random.choice(['improvement', 'consistency', 'mixed results'])} with {random.uniform(2.1, 3.8):.1f} {random.choice(['goals per game', 'expected goals', 'scoring chances'])}"

    def _generate_advanced_summary(self) -> str:
        return f"Advanced metrics: {random.randint(52, 68)}% Corsi, {random.uniform(1.8, 3.2):.1f} xG differential, {random.randint(28, 45)}% high-danger rate"

    def _generate_findings(self) -> str:
        return f"1. {random.choice(['Significant', 'Moderate', 'Slight'])} improvement in {random.choice(self.hockey_terms['metrics'])}\n2. {random.choice(['Strong', 'Consistent', 'Variable'])} performance against {random.choice(['division rivals', 'playoff teams', 'similar opponents'])}"

    def _generate_opponent_details(self) -> str:
        return f"vs {random.choice(self.opponents)}: {random.randint(2, 6)}-{random.randint(1, 4)} record, {random.uniform(2.1, 4.2):.1f} goals per game differential"

    def _generate_tactical_details(self) -> str:
        return f"{random.choice(['Tactical', 'Strategic', 'System'])} adjustments show {random.randint(12, 35)}% improvement in {random.choice(self.hockey_terms['metrics'])}"

    def _generate_specific_advice(self) -> str:
        return f"Focus on {random.choice(['maintaining', 'improving', 'adjusting'])} {random.choice(self.hockey_terms['systems'])} for {random.choice(['upcoming games', 'playoff preparation', 'season optimization'])}"

    def _generate_coach_analysis(self) -> str:
        return f"Matchup advantages: {random.choice(['Speed differential', 'Size mismatch', 'System superiority'])}\nKey factors: {random.choice(['Home ice', 'Rest advantage', 'Health status'])}"

    def _generate_game_plan(self) -> str:
        return f"1. Deploy {random.choice(['Matheson-Barron', 'Guhle-Savard'])} vs their top line\n2. Use {random.choice(['aggressive forecheck', 'neutral zone trap', 'cycle game'])} to exploit weakness"

    def _generate_player_feedback(self) -> str:
        return f"Performance metrics: {random.randint(65, 88)}th percentile\nStrength areas: {random.choice(['Positioning', 'Decision-making', 'Execution'])}"

    def _generate_development_recommendations(self) -> str:
        return f"Priority focus: {random.choice(['Consistency', 'Timing', 'Technique'])}\nPractice emphasis: {random.choice(['Repetition', 'Game situations', 'System integration'])}"

    def _generate_statistical_breakdown(self) -> str:
        return f"Statistical significance: {random.choice(['High', 'Moderate', 'Limited'])} (n={random.randint(25, 60)})\nPerformance differential: +{random.uniform(0.2, 1.1):.1f} {random.choice(['goals', 'points', 'expected goals'])}"

    def _generate_methodology_notes(self) -> str:
        return f"Sample size: {random.randint(800, 1500)} events, Confidence: {random.randint(85, 95)}%, Adjusted for {random.choice(['strength of schedule', 'game state', 'injury impact'])}"

    def _generate_evidence_data(self) -> str:
        return f"Sample analysis: {random.randint(35, 65)} games, Performance vs expected: +{random.uniform(0.15, 0.85):.2f}"

    def _generate_source_citations(self) -> str:
        return f"[SOURCE: {random.choice(['Game logs', 'Shot data', 'Usage statistics'])}] Context-adjusted metrics: {random.uniform(0.85, 1.25):.2f} multiplier"

    def _generate_significance_analysis(self) -> str:
        return f"Confidence level: {random.randint(82, 96)}%, Effect size: {random.choice(['Small', 'Medium', 'Large'])}, Sample adequacy: {random.choice(['Sufficient', 'Limited', 'Robust'])}"

    def _generate_evidence_conclusion(self) -> str:
        return f"Analysis indicates {random.choice(['genuine improvement', 'sustainable trend', 'statistical significance'])} supported by {random.choice(['multiple indicators', 'consistent patterns', 'contextual factors'])}"

    def _get_clarification_element(self) -> str:
        return random.choice(["game", "player", "metric", "time period", "opponent", "situation"])

    def _generate_clarification_option(self) -> str:
        options = [
            f"{random.choice(self.opponents)} on {random.choice(['March 15', 'February 8', 'January 22'])}",
            f"Last {random.randint(5, 15)} games performance",
            f"{random.choice(['Power play', 'Even strength', 'Penalty kill'])} specific analysis"
        ]
        return random.choice(options)

    def _generate_alternative_option(self) -> str:
        return random.choice([
            "Season summary with trend analysis",
            "Comparison to league averages",
            "Focus on specific performance area"
        ])

def main():
    """Generate complete Training Session 2 dataset"""
    
    generator = AdvancedSession2Generator()
    output_dir = Path("/Users/xavier.bouchard/Desktop/HeartBeat/data/processed/llm_model/training/fine_tuning")
    
    print("=" * 80)
    print("GENERATING COMPLETE TRAINING SESSION 2 DATASET")
    print("HeartBeat Engine - Montreal Canadiens Analytics Platform")
    print("=" * 80)
    print()
    
    # Dataset composition targets
    composition = {
        "tool_integration": 880,      # 40%
        "multi_turn": 550,           # 25%  
        "role_based": 440,           # 20%
        "evidence_based": 220,       # 10%
        "error_handling": 110        # 5%
    }
    
    total_target = sum(composition.values())
    print(f"Target Dataset Size: {total_target:,} examples")
    print(f"Composition: {composition}")
    print()
    
    all_examples = []
    
    # Generate each category
    print("PHASE 1: Tool Integration Examples (40%)")
    tool_examples = generator.generate_tool_integration_dataset(composition["tool_integration"])
    all_examples.extend(tool_examples)
    print(f"✅ Generated {len(tool_examples)} tool integration examples")
    print()
    
    print("PHASE 2: Multi-Turn Conversations (25%)")
    multi_examples = generator.generate_multi_turn_dataset(composition["multi_turn"])
    all_examples.extend(multi_examples)
    print(f"✅ Generated {len(multi_examples)} multi-turn examples")
    print()
    
    print("PHASE 3: Role-Based Responses (20%)")
    role_examples = generator.generate_role_based_dataset(composition["role_based"])
    all_examples.extend(role_examples)
    print(f"✅ Generated {len(role_examples)} role-based examples")
    print()
    
    print("PHASE 4: Evidence-Based Analysis (10%)")
    evidence_examples = generator.generate_evidence_based_dataset(composition["evidence_based"])
    all_examples.extend(evidence_examples)
    print(f"✅ Generated {len(evidence_examples)} evidence-based examples")
    print()
    
    print("PHASE 5: Error Handling (5%)")
    error_examples = generator.generate_error_handling_dataset(composition["error_handling"])
    all_examples.extend(error_examples)
    print(f"✅ Generated {len(error_examples)} error handling examples")
    print()
    
    # Shuffle for variety
    random.shuffle(all_examples)
    
    # Create training/validation split (80/20)
    total_examples = len(all_examples)
    split_index = int(total_examples * 0.8)
    
    training_examples = all_examples[:split_index]
    validation_examples = all_examples[split_index:]
    
    print("=" * 80)
    print("DATASET SPLIT & EXPORT")
    print("=" * 80)
    
    # Export training dataset
    training_file = output_dir / "mistral_training_dataset_session_2.jsonl"
    with open(training_file, 'w', encoding='utf-8') as f:
        for example in training_examples:
            # Convert to messages format for Mistral
            training_item = {"messages": example.messages}
            json.dump(training_item, f, ensure_ascii=False)
            f.write('\n')
    
    # Export validation dataset
    validation_file = output_dir / "mistral_validation_dataset_session_2.jsonl"
    with open(validation_file, 'w', encoding='utf-8') as f:
        for example in validation_examples:
            # Convert to messages format for Mistral
            validation_item = {"messages": example.messages}
            json.dump(validation_item, f, ensure_ascii=False)
            f.write('\n')
    
    print(f"📁 Training Dataset: {training_file}")
    print(f"   Examples: {len(training_examples):,}")
    print(f"   File size: {training_file.stat().st_size / (1024*1024):.1f} MB")
    print()
    
    print(f"📁 Validation Dataset: {validation_file}")
    print(f"   Examples: {len(validation_examples):,}")
    print(f"   File size: {validation_file.stat().st_size / (1024*1024):.1f} MB")
    print()
    
    # Generate final statistics
    category_stats = {}
    for example in all_examples:
        category_stats[example.category] = category_stats.get(example.category, 0) + 1
    
    print("📊 FINAL DATASET STATISTICS")
    print("-" * 40)
    print(f"Total Examples: {total_examples:,}")
    print(f"Training Split: {len(training_examples):,} (80%)")
    print(f"Validation Split: {len(validation_examples):,} (20%)")
    print()
    
    print("Category Distribution:")
    for category, count in sorted(category_stats.items()):
        percentage = (count / total_examples) * 100
        print(f"  {category:20s}: {count:4,} ({percentage:4.1f}%)")
    
    print()
    print("🚀 TRAINING SESSION 2 DATASET COMPLETE!")
    print("✅ Ready for Mistral fine-tuning with sophisticated tool orchestration")
    print("✅ Professional hockey analytics with enterprise-grade capabilities")
    print("✅ LangGraph integration preparation complete")
    
    # Generate metadata file
    metadata = {
        "dataset_info": {
            "session_number": 2,
            "created_date": datetime.datetime.now().isoformat(),
            "total_examples": total_examples,
            "training_examples": len(training_examples),
            "validation_examples": len(validation_examples),
            "split_ratio": "80/20"
        },
        "composition": category_stats,
        "target_capabilities": [
            "Tool orchestration mastery with multi-step workflows",
            "Identity-aware role-based response adaptation", 
            "Evidence-based analysis with source attribution",
            "Enterprise error handling and clarification requests",
            "Multi-turn conversation handling with context building"
        ],
        "files": {
            "training": "mistral_training_dataset_session_2.jsonl",
            "validation": "mistral_validation_dataset_session_2.jsonl"
        },
        "base_model": "ft:mistral-large-latest:dd26ff35:20250921:af45b5ef",
        "target_model": "Advanced LangGraph Orchestrator Integration"
    }
    
    metadata_file = output_dir / "session_2_dataset_metadata.json"
    with open(metadata_file, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)
    
    print(f"📋 Metadata: {metadata_file}")

if __name__ == "__main__":
    main()
