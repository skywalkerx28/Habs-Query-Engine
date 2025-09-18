"""
Hockey Analytics Domain-Specific Prompt Templates for HabsAI
===========================================================

This module contains specialized prompt templates designed to ensure mathematical
accuracy and contextual understanding in hockey analytics queries.

Templates are structured to:
- Provide clear mathematical context
- Define metric relationships and interpretations
- Include domain-specific knowledge
- Ensure consistent terminology usage
- Maintain analytical rigor
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import json

@dataclass
class PromptTemplate:
    """Structured prompt template with metadata"""
    name: str
    template: str
    context_type: str
    required_variables: List[str]
    mathematical_focus: str
    domain_knowledge: str
    validation_rules: List[str]

class HockeyPromptManager:
    """Manages hockey-specific prompt templates for accurate LLM responses"""

    def __init__(self):
        self.templates = self._load_templates()
        self.metric_definitions = self._load_metric_definitions()

    def _load_metric_definitions(self) -> Dict[str, Dict[str, Any]]:
        """Load comprehensive metric definitions for context injection"""
        return {
            "expected_goals": {
                "definition": "Expected Goals (xG) measures the quality of scoring opportunities based on shot location, type, and game situation",
                "interpretation": "Higher xG indicates better quality chances. Actual goals vs xG shows finishing efficiency",
                "calculation": "Based on historical conversion rates for similar shots",
                "units": "Goals per game or per 60 minutes",
                "context": "xG > actual goals = underperforming expectations, xG < actual goals = overperforming expectations",
                "player_lingo": "Quality of shots - are we getting good looks or just volume?"
            },

            "corsi": {
                "definition": "Corsi measures puck possession through shot attempts (shots + misses + blocks)",
                "interpretation": "Higher Corsi indicates better puck possession and territorial advantage",
                "calculation": "Total shot attempts for / (shot attempts for + shot attempts against)",
                "units": "Percentage or raw count per 60 minutes",
                "context": "Corsi is a proxy for puck possession in the offensive zone"
            },

            "pdo": {
                "definition": "PDO combines shooting percentage and save percentage (SHOOTING% + SAVE% * 100)",
                "interpretation": "PDO around 100 is league average. Values significantly above/below suggest regression to mean",
                "calculation": "(Goals / Shots) + (Saves / Shots Against) * 100",
                "units": "Index value (typically 95-105 range)",
                "context": "PDO measures luck/randomness in shooting and goaltending"
            },

            "zone_starts": {
                "definition": "Percentage of faceoffs taken in offensive zone vs defensive zone",
                "interpretation": "Higher percentage indicates favorable puck possession situations",
                "calculation": "Offensive zone faceoffs / total faceoffs",
                "units": "Percentage",
                "context": "Teams with poor zone starts work harder to generate offense"
            },

            "high_danger_scoring": {
                "definition": "Goals scored from high-quality scoring areas (slot, crease, etc.)",
                "interpretation": "Higher percentage indicates better finishing in prime scoring areas",
                "calculation": "Goals from high-danger areas / total goals",
                "units": "Percentage",
                "context": "Elite teams excel at converting high-danger chances"
            }
        }

    def _load_templates(self) -> Dict[str, PromptTemplate]:
        """Load all hockey analytics prompt templates"""
        return {
            "performance_analysis": PromptTemplate(
                name="performance_analysis",
                template="""
You are a hockey analytics expert analyzing Montreal Canadiens performance data.

CONTEXT:
- Team: Montreal Canadiens (MTL)
- Season: {season}
- Analysis Type: {analysis_type}
- Data Quality Score: {data_quality}/100

METRICS CONTEXT:
{metric_definitions}

DATA TO ANALYZE:
{data_context}

QUESTION: {user_query}

ANALYSIS REQUIREMENTS:
1. MATHEMATICAL ACCURACY: All calculations must be mathematically sound
2. CONTEXT AWARENESS: Consider game situation, opponent strength, and season context
3. STATISTICAL RIGOR: Use appropriate statistical concepts (correlation, regression to mean, etc.)
4. DOMAIN KNOWLEDGE: Apply hockey-specific strategic understanding
5. UNCERTAINTY QUANTIFICATION: Express confidence levels and uncertainty ranges

