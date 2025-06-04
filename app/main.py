from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, validator
from typing import List, Dict, Any, Optional
import google.generativeai as genai
import os
from dotenv import load_dotenv
import logging
import re
from uuid import uuid4
from fastapi.responses import JSONResponse
from fastapi.security import APIKeyHeader
from functools import lru_cache
import json
from datetime import UTC, datetime, timedelta
from .data.questions import TRIP_QUESTIONS, VACATION_QUESTIONS
from .data.prompts import create_trip_prompt, create_vacation_prompt

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

app = FastAPI(
    title="Enhanced Trip Planner API",
    description="A robust API for generating personalized travel itineraries using Gemini AI",
    version="2.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

origins = [
    "http://localhost:3000",
    "http://localhost:5173",
    "https://voythrix.com",
    "https://www.voythrix.com",
]

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Adjust for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure Gemini AI
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# API Key for additional security (optional)
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

async def verify_api_key(api_key: str = Depends(api_key_header)):
    expected_key = os.getenv("API_KEY")
    if expected_key and api_key != expected_key:
        raise HTTPException(status_code=403, detail="Invalid API Key")
    return api_key

class TripAnswers(BaseModel):
    start_location: str = Field(..., description="Starting location for the trip, e.g., 'New York City'")
    destinations: str = Field(..., description="Separated list of destinations, e.g., 'Paris, Rome, Barcelona'")
    budget: str = Field(..., description="Budget range, e.g., 'INR 5000-10000/day' or 'USD 100-200/day'")
    travel_style: List[str] = Field(..., min_items=1, max_items=3, description="Preferred travel styles (1-3)")
    accommodation: List[str] = Field(..., min_items=1, max_items=3, description="Preferred accommodation types (1-3)")
    interests: List[str] = Field(..., min_items=1, max_items=5, description="Traveler interests (1-5)")
    group_size: str = Field(..., description="Group size, e.g., 'Solo traveler', 'Couple'")
    transportation: str = Field(..., description="Preferred transportation mode")
    dietary_restrictions: Optional[List[str]] = Field(None, description="Dietary restrictions")
    special_requirements: Optional[str] = Field(None, description="Special needs")
    pace: Optional[str] = Field("Moderate", description="Preferred pace: Relaxed, Moderate, or Fast-paced")
    start_date: str = Field(None, description="Trip start date in YYYY-MM-DD format")
    end_date: str = Field(None, description="Trip end date in YYYY-MM-DD format")
        
class VacationAnswers(BaseModel):
   vacation_style: List[str] = Field(..., min_items=1, max_items=3, description="Preferred travel style, e.g., beach, adventure, mountains, cultural")
   departure_location: str = Field(..., description="Departure location, e.g., 'New York City'")
   start_date: str = Field(..., description="Trip start date in YYYY-MM-DD format")
   end_date: str = Field(..., description="Trip end date in YYYY-MM-DD format")
   budget: str = Field(..., description="Budget range, e.g., 'INR 30000 per person' or 'USD 500 per person'")
   preferred_region: str = Field(..., description="Preferred destination region/country, e.g., 'Europe', 'Asia', 'Open to all regions'")
   visa_flexibility: str = Field(..., description="Visa flexibility, e.g., 'Visa-free', 'Visa-on-arrival', 'Any'")
   special_requirements: str = Field(..., description="Choose place where I can go skydiving")
   group_size: str = Field(..., description="Group size, e.g., 'Solo traveler', 'Couple'")

def sanitize_input(text: Optional[str]) -> Optional[str]:
    """Sanitize inputs to prevent prompt injection"""
    if not text:
        return text
    # Remove potentially harmful characters and keywords
    dangerous_patterns = [
        r"[\n\r;]",
        r"(?i)(prompt|inject|execute|script|system|file|http)",
        r"[<>{}[\]\\]"
    ]
    sanitized = text
    for pattern in dangerous_patterns:
        sanitized = re.sub(pattern, "", sanitized)
    return sanitized.strip()[:500]  # Limit length

@app.get("/")
async def root():
    return {
        "message": "Enhanced Trip Planner API is running!",
        "version": app.version,
        "docs": "/docs",
        "redoc": "/redoc"
    }

@app.get("/questions", response_model=Dict[str, Any])
async def get_questions():
    """Return curated questions for trip planning with improved structure"""
    return TRIP_QUESTIONS

@app.get("/vacation-questions", response_model=Dict[str, Any])
async def get_vacation_questions():
    """Return curated questions for vacation planning with improved structure"""
    return VACATION_QUESTIONS

@app.post("/generate-itinerary", response_model=Dict[str, Any])
async def generate_itinerary(answers: TripAnswers):
    """Generate a personalized trip itinerary using Gemini AI"""
    try:
        # Validate API key
        if not os.getenv("GEMINI_API_KEY"):
            logger.error("Gemini API key not configured")
            raise HTTPException(
                status_code=500,
                detail="Service configuration error. Please contact support."
            )

        # Create the model
        model = genai.GenerativeModel('gemini-2.5-flash-preview-05-20')

        # Sanitize and prepare answers
        sanitized_answers = {
            "start_location": sanitize_input(answers.start_location),
            "destinations": sanitize_input(answers.destinations),
            "budget": sanitize_input(answers.budget),
            "travel_style": [sanitize_input(s) for s in answers.travel_style],
            "accommodation": [sanitize_input(a) for a in answers.accommodation],
            "interests": [sanitize_input(i) for i in answers.interests],
            "group_size": sanitize_input(answers.group_size),
            "transportation": sanitize_input(answers.transportation),
            "dietary_restrictions": [sanitize_input(d) for d in answers.dietary_restrictions] if answers.dietary_restrictions else None,
            "special_requirements": sanitize_input(answers.special_requirements),
            "pace": sanitize_input(answers.pace),
            "start_date": answers.start_date,
            "end_date": answers.end_date,
            "duration": None
        }

        try:
            start_dt = datetime.strptime(answers.start_date, "%Y-%m-%d")
            end_dt = datetime.strptime(answers.end_date, "%Y-%m-%d")
            sanitized_answers["duration"] = (end_dt - start_dt).days
        except Exception:
            pass

        # Generate the prompt
        prompt = create_trip_prompt(sanitized_answers)
        logger.info(f"Generating itinerary for: {answers.destinations}")

        # Generate content with safety settings
        response = model.generate_content(
            prompt,
            safety_settings={
                'HARM_CATEGORY_HARASSMENT': 'BLOCK_NONE',
                'HARM_CATEGORY_HATE_SPEECH': 'BLOCK_NONE',
                'HARM_CATEGORY_SEXUALLY_EXPLICIT': 'BLOCK_NONE',
                'HARM_CATEGORY_DANGEROUS_CONTENT': 'BLOCK_NONE'
            }
        )

        if not response.text:
            logger.error("Empty response from Gemini AI")
            raise HTTPException(
                status_code=500,
                detail="The trip planner service is currently unavailable. Please try again later."
            )
        
        # Parse response as JSON
        try:
            itinerary = json.loads(response.text)
            if not isinstance(itinerary, dict):
                raise ValueError("Invalid itinerary format")
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON: {str(e)}")
            # Attempt to extract JSON from malformed response
            json_match = re.search(r'```json\n(.*?)\n```', response.text, re.DOTALL)

            if json_match:
                retries = 0
                max_retries = 2
                while retries <= max_retries:
                    try:
                        itinerary = json.loads(json_match.group(1))
                        break
                    except json.JSONDecodeError:
                        if retries == max_retries:
                            raise HTTPException(
                                status_code=500,
                                detail="We couldn't process the itinerary after multiple attempts. Please adjust your inputs and try again."
                            )
                        retries += 1
                        logger.warning(f"JSON decode failed, attempt {retries} of {max_retries}")
            else:
                raise HTTPException(
                    status_code=500,
                    detail="We couldn't process the itinerary. Please adjust your inputs and try again."
                )
        except Exception as e:
            logger.error(f"Unexpected parsing error: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail="An error occurred while processing your itinerary."
            )

        # Generate request ID and log success
        request_id = str(uuid4())
        logger.info(f"Successfully generated itinerary {request_id} for {answers.destinations}")

        return {
            "success": True,
            "trip_itinerary": itinerary,
            "meta": {
                "request_id": request_id,
                "generated_at": datetime.utcnow().isoformat(),
                "destination_count": len(answers.destinations),
                "duration": sanitized_answers["duration"]
            }
        }

    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred. Our team has been notified."
        )
    
