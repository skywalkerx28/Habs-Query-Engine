"""
HeartBeat Engine - Query Routes
Montreal Canadiens Advanced Analytics Assistant

Main query endpoints that integrate with the LangGraph orchestrator.
"""

from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.responses import StreamingResponse
import asyncio
import logging
import json
from datetime import datetime
from typing import Dict, Any, AsyncGenerator

from orchestrator.utils.state import UserContext
from ..models.requests import QueryRequest
from ..models.responses import QueryResponse, ErrorResponse, AnalyticsData, ToolResult, ClipData
from ..dependencies import get_current_user_context, get_orchestrator

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/query", tags=["query"])

@router.post("/", response_model=QueryResponse)
async def process_query(
    request: QueryRequest,
    user_context: UserContext = Depends(get_current_user_context),
    orchestrator = Depends(get_orchestrator)
):
    """
    Process a hockey analytics query using the LangGraph orchestrator.
    
    This endpoint:
    1. Takes a natural language hockey question
    2. Routes it through the existing LangGraph orchestrator
    3. Returns structured response with analytics data
    """
    
    start_time = datetime.now()
    
    try:
        logger.info(f"Processing query from {user_context.role.value}: {request.query[:100]}...")
        
        # Process query through existing orchestrator
        orchestrator_result = await orchestrator.process_query(
            query=request.query,
            user_context=user_context
        )
        
        # Convert orchestrator result to API response format
        response = _convert_orchestrator_result(orchestrator_result, user_context, start_time)
        
        logger.info(f"Query processed successfully in {response.processing_time_ms}ms")
        return response
        
    except Exception as e:
        logger.error(f"Error processing query: {str(e)}")
        processing_time = int((datetime.now() - start_time).total_seconds() * 1000)
        
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "success": False,
                "error": "Query processing failed",
                "processing_time_ms": processing_time,
                "timestamp": datetime.now().isoformat()
            }
        )

@router.post("/stream")
async def stream_query(
    request: QueryRequest,
    user_context: UserContext = Depends(get_current_user_context),
    orchestrator = Depends(get_orchestrator)
):
    """
    Stream query response for real-time updates.
    
    Returns Server-Sent Events (SSE) for real-time response streaming.
    """
    
    async def generate_response() -> AsyncGenerator[str, None]:
        """Generate streaming response"""
        
        try:
            # Send initial status
            yield f"data: {json.dumps({'type': 'status', 'message': 'Processing query...'})}\n\n"
            
            # Process query through orchestrator
            result = await orchestrator.process_query(
                query=request.query,
                user_context=user_context
            )
            
            # Send partial results as they become available
            if "tool_results" in result:
                for tool_result in result["tool_results"]:
                    yield f"data: {json.dumps({'type': 'tool_result', 'data': tool_result})}\n\n"
            
            # Send final response
            final_response = _convert_orchestrator_result(result, user_context, datetime.now())
            yield f"data: {json.dumps({'type': 'final_response', 'data': final_response.dict()})}\n\n"
            
        except Exception as e:
            logger.error(f"Streaming error: {str(e)}")
            error_data = {
                "type": "error", 
                "message": "Query processing failed",
                "error": str(e)
            }
            yield f"data: {json.dumps(error_data)}\n\n"
    
    return StreamingResponse(
        generate_response(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        }
    )

def _convert_orchestrator_result(
    orchestrator_result: Dict[str, Any], 
    user_context: UserContext,
    start_time: datetime
) -> QueryResponse:
    """Convert orchestrator result to API response format"""
    
    processing_time = int((datetime.now() - start_time).total_seconds() * 1000)
    
    # Extract tool results if available
    tool_results = []
    if "tool_results" in orchestrator_result:
        for result in orchestrator_result["tool_results"]:
            tool_results.append(ToolResult(
                tool=result.get("tool", "unknown"),
                success=result.get("success", False),
                data=result.get("data"),
                processing_time_ms=result.get("processing_time_ms", 0),
                citations=result.get("citations", []),
                error=result.get("error")
            ))
    
    # Create analytics data for frontend (if available)
    analytics = []
    if "analytics" in orchestrator_result:
        for item in orchestrator_result["analytics"]:
            analytics.append(AnalyticsData(
                type=item.get("type", "stat"),
                title=item.get("title", "Analysis"),
                data=item.get("data", {}),
                metadata=item.get("metadata", {}),
                clips=item.get("clips")
            ))
    
    # Check for clip data in tool results and add to analytics
    for result in tool_results:
        if hasattr(result, 'tool') and result.tool == "clip_retrieval" and result.success:
            clip_data = result.data or {}
            clips_list = clip_data.get("clips", [])
            
            if clips_list:
                # Convert clip dictionaries to ClipData models
                clips_models = []
                for clip_dict in clips_list:
                    clips_models.append(ClipData(
                        clip_id=clip_dict.get("clip_id", ""),
                        title=clip_dict.get("title", ""),
                        player_name=clip_dict.get("player_name", ""),
                        game_info=clip_dict.get("game_info", ""),
                        event_type=clip_dict.get("event_type", ""),
                        description=clip_dict.get("description", ""),
                        file_url=clip_dict.get("file_url", ""),
                        thumbnail_url=clip_dict.get("thumbnail_url", ""),
                        duration=clip_dict.get("duration", 0.0),
                        relevance_score=clip_dict.get("relevance_score", 1.0)
                    ))
                
                # Add clips as analytics data
                analytics.append(AnalyticsData(
                    type="clips",
                    title=f"Video Highlights ({len(clips_models)} clips)",
                    data={"total_clips": len(clips_models)},
                    clips=clips_models
                ))
    
    # Build response
    return QueryResponse(
        success=orchestrator_result.get("success", True),
        response=orchestrator_result.get("response", ""),
        query_type=orchestrator_result.get("query_type"),
        tool_results=tool_results,
        processing_time_ms=orchestrator_result.get("processing_time_ms", processing_time),
        evidence=orchestrator_result.get("evidence_chain", []),
        citations=_extract_all_citations(tool_results),
        analytics=analytics,
        user_role=user_context.role.value,
        timestamp=datetime.now(),
        errors=orchestrator_result.get("errors", []),
        warnings=orchestrator_result.get("warnings", [])
    )

def _extract_all_citations(tool_results: list) -> list:
    """Extract all citations from tool results"""
    citations = []
    for result in tool_results:
        citations.extend(result.citations)
    return list(set(citations))  # Remove duplicates
