# routes/cali_scripts.py
"""
CALI Scripts API Routes
Provides frontend access to Caleon's scripted response system
"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Dict, Any, Optional, List
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from cali_scripts.engine import CaliScripts

router = APIRouter(prefix="/api/cali-scripts", tags=["cali-scripts"])

# Pydantic models for request/response
class CaliScriptRequest(BaseModel):
    category: str
    entry: str
    variables: Optional[Dict[str, Any]] = None

class CaliScriptResponse(BaseModel):
    script: str
    category: str
    entry: str

class CategoriesResponse(BaseModel):
    categories: List[str]

class EntriesResponse(BaseModel):
    category: str
    entries: List[str]

# Dependency to get CALI Scripts instance
def get_cali_scripts():
    return CaliScripts

@router.post("/", response_model=CaliScriptResponse)
async def get_script(
    request: CaliScriptRequest,
    cali: CaliScripts = Depends(get_cali_scripts)
):
    """
    Get a scripted response from CALI Scripts
    """
    try:
        script = cali.say(request.category, request.entry, **(request.variables or {}))
        return CaliScriptResponse(
            script=script,
            category=request.category,
            entry=request.entry
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Script error: {str(e)}")

@router.get("/categories", response_model=CategoriesResponse)
async def get_categories(cali: CaliScripts = Depends(get_cali_scripts)):
    """
    Get all available script categories
    """
    try:
        categories = cali.get_categories()
        return CategoriesResponse(categories=categories)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Categories error: {str(e)}")

@router.get("/categories/{category}/entries", response_model=EntriesResponse)
async def get_entries(
    category: str,
    cali: CaliScripts = Depends(get_cali_scripts)
):
    """
    Get all entries in a specific category
    """
    try:
        entries = cali.get_entries(category)
        return EntriesResponse(category=category, entries=entries)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Entries error: {str(e)}")

# Convenience endpoints for common categories
@router.post("/greet", response_model=CaliScriptResponse)
async def greet_endpoint(
    request: CaliScriptRequest,
    cali: CaliScripts = Depends(get_cali_scripts)
):
    """Greeting responses"""
    try:
        script = cali.greet(request.entry, **(request.variables or {}))
        return CaliScriptResponse(script=script, category="greetings", entry=request.entry)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Greet error: {str(e)}")

@router.post("/error", response_model=CaliScriptResponse)
async def error_endpoint(
    request: CaliScriptRequest,
    cali: CaliScripts = Depends(get_cali_scripts)
):
    """Error responses"""
    try:
        script = cali.error(request.entry, **(request.variables or {}))
        return CaliScriptResponse(script=script, category="errors", entry=request.entry)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error script error: {str(e)}")

@router.post("/confirm", response_model=CaliScriptResponse)
async def confirm_endpoint(
    request: CaliScriptRequest,
    cali: CaliScripts = Depends(get_cali_scripts)
):
    """Confirmation responses"""
    try:
        script = cali.confirm(request.entry, **(request.variables or {}))
        return CaliScriptResponse(script=script, category="confirmations", entry=request.entry)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Confirm error: {str(e)}")

@router.post("/draft", response_model=CaliScriptResponse)
async def draft_endpoint(
    request: CaliScriptRequest,
    cali: CaliScripts = Depends(get_cali_scripts)
):
    """Draft engine responses"""
    try:
        script = cali.draft(request.entry, **(request.variables or {}))
        return CaliScriptResponse(script=script, category="drafts", entry=request.entry)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Draft error: {str(e)}")

@router.post("/tooltip", response_model=CaliScriptResponse)
async def tooltip_endpoint(
    request: CaliScriptRequest,
    cali: CaliScripts = Depends(get_cali_scripts)
):
    """Tooltip responses"""
    try:
        script = cali.tooltip(request.entry, **(request.variables or {}))
        return CaliScriptResponse(script=script, category="tooltips", entry=request.entry)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Tooltip error: {str(e)}")