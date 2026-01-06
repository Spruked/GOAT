import json
from typing import Any, Dict
from jsonschema import validate, ValidationError
from cryptography.fernet import Fernet
import datetime

# JSON Schema for project.gproj
GPROJ_SCHEMA = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "GOAT Project File",
    "type": "object",
    "required": [
        "version", "project_id", "created_at", "last_updated", "metadata", "file_map", "structure", "retention", "onboarding", "artifact_goal", "audience", "progress", "encryption", "ucm_context"
    ],
    "properties": {
        "version": {"type": "string", "pattern": "^1\\.0\\.0$"},
        "project_id": {"type": "string"},
        "created_at": {"type": "string", "format": "date-time"},
        "last_updated": {"type": "string", "format": "date-time"},
        "metadata": {
            "type": "object",
            "properties": {
                "title": {"type": "string"},
                "description": {"type": "string"},
                "owner": {"type": "string"},
                "tags": {"type": "array", "items": {"type": "string"}}
            },
            "required": ["title", "owner"]
        },
        "file_map": {
            "type": "object",
            "patternProperties": {
                ".+": {
                    "type": "object",
                    "properties": {
                        "path": {"type": "string"},
                        "type": {"type": "string"},
                        "created": {"type": "string", "format": "date-time"},
                        "size": {"type": "integer"},
                        "hash": {"type": "string"}
                    },
                    "required": ["path", "type", "created", "size", "hash"]
                }
            }
        },
        "structure": {
            "type": "object",
            "properties": {
                "type": {"type": "string", "enum": ["chronological", "thematic", "story_arc", "blueprint", "chapter", "folder", "ai_cluster", "manual"]},
                "tree": {"type": "object"}
            },
            "required": ["type", "tree"]
        },
        "retention": {
            "type": "object",
            "properties": {
                "mode": {"type": "string", "enum": ["temporary", "local", "server", "blockchain"]},
                "purge_on_exit": {"type": "boolean"}
            },
            "required": ["mode"]
        },
        "onboarding": {
            "type": "object",
            "properties": {
                "steps": {"type": "array", "items": {"type": "string"}},
                "completed": {"type": "boolean"},
                "selections": {"type": "object"}
            },
            "required": ["steps", "completed", "selections"]
        },
        "artifact_goal": {"type": "string"},
        "audience": {"type": "string"},
        "progress": {
            "type": "object",
            "properties": {
                "percent": {"type": "number", "minimum": 0, "maximum": 100},
                "last_panel": {"type": "string"},
                "timeline": {"type": "array", "items": {"type": "string"}}
            },
            "required": ["percent"]
        },
        "encryption": {
            "type": "object",
            "properties": {
                "encrypted": {"type": "boolean"},
                "algorithm": {"type": "string"},
                "key_hint": {"type": "string"}
            },
            "required": ["encrypted", "algorithm"]
        },
        "ucm_context": {
            "type": "object",
            "properties": {
                "summary": {"type": "string"},
                "last_interaction": {"type": "string", "format": "date-time"}
            },
            "required": ["summary"]
        }
    }
}

GPROJ_VERSION = "1.0.0"

# Validation helper
def validate_gproj(data: Dict[str, Any]):
    try:
        validate(instance=data, schema=GPROJ_SCHEMA)
    except ValidationError as e:
        raise ValueError(f"project.gproj validation error: {e.message}")

# Encryption helpers
def encrypt_gproj(data: Dict[str, Any], key: bytes) -> bytes:
    raw = json.dumps(data).encode('utf-8')
    f = Fernet(key)
    return f.encrypt(raw)

def decrypt_gproj(data: bytes, key: bytes) -> Dict[str, Any]:
    f = Fernet(key)
    raw = f.decrypt(data)
    return json.loads(raw.decode('utf-8'))

# Factory for new project.gproj
def new_gproj(project_id: str, owner: str, title: str, artifact_goal: str, audience: str, structure_type: str, retention_mode: str, onboarding_selections: Dict[str, Any]) -> Dict[str, Any]:
    now = datetime.datetime.utcnow().isoformat() + 'Z'
    return {
        "version": GPROJ_VERSION,
        "project_id": project_id,
        "created_at": now,
        "last_updated": now,
        "metadata": {
            "title": title,
            "description": "",
            "owner": owner,
            "tags": []
        },
        "file_map": {},
        "structure": {
            "type": structure_type,
            "tree": {}
        },
        "retention": {
            "mode": retention_mode,
            "purge_on_exit": retention_mode == "temporary"
        },
        "onboarding": {
            "steps": [],
            "completed": False,
            "selections": onboarding_selections
        },
        "artifact_goal": artifact_goal,
        "audience": audience,
        "progress": {
            "percent": 0,
            "last_panel": "onboarding",
            "timeline": []
        },
        "encryption": {
            "encrypted": True,
            "algorithm": "fernet",
            "key_hint": "user or session key"
        },
        "ucm_context": {
            "summary": "",
            "last_interaction": now
        }
    }
