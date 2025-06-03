def create_trip_prompt(sanitized_answers: dict) -> str:
    """Create a detailed, optimized prompt for Gemini AI"""
    travel_style_str = ", ".join(sanitized_answers["travel_style"])
    accommodation_str = ", ".join(sanitized_answers["accommodation"])
    interests_str = ", ".join(sanitized_answers["interests"])
    dietary_str = ", ".join(sanitized_answers["dietary_restrictions"]) if sanitized_answers["dietary_restrictions"] else "None"

    date_info = ""
    if sanitized_answers["start_date"]:
        date_info = f"from {sanitized_answers['start_date']} to {sanitized_answers['end_date']}"

    prompt = f"""
As an expert travel planner with 20+ years of experience, create a highly personalized and detailed travel itinerary based on the following preferences. Your response must be a valid JSON object in the exact format specified below.

**Trip Specifications:**
- Starting Location: {sanitized_answers["start_location"]}
- Destinations: {sanitized_answers["destinations"]} 
- Duration: {sanitized_answers["duration"]} {date_info}
- Budget: {sanitized_answers["budget"]}
- Travel Style: {travel_style_str}
- Pace: {sanitized_answers["pace"]}

**Traveler Details:**
- Group Size: {sanitized_answers["group_size"]}
- Accommodation Preferences: {accommodation_str}
- Transportation Preferences: {sanitized_answers["transportation"]}
- Interests: {interests_str}
- Dietary Restrictions: {dietary_str}
- Special Requirements: {sanitized_answers["special_requirements"]}

**Output Format:**
You must return a valid JSON object with exactly this structure:
{{
    itinerary: {{
        "summary": "Brief engaging overview of the trip",
        "destinations": [ "destination1", "destination2", "destination3" ],
        "trip_duration": {{
            "start_date": "YYYY-MM-DD",
            "end_date": "YYYY-MM-DD",
            "total_days": 7,
        }},
        "daily_itinerary": [
            {{
                "day_number": 1,
                "date": "YYYY-MM-DD",
                "title": "Day Title",
                "description": "Detailed description of the day's activities",
            }},
            {{
                "day_number": 2,
                "date": "YYYY-MM-DD",
                "title": "Day Title",
                "description": "Detailed description of the day's activities",
            }},
        ],
        "accommodation": [{{
            "city": "City name",
            "recommendations": [
            {{
                "name": "Hotel/Hostel Name",
                "address": "Full address including street, city, state, zip code",
            }}
            ]
        }}],
        "dining": [{{
            "city": "City name",
            "recommendations": [
            {{
                "name": "Restaurant Name",
                "address": "Full address including street, city, state, zip code",
            }}
            ]
        }}],
        "hidden_gems": ["Hidden gem 1", "Hidden gem 2", "Hidden gem 3"],
        "estimated_costs": {{
            "currency": "departure location currency",
            "minimum_total": 1000,
            "maximum_total": 2000,
        }}
    }},
}}

Important Requirements:
1. The response MUST be a valid JSON object. Return the JSON in a single line.
2. All monetary values must include amounts and currency codes
3. All dates must be in YYYY-MM-DD format
4. All arrays must contain at least one item
5. All required fields must be present
6. No placeholder or example values should be in the final output
7. Use currency code for the currency of the departure location. Do not use symbols.
8. Ensure the itinerary is practical and respects the budget constraints
9. Include a brief engaging overview of the trip in the summary
10. Include 3-5 hidden gems or off-the-beaten-path suggestions for each destination
11. For dining and accommodation, provide 3 recommendations per city with full addresses
12. Ensure the daily itinerary is well-paced and considers travel time between activities
13. The start location is only for current location context, not part of the itinerary
"""
    return prompt

def create_vacation_prompt(sanitized_answers: dict) -> str:
    """Create a prompt to get vacation destination recommendations based on user preferences"""
    
    # Format the dates if provided
    date_info = ""
    if sanitized_answers.get("start_date") and sanitized_answers.get("end_date"):
        date_info = f"from {sanitized_answers['start_date']} to {sanitized_answers['end_date']}"

    prompt = f"""
As an expert travel consultant with extensive global experience, provide personalized vacation destination recommendations based on the following preferences. Focus on creating practical, well-matched suggestions that align with the traveler's interests and constraints.

**Traveler Preferences:**
- Vacation Style: {sanitized_answers["vacation_style"]}  # e.g., beach, adventure, mountains, cultural
- Departure Location: {sanitized_answers["departure_location"]}
- Travel Dates: {date_info}
- Vacation Budget: {sanitized_answers["budget"]}
- Preferred Destination Region/Country: {sanitized_answers.get("preferred_region", "Open to all regions")}
- Visa Flexibility: {sanitized_answers.get("visa_flexibility", "Any")}  
- Special Requirements: {sanitized_answers["special_requirements"]}
- Group Size: {sanitized_answers["group_size"]}

**Requirements for Recommendations:**
1. Provide exactly 5 best-matched destinations
2. Each destination must include:
   - Country and specific region/city
   - Why it's a perfect match for their vacation style
   - Estimated total cost per person (including accommodation, food, activities)
   - Visa requirements from their departure location
   - Best time to visit
   - Public transportation assessment (scale 1-10 with explanation)
   - Safety index (scale 1-10 with explanation)
   - Top 3 must-do activities
   - Recommended duration of stay

**Output Format:**
Return the recommendations in valid JSON format with this structure:
{{
    "summary": "Brief engaging overview of the trip",
    "recommendations": [
        {{
            "destination": {{
                "country": "Country name",
                "region": "Specific region/city",
                "match_score": 95  # 0-100 score based on preference match
            }},
            "why_perfect_match": "Detailed explanation of why this matches their preferences",
            "costs": {{
                "currency": "departure location currency",
                "total_per_person": 2000,
                "breakdown": {{
                    "accommodation": 800,
                    "food": 400,
                    "activities": 500,
                    "transportation": 300
                }}
            }},
            "visa_requirements": {{
                "type": "visa-free/visa-on-arrival/e-visa/embassy-visa",
                "processing_time": "X business days",
                "cost": "departure location currency XX",
                "requirements": ["requirement1", "requirement2"]
            }},
            "best_time_to_visit": {{
                "peak_season": ["Month1", "Month2"],
                "shoulder_season": ["Month3", "Month4"],
                "weather": "Description of weather during requested dates"
            }},
            "transportation": {{
                "score": 8,
                "explanation": "Detailed explanation of public transport system",
                "main_options": ["option1", "option2"]
            }},
            "safety": {{
                "score": 9,
                "explanation": "Safety assessment explanation",
                "special_considerations": ["consideration1", "consideration2"]
            }},
            "must_do_activities": [
                {{
                    "name": "Activity name",
                    "description": "Brief description",
                    "estimated_cost": "departure location currency XX"
                }}
            ],
            "recommended_duration": {{
                "minimum_days": 5,
                "optimal_days": 7,
                "explanation": "Why this duration is recommended"
            }}
        }}
    ],
    "meta": {{
        "currency": "departure location currency",
        "search_criteria": {{
            "vacation_style": "User's input style",
            "budget_range": "User's input budget",
            "dates": "User's input dates"
        }}
    }}
}}

Important notes:
- All costs should be in departure location currency with currency symbols
- Visa requirements must be current and specific to departure location
- Transportation scores should consider both local and inter-city options
- Safety scores should account for current global situations
- Recommendations should respect budget constraints
- The output must be valid JSON in the exact format specified above
- Use currency code for the currency of the departure location. Do not use symbols.
"""
    return prompt