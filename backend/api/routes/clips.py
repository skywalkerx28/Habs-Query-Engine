"""
HeartBeat Engine - Video Clips Routes
Montreal Canadiens Advanced Analytics Assistant

API endpoints for serving video clips and thumbnails with role-based access control.
"""

import os
import logging
from pathlib import Path
from typing import Optional
from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.responses import FileResponse, StreamingResponse
from starlette.background import BackgroundTask

from orchestrator.utils.state import UserContext
from orchestrator.models.clip_models import ClipIndexManager, ClipSearchParams
from orchestrator.utils.thumbnail_generator import thumbnail_generator
from ..dependencies import get_current_user_context
from ..models.responses import ClipData

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/clips", tags=["clips"])

# Initialize clip index manager
clips_base_path = os.getenv("CLIPS_BASE_PATH", "data/clips")
clip_index = ClipIndexManager(clips_base_path)

@router.get("/", response_model=list[ClipData])
async def list_clips(
    player_names: Optional[str] = None,
    event_types: Optional[str] = None,
    opponents: Optional[str] = None,
    time_filter: Optional[str] = None,
    limit: int = 10,
    user_context: UserContext = Depends(get_current_user_context)
):
    """
    List available video clips with filtering options.
    
    Query parameters:
    - player_names: Comma-separated player names
    - event_types: Comma-separated event types  
    - opponents: Comma-separated opponent team names
    - time_filter: Time filter (last_game, last_5_games, etc.)
    - limit: Maximum number of clips to return
    """
    
    try:
        # Parse query parameters
        player_list = player_names.split(",") if player_names else []
        event_list = event_types.split(",") if event_types else []
        opponent_list = opponents.split(",") if opponents else []
        
        # Create search parameters
        search_params = ClipSearchParams(
            player_names=player_list,
            event_types=event_list,
            opponents=opponent_list,
            time_filter=time_filter or "",
            limit=min(limit, 50),  # Cap at 50 clips
            user_context=user_context
        )
        
        # Search for clips
        clip_results = await clip_index.search_clips(search_params)
        
        # Convert to API response format
        clips_data = []
        for clip in clip_results:
            clips_data.append(ClipData(
                clip_id=clip.clip_id,
                title=clip.title,
                player_name=clip.player_name,
                game_info=clip.game_info,
                event_type=clip.event_type,
                description=clip.description,
                file_url=clip.file_url,
                thumbnail_url=clip.thumbnail_url,
                duration=clip.duration,
                relevance_score=clip.relevance_score
            ))
        
        logger.info(f"Listed {len(clips_data)} clips for user {user_context.role.value}")
        return clips_data
        
    except Exception as e:
        logger.error(f"Error listing clips: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve clips"
        )

