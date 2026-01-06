# routes/manuals.py
"""
Manual Generation API Routes
Provides endpoints for creating user manuals, owner's manuals, training manuals, etc.
Separate from book generation functionality
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import Dict, List, Any, Optional
import logging
import uuid
from datetime import datetime

from engines.manual_engine import ManualEngine

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/manuals", tags=["manuals"])

# Initialize manual engine
manual_engine = ManualEngine()

class UserManualRequest(BaseModel):
    product_name: str
    features: List[str]
    instructions: Dict[str, Any]

class OwnerManualRequest(BaseModel):
    product_name: str
    specifications: Dict[str, Any]
    maintenance: Dict[str, Any]

class TrainingManualRequest(BaseModel):
    topic: str
    objectives: List[str]
    content: Dict[str, Any]

class ManualResponse(BaseModel):
    success: bool
    manual_id: str
    manual: Dict[str, Any]
    message: str

@router.post("/user-manual", response_model=ManualResponse)
async def generate_user_manual(request: UserManualRequest, background_tasks: BackgroundTasks) -> ManualResponse:
    """
    Generate a user manual for a product
    """
    try:
        manual = manual_engine.generate_user_manual(
            product_name=request.product_name,
            features=request.features,
            instructions=request.instructions
        )

        manual_id = str(uuid.uuid4())

        return ManualResponse(
            success=True,
            manual_id=manual_id,
            manual=manual,
            message="User manual generated successfully"
        )

    except Exception as e:
        logger.error(f"Failed to generate user manual: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Manual generation failed: {str(e)}")

@router.post("/owner-manual", response_model=ManualResponse)
async def generate_owner_manual(request: OwnerManualRequest, background_tasks: BackgroundTasks) -> ManualResponse:
    """
    Generate an owner's manual for equipment/products
    """
    try:
        manual = manual_engine.generate_owner_manual(
            product_name=request.product_name,
            specifications=request.specifications,
            maintenance=request.maintenance
        )

        manual_id = str(uuid.uuid4())

        return ManualResponse(
            success=True,
            manual_id=manual_id,
            manual=manual,
            message="Owner's manual generated successfully"
        )

    except Exception as e:
        logger.error(f"Failed to generate owner's manual: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Manual generation failed: {str(e)}")

@router.post("/training-manual", response_model=ManualResponse)
async def generate_training_manual(request: TrainingManualRequest, background_tasks: BackgroundTasks) -> ManualResponse:
    """
    Generate a training manual for educational purposes
    """
    try:
        manual = manual_engine.generate_training_manual(
            topic=request.topic,
            objectives=request.objectives,
            content=request.content
        )

        manual_id = str(uuid.uuid4())

        return ManualResponse(
            success=True,
            manual_id=manual_id,
            manual=manual,
            message="Training manual generated successfully"
        )

    except Exception as e:
        logger.error(f"Failed to generate training manual: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Manual generation failed: {str(e)}")

@router.get("/types")
async def get_manual_types() -> Dict[str, Any]:
    """
    Get available manual types and their descriptions
    """
    return {
        "types": {
            "user_manual": {
                "description": "User manuals for products, software, or services",
                "required_fields": ["product_name", "features", "instructions"]
            },
            "owner_manual": {
                "description": "Owner's manuals for equipment, vehicles, or physical products",
                "required_fields": ["product_name", "specifications", "maintenance"]
            },
            "training_manual": {
                "description": "Training manuals for courses, workshops, or educational content",
                "required_fields": ["topic", "objectives", "content"]
            }
        },
        "message": "Manual generation is separate from book creation and focuses on practical, instructional content"
    }