RESPONSE STRUCTURE:
1. **Key Findings**: Main performance insights with mathematical justification
2. **Contextual Analysis**: How results compare to league norms and expectations
3. **Strategic Implications**: What this means for team strategy and decision-making
4. **Data Quality Notes**: Any limitations or caveats in the analysis
5. **Recommendations**: Actionable insights based on the data

Remember: Higher values are generally better unless specified as "against" metrics.
Percentages are out of 100. Time-based metrics are in seconds.
""",
                context_type="performance_analysis",
                required_variables=["season", "analysis_type", "data_quality", "metric_definitions", "data_context", "user_query"],
                mathematical_focus="statistical analysis, performance metrics, comparative analysis",
                domain_knowledge="NHL team performance, hockey strategy, advanced analytics",
                validation_rules=[
                    "All numerical comparisons must be mathematically accurate",
                    "Statistical claims must be supported by data",
                    "Context must be preserved across analysis",
                    "Domain terminology must be used correctly"
                ]
            ),

            "xg_analysis": PromptTemplate(
                name="xg_analysis",
                template="""
You are analyzing Montreal Canadiens Expected Goals (xG) performance with mathematical precision.

XG FUNDAMENTALS:
- Expected Goals measure scoring opportunity quality based on shot location, type, and situation
- xG is calculated using historical conversion rates for similar shots
- Actual Goals vs xG shows finishing efficiency (finishing % = actual goals / xG)
- Positive values in "Actual vs Expected" indicate overperforming expectations

PERFORMANCE SPLIT ANALYSIS:
The data shows performance in three contexts:
- "Below": When Montreal's ES Expected Goals For % < 50% (being out-produced by opponents)
- "Average": Overall performance across all game situations
- "Above": When Montreal's ES Expected Goals For % > 50% (out-producing opponents)

DATA CONTEXT:
{data_summary}

QUESTION: {user_query}

MATHEMATICAL ANALYSIS REQUIREMENTS:
1. Calculate finishing percentages: (Actual Goals / Expected Goals) × 100
2. Compare performance across different game states
3. Identify efficiency patterns and strategic implications
4. Quantify the impact of game situation on performance

RESPONSE STRUCTURE:
1. **XG Efficiency Analysis**: Actual vs expected performance with calculations
2. **Game State Impact**: How performance varies by XG advantage/disadvantage
3. **Strategic Insights**: What the numbers reveal about team strategy
4. **Mathematical Validation**: Confirm all calculations are sound
""",
                context_type="xg_analysis",
                required_variables=["data_summary", "user_query"],
                mathematical_focus="expected goals calculations, efficiency metrics, performance ratios",
                domain_knowledge="advanced hockey analytics, expected goals methodology",
                validation_rules=[
                    "All xG calculations must be mathematically accurate",
                    "Finishing percentages must be correctly calculated",
                    "Performance splits must be clearly distinguished",
                    "Statistical significance should be considered"
                ]
            ),

            "comparative_analysis": PromptTemplate(
                name="comparative_analysis",
                template="""
You are conducting a comparative analysis between Montreal Canadiens and other NHL teams.

COMPARATIVE FRAMEWORK:
- Rankings: 1 = best in NHL, 32 = worst in NHL
- League Median: Represents average NHL team performance
- Percentiles: Position relative to all 32 NHL teams
- Context: Home/away splits, opponent quality, game situation

STATISTICAL CONSIDERATIONS:
- Small sample sizes reduce statistical reliability
- PDO values significantly above/below 100 suggest regression to mean
- Expected Goals provide more stable performance indicators than actual goals
- Corsi and Fenwick are better possession indicators than goals for/against

COMPARISON DATA:
{comparison_data}

QUESTION: {user_query}

ANALYSIS FRAMEWORK:
1. **Relative Performance**: Montreal's ranking and percentile in each metric
2. **Strengths Identification**: Metrics where Montreal ranks in top 10 NHL
3. **Weaknesses Identification**: Metrics where Montreal ranks in bottom 10 NHL
4. **Contextual Factors**: Consider schedule strength, goaltending, injuries
5. **Trend Analysis**: How performance has changed over time