@app.post("/generate-vacation", response_model=Dict[str, Any])
async def generate_vacation(answers: VacationAnswers):
    """Generate a personalized vacation itinerary using Gemini AI"""
    try:
        # Validate API key
        if not os.getenv("GEMINI_API_KEY"):
            logger.error("Gemini API key not configured")
            raise HTTPException(
                status_code=500,
                detail="Service configuration error. Please contact support."
            )

        # Create the model
        model = genai.GenerativeModel('gemini-2.5-flash-preview-05-20') 

        # Sanitize and prepare answers
        sanitized_answers = {
            "vacation_style": [sanitize_input(s) for s in answers.vacation_style],
            "departure_location": sanitize_input(answers.departure_location),
            "start_date": answers.start_date,
            "end_date": answers.end_date,
            "budget": sanitize_input(answers.budget),
            "preferred_region": sanitize_input(answers.preferred_region),
            "visa_flexibility": sanitize_input(answers.visa_flexibility),
            "special_requirements": sanitize_input(answers.special_requirements),
            "group_size": sanitize_input(answers.group_size)
        }

        # Generate the prompt
        prompt = create_vacation_prompt(sanitized_answers)
        logger.info(f"Generating vacation for: {answers.vacation_style[0].capitalize()}")
        
        # Generate content with safety settings
        response = model.generate_content(
            prompt,
            safety_settings={
                'HARM_CATEGORY_HARASSMENT': 'BLOCK_NONE',
                'HARM_CATEGORY_HATE_SPEECH': 'BLOCK_NONE',
                'HARM_CATEGORY_SEXUALLY_EXPLICIT': 'BLOCK_NONE',
                'HARM_CATEGORY_DANGEROUS_CONTENT': 'BLOCK_NONE'
            }
        )

        if not response.text:
            logger.error("Empty response from Gemini AI")
            raise HTTPException(
                status_code=500,
                detail="The vacation planner service is currently unavailable. Please try again later."
            )
        
        # Parse response as JSON
        try:
            vacation = json.loads(response.text)
            if not isinstance(vacation, dict):
                raise ValueError("Invalid vacation format")
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON: {str(e)}")
            # Attempt to extract JSON from malformed response
            json_match = re.search(r'```json\n(.*?)\n```', response.text, re.DOTALL)
            if json_match:
                retries = 0
                max_retries = 2
                while retries <= max_retries:
                    try:
                        vacation = json.loads(json_match.group(1))
                        break
                    except json.JSONDecodeError:
                        if retries == max_retries:
                            raise HTTPException(
                                status_code=500,
                                detail="We couldn't process the vacation after multiple attempts. Please adjust your inputs and try again."
                            )
                        retries += 1
                        logger.warning(f"JSON decode failed, attempt {retries} of {max_retries}")
            else:
                raise HTTPException(
                    status_code=500,
                    detail="We couldn't process the vacation. Please adjust your inputs and try again."
                )
        except Exception as e:
            logger.error(f"Unexpected parsing error: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail="An error occurred while processing your vacation."
            )
        
        # Generate request ID and log success
        request_id = str(uuid4())
        logger.info(f"Successfully generated vacation {request_id} for {answers.vacation_style[0].capitalize()}")

        return {
            "success": True,
            "vacation_itinerary": vacation,
            "meta": {
                "request_id": request_id,
                "generated_at": datetime.now(UTC).isoformat(),
                "destination_count": len(answers.departure_location),
            }
        }
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred. Our team has been notified."
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)