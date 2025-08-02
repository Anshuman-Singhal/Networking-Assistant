from fastapi import FastAPI, APIRouter, HTTPException, BackgroundTasks
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import uuid
from datetime import datetime, timedelta
from enum import Enum
import asyncio

# Import emergentintegrations for LLM
from emergentintegrations.llm.chat import LlmChat, UserMessage

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Create the main app without a prefix
app = FastAPI(title="NetworkingAI API", description="Intelligent Networking Assistant")

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# Enums
class CampaignStatus(str, Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETED = "completed"

class ContactStatus(str, Enum):
    NEW = "new"
    CONTACTED = "contacted"
    RESPONDED = "responded"
    CONVERTED = "converted"

class Priority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

# Models
class Contact(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    email: str
    company: Optional[str] = None
    position: Optional[str] = None
    industry: Optional[str] = None
    linkedin_url: Optional[str] = None
    phone: Optional[str] = None
    notes: Optional[str] = None
    status: ContactStatus = ContactStatus.NEW
    priority: Priority = Priority.MEDIUM
    lead_score: int = Field(default=50, ge=0, le=100)
    relationship_strength: int = Field(default=0, ge=0, le=100)
    tags: List[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    last_contacted: Optional[datetime] = None
    last_interaction: Optional[datetime] = None

class ContactCreate(BaseModel):
    name: str
    email: str
    company: Optional[str] = None
    position: Optional[str] = None
    industry: Optional[str] = None
    linkedin_url: Optional[str] = None
    phone: Optional[str] = None
    notes: Optional[str] = None
    priority: Priority = Priority.MEDIUM
    tags: List[str] = Field(default_factory=list)

class ContactUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    company: Optional[str] = None
    position: Optional[str] = None
    industry: Optional[str] = None
    linkedin_url: Optional[str] = None
    phone: Optional[str] = None
    notes: Optional[str] = None
    status: Optional[ContactStatus] = None
    priority: Optional[Priority] = None
    tags: Optional[List[str]] = None

class EmailTemplate(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    subject: str
    body: str
    type: str  # "introduction", "follow_up", "meeting_request", etc.
    created_at: datetime = Field(default_factory=datetime.utcnow)

class EmailTemplateCreate(BaseModel):
    name: str
    subject: str
    body: str
    type: str

class Campaign(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    description: Optional[str] = None
    status: CampaignStatus = CampaignStatus.DRAFT
    contact_ids: List[str] = Field(default_factory=list)
    template_id: Optional[str] = None
    scheduled_at: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    sent_count: int = 0
    response_count: int = 0
    conversion_count: int = 0

class CampaignCreate(BaseModel):
    name: str
    description: Optional[str] = None
    contact_ids: List[str] = Field(default_factory=list)
    template_id: Optional[str] = None
    scheduled_at: Optional[datetime] = None

class CampaignUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[CampaignStatus] = None
    contact_ids: Optional[List[str]] = None
    template_id: Optional[str] = None
    scheduled_at: Optional[datetime] = None

class NetworkingGoals(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str = Field(default="default_user")
    industry: str
    role: str
    company_size: Optional[str] = None
    networking_objectives: List[str] = Field(default_factory=list)
    target_contacts_per_month: int = Field(default=10)
    preferred_communication_style: str = Field(default="professional")
    pain_points: List[str] = Field(default_factory=list)
    success_metrics: List[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class NetworkingGoalsCreate(BaseModel):
    industry: str
    role: str
    company_size: Optional[str] = None
    networking_objectives: List[str] = Field(default_factory=list)
    target_contacts_per_month: int = Field(default=10)
    preferred_communication_style: str = Field(default="professional")
    pain_points: List[str] = Field(default_factory=list)
    success_metrics: List[str] = Field(default_factory=list)

class EmailGenerationRequest(BaseModel):
    contact_id: str
    email_type: str  # "introduction", "follow_up", "meeting_request"
    context: Optional[str] = None
    tone: str = Field(default="professional")

class EmailGenerationResponse(BaseModel):
    subject: str
    body: str
    personalization_notes: List[str] = Field(default_factory=list)

class InteractionLog(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    contact_id: str
    type: str  # "email_sent", "email_received", "meeting", "call", etc.
    subject: Optional[str] = None
    content: Optional[str] = None
    status: str = Field(default="completed")
    created_at: datetime = Field(default_factory=datetime.utcnow)

class InteractionLogCreate(BaseModel):
    contact_id: str
    type: str
    subject: Optional[str] = None
    content: Optional[str] = None
    status: str = Field(default="completed")

class AnalyticsResponse(BaseModel):
    total_contacts: int
    contacts_by_status: Dict[str, int]
    contacts_by_priority: Dict[str, int]
    total_campaigns: int
    campaigns_by_status: Dict[str, int]
    email_performance: Dict[str, Any]
    relationship_scores: Dict[str, float]
    monthly_growth: Dict[str, int]

# API Key placeholder - User will fill this in
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY', 'YOUR_OPENAI_API_KEY_HERE')

# Helper functions
async def get_llm_chat(session_id: str, system_message: str) -> LlmChat:
    """Create a new LLM chat instance"""
    chat = LlmChat(
        api_key=OPENAI_API_KEY,
        session_id=session_id,
        system_message=system_message
    )
    return chat.with_model("openai", "gpt-4o").with_max_tokens(4096)

async def calculate_lead_score(contact: Contact) -> int:
    """Calculate lead score based on contact information"""
    score = 50  # Base score
    
    if contact.company:
        score += 10
    if contact.position:
        score += 10
    if contact.linkedin_url:
        score += 15
    if contact.industry:
        score += 10
    if contact.phone:
        score += 5
    
    # Bonus for recent interactions
    if contact.last_interaction:
        days_since = (datetime.utcnow() - contact.last_interaction).days
        if days_since < 7:
            score += 20
        elif days_since < 30:
            score += 10
    
    return min(score, 100)

async def update_relationship_strength(contact_id: str):
    """Update relationship strength based on interactions"""
    interactions = await db.interaction_logs.find({"contact_id": contact_id}).to_list(None)
    
    base_strength = len(interactions) * 5
    recent_interactions = [i for i in interactions if (datetime.utcnow() - i["created_at"]).days < 30]
    recent_bonus = len(recent_interactions) * 10
    
    strength = min(base_strength + recent_bonus, 100)
    
    await db.contacts.update_one(
        {"id": contact_id},
        {"$set": {"relationship_strength": strength, "updated_at": datetime.utcnow()}}
    )

# Routes
@api_router.get("/")
async def root():
    return {"message": "NetworkingAI API is running"}

# Networking Goals Routes
@api_router.post("/networking-goals", response_model=NetworkingGoals)
async def create_networking_goals(goals: NetworkingGoalsCreate):
    goals_dict = goals.dict()
    goals_obj = NetworkingGoals(**goals_dict)
    await db.networking_goals.insert_one(goals_obj.dict())
    return goals_obj

@api_router.get("/networking-goals", response_model=List[NetworkingGoals])
async def get_networking_goals(user_id: str = "default_user"):
    goals = await db.networking_goals.find({"user_id": user_id}).to_list(1000)
    return [NetworkingGoals(**goal) for goal in goals]

# Contact Routes
@api_router.post("/contacts", response_model=Contact)
async def create_contact(contact: ContactCreate):
    contact_dict = contact.dict()
    contact_obj = Contact(**contact_dict)
    
    # Calculate initial lead score
    contact_obj.lead_score = await calculate_lead_score(contact_obj)
    
    await db.contacts.insert_one(contact_obj.dict())
    return contact_obj

@api_router.get("/contacts", response_model=List[Contact])
async def get_contacts(
    status: Optional[ContactStatus] = None,
    priority: Optional[Priority] = None,
    limit: int = 100
):
    filter_dict = {}
    if status:
        filter_dict["status"] = status
    if priority:
        filter_dict["priority"] = priority
    
    contacts = await db.contacts.find(filter_dict).limit(limit).to_list(limit)
    return [Contact(**contact) for contact in contacts]

@api_router.get("/contacts/{contact_id}", response_model=Contact)
async def get_contact(contact_id: str):
    contact = await db.contacts.find_one({"id": contact_id})
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    return Contact(**contact)

@api_router.put("/contacts/{contact_id}", response_model=Contact)
async def update_contact(contact_id: str, contact_update: ContactUpdate):
    contact = await db.contacts.find_one({"id": contact_id})
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    
    update_dict = contact_update.dict(exclude_unset=True)
    update_dict["updated_at"] = datetime.utcnow()
    
    await db.contacts.update_one({"id": contact_id}, {"$set": update_dict})
    
    updated_contact = await db.contacts.find_one({"id": contact_id})
    return Contact(**updated_contact)

@api_router.delete("/contacts/{contact_id}")
async def delete_contact(contact_id: str):
    result = await db.contacts.delete_one({"id": contact_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Contact not found")
    return {"message": "Contact deleted successfully"}

# AI Email Generation Routes
@api_router.post("/generate-email", response_model=EmailGenerationResponse)
async def generate_email(request: EmailGenerationRequest):
    if OPENAI_API_KEY == 'YOUR_OPENAI_API_KEY_HERE':
        raise HTTPException(status_code=400, detail="OpenAI API key not configured. Please add your API key to the .env file.")
    
    # Get contact information
    contact = await db.contacts.find_one({"id": request.contact_id})
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    
    contact_obj = Contact(**contact)
    
    # Get networking goals for context
    goals = await db.networking_goals.find_one({"user_id": "default_user"})
    
    # Create system message for AI
    system_message = f"""You are an expert networking assistant that generates personalized outreach emails. 
    Your task is to create professional, engaging emails that help build meaningful business relationships.
    
    Always respond in the following JSON format:
    {{
        "subject": "Email subject line",
        "body": "Email body content",
        "personalization_notes": ["note1", "note2"]
    }}
    """
    
    # Create prompt for email generation
    prompt = f"""Generate a {request.email_type} email for the following contact:
    
    Contact Information:
    - Name: {contact_obj.name}
    - Company: {contact_obj.company or 'Not specified'}
    - Position: {contact_obj.position or 'Not specified'}
    - Industry: {contact_obj.industry or 'Not specified'}
    
    Email Type: {request.email_type}
    Tone: {request.tone}
    Additional Context: {request.context or 'None'}
    
    {"Networking Goals: " + str(goals.get('networking_objectives', [])) if goals else ""}
    
    Please generate a personalized email that:
    1. Is appropriate for the {request.email_type} purpose
    2. Matches the {request.tone} tone
    3. Includes relevant personalization based on their company/position
    4. Is concise and actionable
    5. Follows professional email best practices
    """
    
    try:
        # Generate email using AI
        chat = await get_llm_chat(f"email_gen_{request.contact_id}", system_message)
        user_message = UserMessage(text=prompt)
        
        response = await chat.send_message(user_message)
        
        # Parse the response (assuming it returns JSON format)
        import json
        try:
            email_data = json.loads(response)
            return EmailGenerationResponse(**email_data)
        except json.JSONDecodeError:
            # Fallback if AI doesn't return JSON
            lines = response.split('\n')
            subject = lines[0] if lines else f"Re: {request.email_type.replace('_', ' ').title()}"
            body = '\n'.join(lines[1:]) if len(lines) > 1 else response
            
            return EmailGenerationResponse(
                subject=subject,
                body=body,
                personalization_notes=[f"Generated for {contact_obj.name} at {contact_obj.company}"]
            )
            
    except Exception as e:
        logger.error(f"Error generating email: {str(e)}")
        # Fallback response
        return EmailGenerationResponse(
            subject=f"Re: {request.email_type.replace('_', ' ').title()}",
            body=f"Hi {contact_obj.name},\n\nI hope this email finds you well.\n\n[This is a placeholder - please configure your OpenAI API key for AI-generated content]\n\nBest regards",
            personalization_notes=["AI generation failed - using template"]
        )

# Email Template Routes
@api_router.post("/email-templates", response_model=EmailTemplate)
async def create_email_template(template: EmailTemplateCreate):
    template_dict = template.dict()
    template_obj = EmailTemplate(**template_dict)
    await db.email_templates.insert_one(template_obj.dict())
    return template_obj

@api_router.get("/email-templates", response_model=List[EmailTemplate])
async def get_email_templates():
    templates = await db.email_templates.find().to_list(1000)
    return [EmailTemplate(**template) for template in templates]

# Campaign Routes
@api_router.post("/campaigns", response_model=Campaign)
async def create_campaign(campaign: CampaignCreate):
    campaign_dict = campaign.dict()
    campaign_obj = Campaign(**campaign_dict)
    await db.campaigns.insert_one(campaign_obj.dict())
    return campaign_obj

@api_router.get("/campaigns", response_model=List[Campaign])
async def get_campaigns():
    campaigns = await db.campaigns.find().to_list(1000)
    return [Campaign(**campaign) for campaign in campaigns]

@api_router.get("/campaigns/{campaign_id}", response_model=Campaign)
async def get_campaign(campaign_id: str):
    campaign = await db.campaigns.find_one({"id": campaign_id})
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    return Campaign(**campaign)

@api_router.put("/campaigns/{campaign_id}", response_model=Campaign)
async def update_campaign(campaign_id: str, campaign_update: CampaignUpdate):
    campaign = await db.campaigns.find_one({"id": campaign_id})
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    
    update_dict = campaign_update.dict(exclude_unset=True)
    update_dict["updated_at"] = datetime.utcnow()
    
    await db.campaigns.update_one({"id": campaign_id}, {"$set": update_dict})
    
    updated_campaign = await db.campaigns.find_one({"id": campaign_id})
    return Campaign(**updated_campaign)

# Interaction Logging Routes
@api_router.post("/interactions", response_model=InteractionLog)
async def create_interaction_log(interaction: InteractionLogCreate):
    interaction_dict = interaction.dict()
    interaction_obj = InteractionLog(**interaction_dict)
    
    await db.interaction_logs.insert_one(interaction_obj.dict())
    
    # Update contact's last interaction and relationship strength
    await db.contacts.update_one(
        {"id": interaction.contact_id},
        {"$set": {"last_interaction": datetime.utcnow()}}
    )
    
    # Update relationship strength in background
    await update_relationship_strength(interaction.contact_id)
    
    return interaction_obj

@api_router.get("/interactions/{contact_id}", response_model=List[InteractionLog])
async def get_contact_interactions(contact_id: str):
    interactions = await db.interaction_logs.find({"contact_id": contact_id}).to_list(1000)
    return [InteractionLog(**interaction) for interaction in interactions]

# Analytics Routes
@api_router.get("/analytics", response_model=AnalyticsResponse)
async def get_analytics():
    # Get contact statistics
    total_contacts = await db.contacts.count_documents({})
    
    contacts_by_status = {}
    for status in ContactStatus:
        count = await db.contacts.count_documents({"status": status.value})
        contacts_by_status[status.value] = count
    
    contacts_by_priority = {}
    for priority in Priority:
        count = await db.contacts.count_documents({"priority": priority.value})
        contacts_by_priority[priority.value] = count
    
    # Get campaign statistics
    total_campaigns = await db.campaigns.count_documents({})
    
    campaigns_by_status = {}
    for status in CampaignStatus:
        count = await db.campaigns.count_documents({"status": status.value})
        campaigns_by_status[status.value] = count
    
    # Calculate email performance
    campaigns = await db.campaigns.find().to_list(1000)
    total_sent = sum(c.get("sent_count", 0) for c in campaigns)
    total_responses = sum(c.get("response_count", 0) for c in campaigns)
    total_conversions = sum(c.get("conversion_count", 0) for c in campaigns)
    
    email_performance = {
        "total_sent": total_sent,
        "total_responses": total_responses,
        "total_conversions": total_conversions,
        "response_rate": (total_responses / total_sent * 100) if total_sent > 0 else 0,
        "conversion_rate": (total_conversions / total_sent * 100) if total_sent > 0 else 0
    }
    
    # Calculate relationship scores
    contacts = await db.contacts.find().to_list(1000)
    avg_lead_score = sum(c.get("lead_score", 0) for c in contacts) / len(contacts) if contacts else 0
    avg_relationship_strength = sum(c.get("relationship_strength", 0) for c in contacts) / len(contacts) if contacts else 0
    
    relationship_scores = {
        "average_lead_score": avg_lead_score,
        "average_relationship_strength": avg_relationship_strength
    }
    
    # Monthly growth (simplified)
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    new_contacts_this_month = await db.contacts.count_documents({"created_at": {"$gte": thirty_days_ago}})
    
    monthly_growth = {
        "new_contacts": new_contacts_this_month,
        "new_campaigns": await db.campaigns.count_documents({"created_at": {"$gte": thirty_days_ago}})
    }
    
    return AnalyticsResponse(
        total_contacts=total_contacts,
        contacts_by_status=contacts_by_status,
        contacts_by_priority=contacts_by_priority,
        total_campaigns=total_campaigns,
        campaigns_by_status=campaigns_by_status,
        email_performance=email_performance,
        relationship_scores=relationship_scores,
        monthly_growth=monthly_growth
    )

# Contact Discovery Route (Simplified)
@api_router.post("/discover-contacts")
async def discover_contacts(criteria: Dict[str, Any]):
    """Simplified contact discovery - in a real app this would integrate with LinkedIn API, data providers, etc."""
    # This is a placeholder - real implementation would use external APIs
    sample_contacts = [
        {
            "name": "John Smith",
            "email": "john.smith@example.com",
            "company": "Tech Corp",
            "position": "Senior Developer",
            "industry": criteria.get("industry", "Technology"),
            "linkedin_url": "https://linkedin.com/in/johnsmith",
            "lead_score": 75
        },
        {
            "name": "Sarah Johnson",
            "email": "sarah.j@example.com",
            "company": "Innovation Inc",
            "position": "Product Manager",
            "industry": criteria.get("industry", "Technology"),
            "linkedin_url": "https://linkedin.com/in/sarahjohnson",
            "lead_score": 82
        }
    ]
    
    return {
        "discovered_contacts": sample_contacts,
        "total_found": len(sample_contacts),
        "criteria_used": criteria
    }

# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()