@router.get("/{clip_id}/video")
async def serve_video(
    clip_id: str,
    user_context: UserContext = Depends(get_current_user_context)
):
    """
    Serve a video clip file with access control.
    
    Returns the actual video file for playback.
    """
    
    try:
        # Find the clip metadata
        all_clips = clip_index.discover_clips("2024-2025")  # TODO: Make season dynamic
        clip_metadata = None
        
        for clip in all_clips:
            if clip.clip_id == clip_id:
                clip_metadata = clip
                break
        
        if not clip_metadata:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Clip not found"
            )
        
        # Check user access permissions
        if not _user_can_access_clip(user_context, clip_metadata):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied to this clip"
            )
        
        # Verify file exists
        video_path = Path(clip_metadata.file_path)
        if not video_path.exists():
            logger.error(f"Video file not found: {video_path}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Video file not found"
            )
        
        # Determine content type
        content_type = _get_content_type(video_path.suffix.lower())
        
        logger.info(f"Serving video {clip_id} to user {user_context.role.value}")
        
        # Return video file
        return FileResponse(
            path=str(video_path),
            media_type=content_type,
            filename=f"{clip_metadata.player_name}_{clip_metadata.event_type}.mp4"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error serving video {clip_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to serve video"
        )

@router.get("/{clip_id}/thumbnail")
async def serve_thumbnail(
    clip_id: str,
    user_context: UserContext = Depends(get_current_user_context)
):
    """
    Serve a video thumbnail image.
    
    Returns a thumbnail image for the video clip.
    """
    
    try:
        # Find the clip metadata
        all_clips = clip_index.discover_clips("2024-2025")
        clip_metadata = None
        
        for clip in all_clips:
            if clip.clip_id == clip_id:
                clip_metadata = clip
                break
        
        if not clip_metadata:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Clip not found"
            )
        
        # Check user access permissions
        if not _user_can_access_clip(user_context, clip_metadata):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied to this clip"
            )
        
        # Generate or get existing thumbnail
        thumbnail_path = await thumbnail_generator.generate_thumbnail(
            video_path=clip_metadata.file_path,
            clip_id=clip_id,
            player_name=clip_metadata.player_name,
            event_type=clip_metadata.event_type
        )
        
        if not thumbnail_path or not Path(thumbnail_path).exists():
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to generate thumbnail"
            )
        
        logger.info(f"Serving thumbnail for clip {clip_id}")
        
        return FileResponse(
            path=thumbnail_path,
            media_type="image/jpeg",
            filename=f"thumb_{clip_id}.jpg"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error serving thumbnail {clip_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to serve thumbnail"
        )

@router.get("/{clip_id}/metadata")
async def get_clip_metadata(
    clip_id: str,
    user_context: UserContext = Depends(get_current_user_context)
):
    """
    Get detailed metadata for a specific clip.
    
    Returns comprehensive clip information.
    """
    
    try:
        # Find the clip metadata
        all_clips = clip_index.discover_clips("2024-2025")
        clip_metadata = None
        
        for clip in all_clips:
            if clip.clip_id == clip_id:
                clip_metadata = clip
                break
        
        if not clip_metadata:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Clip not found"
            )
        
        # Check user access permissions
        if not _user_can_access_clip(user_context, clip_metadata):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied to this clip"
            )
        
        # Return detailed metadata
        return {
            "clip_id": clip_metadata.clip_id,
            "player_name": clip_metadata.player_name,
            "game_date": clip_metadata.game_date,
            "opponent": clip_metadata.opponent,
            "event_type": clip_metadata.event_type,
            "description": clip_metadata.description,
            "file_path": clip_metadata.file_path,
            "file_size_mb": clip_metadata.file_size_mb,
            "duration_seconds": clip_metadata.duration_seconds,
            "tags": clip_metadata.tags,
            "created_at": clip_metadata.created_at,
            "indexed_at": clip_metadata.indexed_at
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting metadata for clip {clip_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get clip metadata"
        )

def _user_can_access_clip(user_context: UserContext, clip_metadata) -> bool:
    """Check if user has access to a specific clip"""
    
    # For now, implement basic access control
    # Players can access their own clips and team clips
    # Coaches and staff can access all team clips
    
    from orchestrator.config.settings import UserRole
    
    if user_context.role in [UserRole.COACH, UserRole.ANALYST, UserRole.STAFF, UserRole.SCOUT]:
        return True  # Full access for staff
    
    if user_context.role == UserRole.PLAYER:
        # Players can access their own clips
        user_name = user_context.name.lower().replace(" ", "_")
        clip_player = clip_metadata.player_name.lower().replace(" ", "_")
        return user_name == clip_player
    
    return False  # Default deny

def _get_content_type(file_extension: str) -> str:
    """Get content type for video file"""
    
    content_types = {
        ".mp4": "video/mp4",
        ".mov": "video/quicktime",
        ".avi": "video/x-msvideo",
        ".mkv": "video/x-matroska",
        ".webm": "video/webm"
    }
    
    return content_types.get(file_extension, "application/octet-stream")