VALIDATION REQUIREMENTS:
- All rankings must be mathematically accurate
- Statistical significance must be considered for small samples
- Contextual factors must be properly weighted
- Uncertainty must be quantified where appropriate
""",
                context_type="comparative_analysis",
                required_variables=["comparison_data", "user_query"],
                mathematical_focus="ranking systems, percentile calculations, statistical comparisons",
                domain_knowledge="NHL team comparisons, league context, performance evaluation",
                validation_rules=[
                    "All rankings must be verified against source data",
                    "Percentile calculations must be mathematically correct",
                    "Statistical significance must be properly assessed",
                    "Contextual factors must be appropriately considered"
                ]
            ),

            "predictive_analysis": PromptTemplate(
                name="predictive_analysis",
                template="""
You are providing predictive analytics for Montreal Canadiens performance using mathematical modeling.

PREDICTIVE FRAMEWORK:
- Regression Analysis: Identify relationships between metrics and outcomes
- Trend Extrapolation: Project future performance based on current trajectories
- Probability Assessment: Quantify likelihood of different outcomes
- Confidence Intervals: Express uncertainty in predictions

STATISTICAL METHODOLOGY:
- Correlation Analysis: Identify relationships between performance metrics
- Time Series Analysis: Track performance trends over the season
- Regression to Mean: Account for PDO and luck-based metrics
- Sample Size Considerations: Weight recent performance appropriately

PREDICTIVE FACTORS:
{performance_factors}

QUESTION: {user_query}

PREDICTION STRUCTURE:
1. **Current Performance Baseline**: Establish current metrics and trends
2. **Statistical Projections**: Use mathematical models to project future performance
3. **Key Variables**: Identify most important predictive factors
4. **Uncertainty Quantification**: Express confidence levels and ranges
5. **Scenario Analysis**: Consider best/worst case outcomes

VALIDATION REQUIREMENTS:
- All predictions must be grounded in statistical evidence
- Uncertainty must be properly quantified
- Assumptions must be clearly stated
- Confidence intervals must be mathematically sound
""",
                context_type="predictive_analysis",
                required_variables=["performance_factors", "user_query"],
                mathematical_focus="regression analysis, probability calculations, trend extrapolation",
                domain_knowledge="performance prediction, statistical modeling, NHL trends",
                validation_rules=[
                    "All statistical models must be mathematically sound",
                    "Predictions must be based on historical data relationships",
                    "Uncertainty must be properly quantified",
                    "Assumptions must be clearly documented"
                ]
            ),

            "strategic_recommendations": PromptTemplate(
                name="strategic_recommendations",
                template="""
You are providing strategic recommendations for the Montreal Canadiens based on mathematical analysis.

STRATEGIC FRAMEWORK:
- Line Optimization: Mathematical analysis of line combinations and chemistry
- Tactical Adjustments: Zone entry/exit strategies based on performance data
- Player Deployment: Optimal usage patterns based on performance metrics
- Game State Management: When to be aggressive vs conservative

ANALYTICAL APPROACH:
- Efficiency Analysis: Goals per minute, Corsi per 60 minutes
- Opportunity Cost: Trade-offs between different strategic approaches
- Risk Assessment: Mathematical evaluation of strategic risk/reward
- Competitive Advantage: Identify strategic edges over opponents

PERFORMANCE CONTEXT:
{strategic_context}

QUESTION: {user_query}

RECOMMENDATION STRUCTURE:
1. **Performance Diagnosis**: Identify key strengths and weaknesses mathematically
2. **Strategic Opportunities**: Areas where data suggests strategic improvements
3. **Tactical Recommendations**: Specific adjustments based on performance analysis
4. **Implementation Priority**: Rank recommendations by potential impact
5. **Success Metrics**: How to measure the effectiveness of implemented changes

