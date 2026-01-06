# Example: Integrating CALI Scripts into GOAT

"""
Example showing how to integrate Caleon Scripted Response System
into existing GOAT FastAPI endpoints and React frontend.
"""

# backend/server/main.py (or wherever your FastAPI app is)
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from cali_scripts.engine import CaliScripts

app = FastAPI(title="GOAT Platform")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Example endpoints using CALI Scripts
@app.get("/")
async def root():
    """Root endpoint with Caleon greeting."""
    return {
        "message": CaliScripts.greet("first_time"),
        "status": "online"
    }

@app.get("/dashboard")
async def dashboard(user_name: str = "User"):
    """Dashboard welcome with personalization."""
    return {
        "welcome": CaliScripts.greet("welcome_dashboard", name=user_name),
        "status": "ready"
    }

@app.post("/draft/start")
async def start_draft(project_type: str = "book"):
    """Start draft process."""
    if project_type == "book":
        response = CaliScripts.say("goat_builder", "book_start")
    elif project_type == "course":
        response = CaliScripts.say("goat_builder", "course_start")
    else:
        response = CaliScripts.say("goat_builder", "framework_start")

    return {"message": response}

@app.get("/pricing")
async def pricing_info():
    """Pricing page information."""
    return {
        "explanation": CaliScripts.say("pricing", "explain_packages"),
        "web3_note": CaliScripts.say("pricing", "web3_domains")
    }

# Error handling example
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global error handler using CALI Scripts."""
    return {
        "error": CaliScripts.error("unknown_error"),
        "detail": str(exc)
    }

# frontend/src/components/Dashboard.jsx (React example)
import React, { useEffect, useState } from 'react';

function Dashboard({ user }) {
    const [message, setMessage] = useState('');

    useEffect(() => {
        // Fetch dashboard message from backend
        fetch('/dashboard')
            .then(res => res.json())
            .then(data => setMessage(data.welcome));
    }, [user]);

    return (
        <div className="dashboard">
            <h1>{message}</h1>
            <p>Caleon is ready to help you build your legacy.</p>
        </div>
    );
}

export default Dashboard;

# frontend/src/components/DraftProgress.jsx
import React from 'react';

function DraftProgress({ chapter, section, status }) {
    // Import would be from a frontend API wrapper
    // const CaliScripts = useCaliScripts();

    const getProgressMessage = () => {
        switch(status) {
            case 'starting':
                return `Starting chapter ${chapter}, section ${section}. Give me a moment.`;
            case 'progress':
                return 'Still drafting… good work takes a minute.';
            case 'complete':
                return `Chapter ${chapter} complete. Take a look before we move forward.`;
            default:
                return 'Draft in progress...';
        }
    };

    return (
        <div className="draft-progress">
            <p>{getProgressMessage()}</p>
        </div>
    );
}

# Python utility for frontend integration
def get_cali_message(category, entry, **variables):
    """
    Utility function that could be called from frontend via API
    """
    return CaliScripts.say(category, entry, **variables)

# Example usage in error boundaries
class ErrorBoundary extends React.Component {
    constructor(props) {
        super(props);
        this.state = { hasError: false, errorMessage: '' };
    }

    static getDerivedStateFromError(error) {
        return { hasError: true };
    }

    componentDidCatch(error, errorInfo) {
        // In real implementation, call backend API for CALI error message
        this.setState({
            errorMessage: "Something unexpected happened. I'm on it — try again in a moment."
        });
    }

    render() {
        if (this.state.hasError) {
            return <h1>{this.state.errorMessage}</h1>;
        }

        return this.props.children;
    }
}