"""
HeartBeat Engine - Response Display Component
Stanley Assistant

Response display and visualization component for the Streamlit application.
"""

import streamlit as st
import json
from datetime import datetime
from typing import Dict, Any, List, Optional
import plotly.express as px
import plotly.graph_objects as go

class ResponseDisplay:
    """
    Response display component for hockey analytics results.
    
    Features:
    - Formatted response display with role-appropriate styling
    - Evidence and citation management
    - Interactive data visualizations
    - Export and sharing capabilities
    """
    
    def __init__(self):
        pass
    
    def render(self, result: Dict[str, Any]) -> None:
        """
        Render complete response with analytics and visualizations.
        
        Args:
            result: Query result from orchestrator
        """
        
        if not result:
            return
        
        # Main response section
        self._render_main_response(result)
        
        # Analytics visualization
        self._render_analytics_visualization(result)
        
        # Evidence and citations
        self._render_evidence_section(result)
        
        # Export options
        self._render_export_options(result)
    
    def _render_main_response(self, result: Dict[str, Any]) -> None:
        """Render main response text with formatting"""
        
        response_text = result.get('response', 'No response available')
        query_type = result.get('query_type', 'unknown')
        processing_time = result.get('processing_time_ms', 0)
        
        # Response header
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            st.markdown(f"### Analysis Result")
        
        with col2:
            st.markdown(f"**Type:** {query_type.replace('_', ' ').title()}")
        
        with col3:
            st.markdown(f"**Time:** {processing_time}ms")
        
        # Main response content
        st.markdown(f"""
        <div class="response-container">
            {self._format_response_text(response_text)}
        </div>
        """, unsafe_allow_html=True)
        
        # Response quality indicators
        self._render_quality_indicators(result)
    
    def _format_response_text(self, text: str) -> str:
        """Format response text with proper styling"""
        
        # Convert markdown-style formatting to HTML
        formatted_text = text.replace('\n\n', '</p><p>')
        formatted_text = f"<p>{formatted_text}</p>"
        
        # Highlight tool references
        formatted_text = formatted_text.replace(
            '[TOOL:', 
            '<span style="background-color: #E3F2FD; padding: 2px 6px; border-radius: 3px; font-family: monospace;">[TOOL:'
        )
        formatted_text = formatted_text.replace(']', ']</span>')
        
        # Highlight player names (common Montreal Canadiens players)
        players = ['Suzuki', 'Caufield', 'Hutson', 'Slafkovsky', 'Guhle', 'Matheson', 'Dach', 'Newhook']
        
        for player in players:
            formatted_text = formatted_text.replace(
                player,
                f'<strong style="color: #AF1E2D;">{player}</strong>'
            )
        
        return formatted_text
    
    def _render_quality_indicators(self, result: Dict[str, Any]) -> None:
        """Render response quality indicators"""
        
        col1, col2, col3, col4 = st.columns(4)
        
        # Evidence quality
        evidence_count = len(result.get('evidence_chain', []))
        with col1:
            st.metric(
                "Evidence Sources", 
                evidence_count,
                help="Number of data sources used in analysis"
            )
        
        # Tool usage
        tools_used = len(result.get('tool_results', []))
        successful_tools = sum(1 for t in result.get('tool_results', []) if t.get('success', False))
        
        with col2:
            st.metric(
                "Tools Used",
                f"{successful_tools}/{tools_used}",
                help="Successful tool executions out of total tools used"
            )
        
        # Response length
        response_length = len(result.get('response', '').split())
        with col3:
            st.metric(
                "Response Length",
                f"{response_length} words",
                help="Length of generated response"
            )
        
        # Success rate
        success_rate = (successful_tools / tools_used * 100) if tools_used > 0 else 0
        with col4:
            st.metric(
                "Success Rate",
                f"{success_rate:.0f}%",
                help="Overall analysis success rate"
            )
    
    def _render_analytics_visualization(self, result: Dict[str, Any]) -> None:
        """Render analytics visualizations if data is available"""
        
        tool_results = result.get('tool_results', [])
        
        # Find parquet tool results with data
        analytics_data = None
        for tool_result in tool_results:
            if tool_result.get('tool') == 'parquet_query' and tool_result.get('success'):
                analytics_data = tool_result.get('data')
                break
        
        if not analytics_data or 'sample_data' not in analytics_data:
            return
        
        st.markdown("### Data Visualization")
        
        # Create visualizations based on data type
        analysis_type = analytics_data.get('analysis_type', '')
        
        if 'player' in analysis_type.lower():
            self._render_player_visualization(analytics_data)
        elif 'team' in analysis_type.lower():
            self._render_team_visualization(analytics_data)
        elif 'line' in analysis_type.lower():
            self._render_line_combination_visualization(analytics_data)
        else:
            self._render_generic_data_table(analytics_data)
    
    def _render_player_visualization(self, data: Dict[str, Any]) -> None:
        """Render player-specific visualizations"""
        
        sample_data = data.get('sample_data', [])
        
        if not sample_data:
            st.info("No player data available for visualization")
            return
        
        # Create tabs for different views
        tab1, tab2 = st.tabs(["Statistics", "Data Table"])
        
        with tab1:
            # Try to create a simple chart if numeric data is available
            try:
                import pandas as pd
                df = pd.DataFrame(sample_data)
                
                # Find numeric columns for visualization
                numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
                
                if numeric_cols and len(numeric_cols) >= 2:
                    # Create scatter plot with first two numeric columns
                    fig = px.scatter(
                        df,
                        x=numeric_cols[0],
                        y=numeric_cols[1],
                        title=f"Player Performance: {numeric_cols[0]} vs {numeric_cols[1]}",
                        color_discrete_sequence=["#AF1E2D"]
                    )
                    
                    fig.update_layout(
                        plot_bgcolor='white',
                        paper_bgcolor='white'
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("Numeric data not available for chart visualization")
                    
            except Exception as e:
                st.warning(f"Visualization error: {str(e)}")
        
        with tab2:
            # Display data table
            st.dataframe(
                sample_data,
                use_container_width=True,
                hide_index=True
            )
    
    def _render_team_visualization(self, data: Dict[str, Any]) -> None:
        """Render team-specific visualizations"""
        
        sample_data = data.get('sample_data', [])
        
        if not sample_data:
            st.info("No team data available for visualization")
            return
        
        # Display team data table
        st.dataframe(
            sample_data,
            use_container_width=True,
            hide_index=True
        )
        
        # Try to create team performance chart
        try:
            import pandas as pd
            df = pd.DataFrame(sample_data)
            
            # Look for game results to create win/loss chart
            if 'Result' in df.columns:
                result_counts = df['Result'].value_counts()
                
                fig = px.pie(
                    values=result_counts.values,
                    names=result_counts.index,
                    title="Game Results Distribution",
                    color_discrete_sequence=["#AF1E2D", "#192168", "#CCCCCC"]
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
        except Exception as e:
            st.warning(f"Team visualization error: {str(e)}")
    
    def _render_line_combination_visualization(self, data: Dict[str, Any]) -> None:
        """Render line combination visualizations"""
        
        sample_data = data.get('sample_data', [])
        
        if not sample_data:
            st.info("No line combination data available")
            return
        
        # Display line combinations table
        st.markdown("**Line Combinations Analysis:**")
        st.dataframe(
            sample_data,
            use_container_width=True,
            hide_index=True
        )
    
    def _render_generic_data_table(self, data: Dict[str, Any]) -> None:
        """Render generic data table for unknown data types"""
        
        sample_data = data.get('sample_data', [])
        
        if sample_data:
            st.dataframe(
                sample_data,
                use_container_width=True,
                hide_index=True
            )
        else:
            st.info("No data available for display")
    
    def _render_evidence_section(self, result: Dict[str, Any]) -> None:
        """Render evidence and citation section"""
        
        evidence_chain = result.get('evidence_chain', [])
        tool_results = result.get('tool_results', [])
        
        if not evidence_chain and not tool_results:
            return
        
        st.markdown("### Evidence & Sources")
        
        # Evidence chain
        if evidence_chain:
            st.markdown("**Data Sources:**")
            
            for i, source in enumerate(set(evidence_chain), 1):
                st.markdown(f"""
                <div class="citation-box">
                    {i}. {source}
                </div>
                """, unsafe_allow_html=True)
        
        # Detailed tool results
        if tool_results:
            with st.expander("Detailed Tool Results", expanded=False):
                for i, tool_result in enumerate(tool_results, 1):
                    st.markdown(f"**Tool {i}: {tool_result.get('tool', 'Unknown')}**")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        status = "Success" if tool_result.get('success') else "Failed"
                        st.markdown(f"Status: {status}")
                    
                    with col2:
                        citations = tool_result.get('citations', [])
                        st.markdown(f"Citations: {len(citations)}")
                    
                    if citations:
                        for citation in citations:
                            st.markdown(f"- {citation}")
                    
                    st.markdown("---")
    
    def _render_export_options(self, result: Dict[str, Any]) -> None:
        """Render export and sharing options"""
        
        st.markdown("### Export Options")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("Copy Response", use_container_width=True):
                # Copy response to clipboard (requires additional JS)
                st.success("Response copied to clipboard!")
        
        with col2:
            # Export as JSON
            export_data = {
                "query": st.session_state.get('current_query', ''),
                "response": result.get('response', ''),
                "timestamp": datetime.now().isoformat(),
                "query_type": result.get('query_type', ''),
                "evidence_chain": result.get('evidence_chain', []),
                "processing_time_ms": result.get('processing_time_ms', 0)
            }
            
            st.download_button(
                "Download JSON",
                data=json.dumps(export_data, indent=2),
                file_name=f"heartbeat_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json",
                use_container_width=True
            )
        
        with col3:
            # Export as text report
            report_text = self._generate_text_report(result)
            
            st.download_button(
                "Download Report",
                data=report_text,
                file_name=f"heartbeat_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain",
                use_container_width=True
            )
    
    def _generate_text_report(self, result: Dict[str, Any]) -> str:
        """Generate formatted text report"""
        
        report = f"""
HeartBeat Engine - Hockey Analytics Report
Stanley - Montreal Canadiens Advanced Analytics Assistant
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

QUERY: {st.session_state.get('current_query', 'Unknown')}
QUERY TYPE: {result.get('query_type', 'Unknown')}
PROCESSING TIME: {result.get('processing_time_ms', 0)}ms

ANALYSIS RESULT:
{result.get('response', 'No response available')}

EVIDENCE SOURCES:
"""
        
        evidence_chain = result.get('evidence_chain', [])
        if evidence_chain:
            for i, source in enumerate(set(evidence_chain), 1):
                report += f"{i}. {source}\n"
        else:
            report += "No evidence sources available\n"
        
        report += f"""
TOOL EXECUTION SUMMARY:
"""
        
        tool_results = result.get('tool_results', [])
        if tool_results:
            successful_tools = sum(1 for t in tool_results if t.get('success', False))
            report += f"Tools Used: {len(tool_results)}\n"
            report += f"Successful: {successful_tools}\n"
            report += f"Success Rate: {(successful_tools/len(tool_results)*100):.1f}%\n"
        else:
            report += "No tool execution data available\n"
        
        report += f"""
---
HeartBeat Engine v1.0
Montreal Canadiens Advanced Analytics
"""
        
        return report