VALIDATION REQUIREMENTS:
- All recommendations must be supported by mathematical evidence
- Risk/reward analysis must be quantitatively sound
- Implementation feasibility must be considered
- Success metrics must be measurable and objective
""",
                context_type="strategic_recommendations",
                required_variables=["strategic_context", "user_query"],
                mathematical_focus="efficiency calculations, risk assessment, optimization analysis",
                domain_knowledge="hockey strategy, tactical analysis, team management",
                validation_rules=[
                    "All recommendations must be data-driven",
                    "Mathematical justification must be provided",
                    "Risk/reward analysis must be quantitative",
                    "Implementation considerations must be realistic"
                ]
            ),

            "player_focused_analysis": PromptTemplate(
                name="player_focused_analysis",
                template="""
You are a hockey analytics expert talking directly to Montreal Canadiens players about their performance.

PLAYER PERSPECTIVE FRAMEWORK:
- Ice Time & Opportunity: How much you're playing and in what situations
- Offensive Contribution: Your role in creating and finishing scoring chances
- Defensive Impact: Your contribution to team defense and puck possession
- Physical Play: Board battles, puck battles, and physical engagement
- Game State Performance: How you perform when winning vs losing

HOCKEY PLAYER LINGO & CONTEXT:
- "Good looks" = Quality scoring opportunities
- "Heavy shots" = Hard, accurate shots
- "Gordie Howe hat trick" = Goal + Assist + Fight in same game
- "D-zone coverage" = Defensive zone positioning and responsibility
- "Gap control" = Distance between you and opponent when forechecking
- "Puck possession" = Controlling the puck vs chasing it
- "Board battles" = Physical battles along the boards for puck control
- "Slot shots" = Shots from the high-danger scoring area
- "Odd-man rushes" = Breakaways or 2-on-1 opportunities

PLAYER PERFORMANCE CONTEXT:
{player_context}

QUESTION: {user_query}

PLAYER-FOCUSED ANALYSIS STRUCTURE:
1. **Your Role & Ice Time**: How much you're playing and in what situations
2. **Offensive Impact**: Your contribution to scoring and chance creation
3. **Defensive Contribution**: Your impact on preventing opponent chances
4. **Physical Play**: Your physical engagement and battles won
5. **Strengths to Lean On**: What you're doing well
6. **Areas to Work On**: Specific improvements with actionable advice
7. **Motivational Takeaway**: Encouraging message based on your performance

VALIDATION REQUIREMENTS:
- Use authentic hockey player language and terminology
- Focus on actionable insights players can control
- Provide specific, measurable improvement suggestions
- Include motivational context and encouragement
- Frame analysis in terms of player impact and contribution
""",
                context_type="player_focused_analysis",
                required_variables=["player_context", "user_query"],
                mathematical_focus="individual performance metrics, ice time analysis, contribution calculations",
                domain_knowledge="player performance, hockey psychology, individual development",
                validation_rules=[
                    "Use authentic hockey player terminology",
                    "Focus on player-controllable aspects",
                    "Include specific, actionable feedback",
                    "Maintain motivational and encouraging tone",
                    "Frame analysis from player's perspective"
                ]
            ),

            "coach_player_communication": PromptTemplate(
                name="coach_player_communication",
                template="""
You are translating complex hockey analytics into coach-to-player communication that motivates and educates.

COACH-TO-PLAYER COMMUNICATION STYLE:
- Direct but encouraging language
- Focus on controllable aspects
- Use hockey metaphors and analogies
- Explain "why" behind the numbers
- Connect individual performance to team success
- Provide specific, actionable improvement steps

HOCKEY COACH LINGO EXAMPLES:
- "Battle harder" = Increase physical engagement in puck battles
- "Close the gap" = Reduce distance to opponent when forechecking
- "Support the play" = Position yourself to provide passing options
- "Own your zone" = Take responsibility for defensive coverage
- "Find the soft spot" = Exploit opponent's defensive weaknesses
- "Win the 1-on-1 battle" = Beat your direct opponent in individual confrontations

PERFORMANCE DATA CONTEXT:
{performance_data}

QUESTION: {user_query}

