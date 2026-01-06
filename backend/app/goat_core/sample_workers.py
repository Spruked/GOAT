# ==========================================
# SAMPLE WORKER IMPLEMENTATIONS
# Concrete workers that can be deployed by DALS forge
# ==========================================

from typing import Dict, List, Any, Optional
from .goat_orchestrator import WorkerPlaceholder, WorkerManifest
import asyncio
import random

# ==========================================
# BASE WORKER CLASSES
# ==========================================

class BaseWorker(WorkerPlaceholder):
    """Base implementation with common functionality"""

    def __init__(self, manifest: WorkerManifest):
        super().__init__(manifest)
        self.response_templates: Dict[str, List[str]] = {}
        self._initialize_templates()

    def _initialize_templates(self):
        """Override in subclasses to set up response templates"""
        pass

    async def execute(self, task: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Basic execution with template-based responses"""
        message = task.get("message", "")

        # Simple keyword matching for demo
        response_key = self._classify_message(message)

        if response_key in self.response_templates:
            template = random.choice(self.response_templates[response_key])
            response = self._format_response(template, task, context)
        else:
            response = self._get_fallback_response(message)

        # Simulate learning
        await self.learn_from_experience({"response": response}, {"useful": True})

        return {"response": response, "worker_id": self.manifest.worker_id}

    def _classify_message(self, message: str) -> str:
        """Override in subclasses for message classification"""
        return "general"

    def _format_response(self, template: str, task: Dict[str, Any], context: Dict[str, Any]) -> str:
        """Format template with context"""
        return template

    def _get_fallback_response(self, message: str) -> str:
        """Fallback response when no template matches"""
        return f"I understand you're asking about: {message[:50]}... Let me help with that."

    async def learn_from_experience(self, result: Dict[str, Any], feedback: Dict[str, Any]):
        """Basic learning - increase specialization score"""
        if feedback.get("useful", False):
            self.manifest.specialization_score = min(1.0, self.manifest.specialization_score + 0.01)

# ==========================================
# DEPARTMENT-SPECIFIC WORKERS
# ==========================================

class OnboardingWorker(BaseWorker):
    """Handles user onboarding and setup"""

    def _initialize_templates(self):
        self.response_templates = {
            "getting_started": [
                "Welcome to GOAT! Let's get you set up. First, tell me what you'd like to build or explore.",
                "Great! I'm here to guide you through your first steps. What type of project interests you?",
                "Perfect! Let's start your journey. Are you looking to create content, build an app, or explore our features?"
            ],
            "setup_help": [
                "I'll help you with the setup process. What specific area do you need assistance with?",
                "Setup is my specialty! Let me walk you through the key steps.",
                "Let's get everything configured properly. What's your first question about setup?"
            ],
            "general": [
                "I'm here to help you get started! What would you like to know?",
                "Let's begin your onboarding journey. What can I assist you with today?"
            ]
        }

    def _classify_message(self, message: str) -> str:
        msg_lower = message.lower()
        if any(word in msg_lower for word in ["start", "begin", "getting started", "new"]):
            return "getting_started"
        if any(word in msg_lower for word in ["setup", "configure", "install"]):
            return "setup_help"
        return "general"

class PricingWorker(BaseWorker):
    """Handles pricing and subscription questions"""

    def _initialize_templates(self):
        self.response_templates = {
            "cost_inquiry": [
                "I'd be happy to explain our pricing structure. We offer flexible plans starting at $29/month.",
                "Our pricing is designed to scale with your needs. Let me show you the options.",
                "We have several tiers to choose from. Which features are most important to you?"
            ],
            "subscription": [
                "We offer monthly and annual subscriptions with different feature sets.",
                "You can upgrade or downgrade your plan at any time. Would you like to see the comparison?",
                "Our subscription includes full access to all departments and unlimited worker deployments."
            ],
            "general": [
                "I can help you understand our pricing and find the right plan for your needs.",
                "Let's discuss what works best for your budget and requirements."
            ]
        }

    def _classify_message(self, message: str) -> str:
        msg_lower = message.lower()
        if any(word in msg_lower for word in ["cost", "price", "fee", "charge"]):
            return "cost_inquiry"
        if any(word in msg_lower for word in ["subscription", "plan", "billing"]):
            return "subscription"
        return "general"

class CreatorWorker(BaseWorker):
    """Handles content creation and building"""

    def _initialize_templates(self):
        self.response_templates = {
            "content_creation": [
                "Let's create something amazing! What type of content are you thinking of?",
                "I'm excited to help you build. Do you have a specific project in mind?",
                "Creation mode activated! Tell me about what you want to make."
            ],
            "design_help": [
                "I can help with design concepts and implementation. What are you designing?",
                "Let's collaborate on your design. What style or aesthetic appeals to you?",
                "Design is one of my specialties. How can I assist with your project?"
            ],
            "general": [
                "I'm here to help you create and build. What would you like to work on?",
                "Let's get creative! What's your next project?"
            ]
        }

    def _classify_message(self, message: str) -> str:
        msg_lower = message.lower()
        if any(word in msg_lower for word in ["create", "build", "make", "content"]):
            return "content_creation"
        if any(word in msg_lower for word in ["design", "ui", "ux", "visual"]):
            return "design_help"
        return "general"

class TechWorker(BaseWorker):
    """Handles technical questions and integration"""

    def _initialize_templates(self):
        self.response_templates = {
            "api_integration": [
                "I can help you integrate with our APIs. What system are you connecting to?",
                "API integration is straightforward. Let me guide you through the process.",
                "We have comprehensive API documentation. Which integration are you working on?"
            ],
            "technical_setup": [
                "Let's get your technical setup configured. What are you trying to accomplish?",
                "I can help with the technical details. What's your current setup?",
                "Technical configuration is my expertise. How can I assist?"
            ],
            "general": [
                "I handle all the technical aspects. What technical question do you have?",
                "Let's solve this technical challenge together. What's the issue?"
            ]
        }

    def _classify_message(self, message: str) -> str:
        msg_lower = message.lower()
        if any(word in msg_lower for word in ["api", "integration", "connect"]):
            return "api_integration"
        if any(word in msg_lower for word in ["setup", "configure", "technical", "code"]):
            return "technical_setup"
        return "general"

class LegalWorker(BaseWorker):
    """Handles legal and policy questions"""

    def _initialize_templates(self):
        self.response_templates = {
            "policy_questions": [
                "I can help explain our policies. Which policy are you asking about?",
                "Our policies are designed to protect both users and creators. Let me clarify.",
                "Policy questions are important. Let me provide the relevant information."
            ],
            "terms_service": [
                "Our Terms of Service cover usage rights and responsibilities. Would you like me to explain any specific section?",
                "The terms are written to be clear and fair. What aspect would you like to understand better?",
                "Terms of Service ensure a great experience for everyone. How can I help clarify them?"
            ],
            "general": [
                "I handle legal and policy matters. What legal question do you have?",
                "Legal compliance is crucial. How can I assist with your policy questions?"
            ]
        }

    def _classify_message(self, message: str) -> str:
        msg_lower = message.lower()
        if any(word in msg_lower for word in ["policy", "privacy", "gdpr", "compliance"]):
            return "policy_questions"
        if any(word in msg_lower for word in ["terms", "service", "agreement", "contract"]):
            return "terms_service"
        return "general"

# ==========================================
# WORKER FACTORY (DALS Forge Connector)
# ==========================================

def dals_forge_connector(
    worker_id: str,
    department: str,
    feature: str,
    logic_seed: str,
    custom_skills: Dict[str, Any]
) -> WorkerPlaceholder:
    """
    Factory function that creates workers based on department/feature.
    This is the main integration point for the DALS forge.
    """

    # Worker type mapping
    worker_classes = {
        ("Onboarding", "setup"): OnboardingWorker,
        ("Onboarding", "guide"): OnboardingWorker,
        ("Pricing", "info"): PricingWorker,
        ("Pricing", "advisor"): PricingWorker,
        ("Creator", "tools"): CreatorWorker,
        ("Creator", "content"): CreatorWorker,
        ("Tech", "integration"): TechWorker,
        ("Tech", "api"): TechWorker,
        ("Legal", "policy"): LegalWorker,
        ("Legal", "terms"): LegalWorker,
    }

    # Get the appropriate worker class
    worker_class = worker_classes.get((department, feature), BaseWorker)

    # Create manifest
    manifest = WorkerManifest(
        worker_id=worker_id,
        department=department,
        feature=feature,
        logic_template=logic_seed,
        skills_snapshot=custom_skills
    )

    # Instantiate and return
    return worker_class(manifest=manifest)