COACH-TO-PLAYER RESPONSE STRUCTURE:
1. **The Good Stuff**: Start with what you're doing well (builds confidence)
2. **The Data Says**: Explain key metrics in simple, relatable terms
3. **The Why Factor**: Connect the numbers to actual game impact
4. **The Action Plan**: 2-3 specific, controllable improvements
5. **The Motivation**: Why this matters for you and the team
6. **The Next Steps**: What to focus on in practice and games

VALIDATION REQUIREMENTS:
- Use coach-like direct but encouraging communication
- Translate analytics into actionable hockey concepts
- Focus on player development and motivation
- Connect individual performance to team success
- Provide specific, measurable improvement targets
""",
                context_type="coach_player_communication",
                required_variables=["performance_data", "user_query"],
                mathematical_focus="simplified performance metrics, trend analysis, goal setting",
                domain_knowledge="player coaching, motivation, team dynamics",
                validation_rules=[
                    "Use coach-like communication style",
                    "Translate complex analytics into simple concepts",
                    "Focus on motivation and development",
                    "Provide actionable improvement steps",
                    "Connect individual to team performance"
                ]
            )
        }

    def get_template(self, template_name: str, **variables) -> str:
        """Get a formatted template with variables filled in"""
        if template_name not in self.templates:
            raise ValueError(f"Template '{template_name}' not found")

        template = self.templates[template_name]

        # Check required variables
        missing_vars = set(template.required_variables) - set(variables.keys())
        if missing_vars:
            raise ValueError(f"Missing required variables: {missing_vars}")

        # Format the template
        formatted_template = template.template.format(**variables)

        return formatted_template

    def get_metric_context(self, metric_name: str) -> Optional[Dict[str, Any]]:
        """Get detailed context for a specific metric"""
        # Try exact match first
        if metric_name in self.metric_definitions:
            return self.metric_definitions[metric_name]

        # Try partial match
        for key, definition in self.metric_definitions.items():
            if key.lower() in metric_name.lower() or any(term in metric_name.lower() for term in key.split('_')):
                return definition

        return None

    def generate_metric_definitions_text(self, metrics: List[str]) -> str:
        """Generate formatted metric definitions text for prompt injection"""
        definitions = []

        for metric in metrics:
            context = self.get_metric_context(metric)
            if context:
                definition_text = f"""
{metric}:
- Definition: {context['definition']}
- Interpretation: {context['interpretation']}
- Units: {context['units']}
- Context: {context['context']}
"""
                definitions.append(definition_text)

        return "\n".join(definitions)

    def create_context_enriched_prompt(self,
                                     template_name: str,
                                     user_query: str,
                                     data_context: Dict[str, Any],
                                     additional_context: Optional[Dict[str, Any]] = None) -> str:
        """Create a fully enriched prompt with all necessary context"""

        template = self.templates[template_name]

        # Prepare variables
        variables = {
            "user_query": user_query,
            "season": data_context.get("season", "2024-25"),
            "analysis_type": data_context.get("analysis_type", "comprehensive"),
            "data_quality": data_context.get("data_quality", 95),
            "data_context": json.dumps(data_context, indent=2),
            "data_summary": json.dumps(data_context.get("summary", {}), indent=2),
            "comparison_data": json.dumps(data_context.get("comparisons", {}), indent=2),
            "performance_factors": json.dumps(data_context.get("factors", {}), indent=2),
            "strategic_context": json.dumps(data_context.get("strategy", {}), indent=2),
            "player_context": json.dumps(data_context.get("player_data", {}), indent=2),
            "performance_data": json.dumps(data_context.get("performance_data", {}), indent=2)
        }

        # Add metric definitions
        metrics = data_context.get("metrics", [])
        variables["metric_definitions"] = self.generate_metric_definitions_text(metrics)

        # Add additional context if provided
        if additional_context:
            variables.update(additional_context)

        return self.get_template(template_name, **variables)

    def detect_query_perspective(self, query: str) -> str:
        """Detect whether query is from player or coach perspective"""

        player_indicators = [
            "my performance", "my ice time", "my shots", "my assists",
            "i'm", "me", "my gap control", "my positioning",
            "how am i doing", "what can i improve", "my battles",
            "am i getting", "my offensive zone time"
        ]

        coach_indicators = [
            "team performance", "line chemistry", "system", "tactics",
            "strategic", "deployment", "optimization", "coaching",
            "bench", "line combinations", "power play setup"
        ]

        query_lower = query.lower()

        player_score = sum(1 for indicator in player_indicators if indicator in query_lower)
        coach_score = sum(1 for indicator in coach_indicators if indicator in query_lower)

        if player_score > coach_score:
            return "player_focused_analysis"
        elif coach_score > player_score:
            return "coach_player_communication"
        else:
            return "performance_analysis"  # Default fallback

    def get_player_lingo_examples(self) -> Dict[str, List[str]]:
        """Get examples of authentic hockey player lingo and terminology"""

        return {
            "scoring_opportunities": [
                "Getting good looks from the slot",
                "Heavy shots from the point",
                "Finding the soft spot in coverage",
                "Creating space for one-timers"
            ],

            "defensive_play": [
                "Owning your zone in the D",
                "Winning board battles",
                "Gap control on the forecheck",
                "Supporting the play from behind"
            ],

            "physical_play": [
                "Finishing checks along the boards",
                "Winning puck battles in the corners",
                "Battle harder in front of the net",
                "Boxing out in the crease"
            ],

            "performance_feedback": [
                "You're getting quality ice time in key situations",
                "Your gap control is solid - keep closing that distance",
                "You're winning more battles than you're losing",
                "Your positioning gives you good puck support angles"
            ],

            "player_queries": [
                "Coach, am I getting enough offensive zone starts?",
                "How's my gap control looking out there?",
                "Am I winning my board battles?",
                "What's my ice time like compared to last game?",
                "How are my shots looking - getting good looks?",
                "Am I supporting the play well from my position?"
            ]
        }

    def add_player_terminology(self, term: str, definition: str, player_lingo: str = ""):
        """Add custom player terminology to the system"""

        if term not in self.metric_definitions:
            self.metric_definitions[term] = {
                "definition": definition,
                "player_lingo": player_lingo,
                "context": "Player-specific terminology",
                "interpretation": "Player perspective on performance",
                "units": "N/A",
                "calculation": "Qualitative assessment"
            }

    def create_player_example_response(self, query_type: str, player_name: str = "Player") -> str:
        """Create example responses showing authentic player communication"""

        examples = {
            "gap_control": f"""
Hey {player_name}, looking at your gap control data - you're maintaining about 2.1 meters of distance on average,
which is solid. That's giving you good reaction time to engage or disengage. Keep working on closing that gap against offenders
as much as possible, trust your feet. The data shows when you gap is tighter,
you're consequentially reducing the amount of time your team is spending in their own zone.
""",

            "ice_time": f"""
{player_name}, you're averaging 14:32 per game this season, which puts you in a good spot for offensive contribution.
You're getting 62% of your minutes at even strength and 58% on the power play - that's quality ice time.
The analytics show you're most effective between minutes 12-18 of each period, so keep pushing for that rhythm.
""",

            "board_battles": f"""
The numbers show you're winning 54% of your board battles, which is above average for your position.
You're particularly strong along the left side boards (62% win rate) but could work on your right side technique.
Focus on getting lower in your stance and using your body position to shield the puck better.
"""
        }

        return examples.get(query_type, "Custom analysis based on your performance data would go here.")

    def validate_player_authenticity(self, response: str) -> Dict[str, Any]:
        """Validate that response uses authentic player language"""

        validation = {
            "authentic_terms_used": 0,
            "coach_speak_detected": 0,
            "player_perspective_score": 0,
            "recommendations": []
        }

        player_terms = [
            "good looks", "heavy shots", "gap control", "board battles",
            "puck battles", "own your zone", "support the play",
            "close the gap", "battle harder", "slot shots", "odd-man rush"
        ]

        coach_terms = [
            "optimization", "efficiency metrics", "correlation analysis",
            "statistical significance", "performance indicators",
            "deployment strategy", "line chemistry analysis"
        ]

        response_lower = response.lower()

        for term in player_terms:
            if term in response_lower:
                validation["authentic_terms_used"] += 1

        for term in coach_terms:
            if term in response_lower:
                validation["coach_speak_detected"] += 1

        # Calculate player perspective score
        total_terms = validation["authentic_terms_used"] + validation["coach_speak_detected"]
        if total_terms > 0:
            validation["player_perspective_score"] = validation["authentic_terms_used"] / total_terms

        # Generate recommendations
        if validation["authentic_terms_used"] < 3:
            validation["recommendations"].append("Add more authentic hockey player terminology")

        if validation["coach_speak_detected"] > 2:
            validation["recommendations"].append("Reduce analytical jargon, use more player-friendly language")

        if validation["player_perspective_score"] < 0.6:
            validation["recommendations"].append("Frame analysis from player's perspective, not just numbers")

        return validation

def main():
    """Example usage of the prompt manager with player-focused features"""
    manager = HockeyPromptManager()

    print("HabsAI Hockey Prompt Templates - Player-Focused Demo")
    print("=" * 60)

    # Demonstrate query perspective detection
    print("\n1. Query Perspective Detection:")
    player_queries = [
        "How's my gap control looking?",
        "Am I winning my board battles?",
        "What's my ice time like this season?"
    ]

    coach_queries = [
        "What's the team's line chemistry?",
        "How should we optimize our power play?",
        "What's our strategic deployment?"
    ]

    for query in player_queries + coach_queries:
        perspective = manager.detect_query_perspective(query)
        query_type = "Player" if "player" in perspective else "Coach"
        print(f"  '{query}' → {query_type} perspective ({perspective})")

    # Demonstrate player lingo examples
    print("\n2. Player Lingo Examples:")
    lingo_examples = manager.get_player_lingo_examples()

    for category, examples in lingo_examples.items():
        print(f"\n  {category.replace('_', ' ').title()}:")
        for example in examples[:2]:  # Show first 2 examples
            print(f"    • {example}")

    # Demonstrate player-focused prompt generation
    print("\n3. Player-Focused Prompt Generation:")

    player_data_context = {
        "season": "2024-25",
        "player_data": {
            "name": "Alex",
            "position": "Forward",
            "ice_time": "14:32",
            "gap_control": "2.1 meters",
            "board_battles": "54% win rate"
        },
        "metrics": ["gap_control", "board_battles", "ice_time"]
    }

    player_prompt = manager.create_context_enriched_prompt(
        "player_focused_analysis",
        "How's my gap control and board battles looking?",
        player_data_context
    )

    print("\n  Generated Player-Focused Prompt:")
    print("  " + "=" * 40)
    print("  " + player_prompt.replace("\n", "\n  ")[:500] + "...")

    # Demonstrate example player responses
    print("\n4. Example Player Responses:")

    response_types = ["gap_control", "ice_time", "board_battles"]
    for resp_type in response_types:
        example = manager.create_player_example_response(resp_type, "Alex")
        print(f"\n  {resp_type.replace('_', ' ').title()}:")
        print(f"    {example.strip()[:100]}...")

    # Demonstrate authenticity validation
    print("\n5. Authenticity Validation:")

    authentic_response = """
    Alex, you're maintaining about 2.1 meters of gap control which is solid.
    That gives you good reaction time. Keep working on closing that gap to win more puck battles.
    """

    validation = manager.validate_player_authenticity(authentic_response)

    print(f"Authentic terms used: {validation['authentic_terms_used']}")
    print(f"Coach speak detected: {validation['coach_speak_detected']}")
    print(f"Player perspective score: {validation['player_perspective_score']:.1f}")

    print("\n6. Adding Custom Player Terminology:")

    # Add custom terminology
    manager.add_player_terminology(
        "crease_crashes",
        "Aggressive net-front presence to screen goalie and create rebounds",
        "Battle harder in front of the net"
    )

    print("Added 'crease_crashes' terminology")
    print("Player lingo: 'Battle harder in front of the net'")

    print("\n" + "=" * 60)
    print("Player-focused features are ready for your HabsAI system!")
    print("Use these to create authentic, relatable hockey conversations.")

if __name__ == "__main__":
    main()
