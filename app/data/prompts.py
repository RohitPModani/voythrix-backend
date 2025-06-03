def create_trip_prompt(sanitized_answers: dict) -> str:
    """Create a detailed, optimized prompt for Gemini AI"""
    destinations_str = ", ".join(sanitized_answers["destinations"])
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
- Destinations: {destinations_str}
- Duration: {sanitized_answers["duration"]} {date_info}
- Budget: {sanitized_answers["budget"]}
- Travel Style: {travel_style_str}
- Season: {sanitized_answers["travel_season"] or 'Any season'}
- Pace: {sanitized_answers["pace"]}

**Traveler Details:**
- Group Size: {sanitized_answers["group_size"]}
- Accommodation Preferences: {accommodation_str}
- Transportation Preferences: {sanitized_answers["transportation"]}
- Interests: {interests_str}
- Dietary Restrictions: {dietary_str}
- Special Requirements: {sanitized_answers["special_requirements"]}

**Required Output Components:**
1. Day-by-Day Schedule Requirements:
   - Each day must be broken into morning, afternoon, and evening segments
   - Every activity must include exact timing and duration
   - All locations must have precise addresses or coordinates
   - Include travel time between activities
   - Provide specific cost estimates per activity

2. Multi-Destination Requirements:
   - Clear time allocation between locations
   - Detailed inter-city transportation plans
   - Account for travel time in daily schedules

3. Dining Component Requirements:
   - Multiple options for each meal period
   - Must respect dietary restrictions
   - Include price ranges and cuisine types
   - Specify booking requirements

4. Accommodation Component Requirements:
   - Multiple options per location
   - Detailed amenity lists
   - Location advantages/disadvantages
   - Specific booking information

5. Essential Information Requirements:
   - Emergency contact details
   - Cultural guidelines
   - Weather forecasts
   - Entry requirements
   - Local transportation tips

**Output Format:**
You must return a valid JSON object with exactly this structure:
{{
    "itinerary": {{
        "summary": "Brief engaging overview of the trip",
        "destinations": ["City1, Country1", "City2, Country2"],
        "trip_duration": {{
            "total_days": 7,
            "start_date": "YYYY-MM-DD",
            "end_date": "YYYY-MM-DD"
        }},
        "days": [
            {{
                "day_number": 1,
                "date": "YYYY-MM-DD",
                "destination": "City, Country",
                "themes": ["Theme1", "Theme2"],
                "morning": [
                    {{
                        "time": "HH:MM-HH:MM",
                        "activity": "Activity name",
                        "description": "Detailed description",
                        "location": {{
                            "name": "Location name",
                            "address": "Full address",
                            "coordinates": "lat,long"
                        }},
                        "cost": {{
                            "amount": "XX",
                            "currency": "Currency code"
                        }},
                        "booking_info": {{
                            "required": true/false,
                            "instructions": "Booking details"
                        }},
                        "travel_time_from_previous": "XX minutes",
                        "notes": ["Important note 1", "Important note 2"]
                    }}
                ],
                "afternoon": [
                    // Same structure as morning
                ],
                "evening": [
                    // Same structure as morning
                ],
                "dining": {{
                    "breakfast": [
                        {{
                            "name": "Restaurant name",
                            "cuisine": "Cuisine type",
                            "cost_range": "€€",
                            "address": "Full address",
                            "recommended_dishes": ["Dish1", "Dish2"],
                            "booking_required": true/false,
                            "notes": ["Note1", "Note2"]
                        }}
                    ],
                    "lunch": [
                        // Same structure as breakfast
                    ],
                    "dinner": [
                        // Same structure as breakfast
                    ]
                }},
                "transportation": [
                    {{
                        "type": "Transport type",
                        "route": "From A to B",
                        "cost": {{
                            "amount": "XX",
                            "currency": "Currency code"
                        }},
                        "duration": "XX minutes",
                        "frequency": "Every X minutes",
                        "booking_info": "Booking details if needed"
                    }}
                ],
                "daily_budget_estimate": {{
                    "low": "Amount",
                    "high": "Amount",
                    "currency": "Currency code"
                }},
                "important_notes": ["Note1", "Note2"]
            }}
        ],
        "accommodation": [
            {{
                "city": "City, Country",
                "recommendations": [
                    {{
                        "name": "Property name",
                        "type": "Hotel/Hostel/etc",
                        "price_range": {{
                            "low": "Amount",
                            "high": "Amount",
                            "currency": "Currency code"
                        }},
                        "location": {{
                            "address": "Full address",
                            "coordinates": "lat,long",
                            "proximity_highlights": ["Near X", "Near Y"]
                        }},
                        "amenities": ["Amenity1", "Amenity2"],
                        "pros": ["Pro1", "Pro2"],
                        "cons": ["Con1", "Con2"],
                        "booking_info": {{
                            "platform": "Booking platform",
                            "link": "Booking URL",
                            "notes": "Booking notes"
                        }}
                    }}
                ]
            }}
        ],
        "essential_information": {{
            "emergency_contacts": {{
                "police": "Number",
                "ambulance": "Number",
                "tourist_police": "Number",
            }},
            "cultural_tips": ["Tip1", "Tip2"],
            "packing_list": ["Item1", "Item2"],
            "weather_expectations": {{
                "temperature_range": "XX-YY°C",
                "precipitation": "Expected rainfall",
                "seasonal_notes": "Season-specific information"
            }},
            "visa_requirements": {{
                "type": "Visa type",
                "process": "Application process",
                "duration": "Processing time",
                "cost": {{
                    "amount": "XX",
                    "currency": "Currency code"
                }}
            }},
            "local_sim_wifi_advice": {{
                "sim_advice": "Local sim advice",
                "wifi_advice": "Local wifi advice"
            }},
            "safety_considerations": ["Safety tip 1", "Safety tip 2"],
            "local_transportation": {{
                "options": ["Option1", "Option2"],
                "tips": ["Transport tip 1", "Transport tip 2"],
                "apps": ["Recommended app 1", "Recommended app 2"]
            }},
            "hidden_gems": ["Hidden gem 1", "Hidden gem 2"],
            "photo_worthy_locations": ["Photo worthy location 1", "Photo worthy location 2"],
        }},
        "total_budget_estimate": {{
            "low": "Amount",
            "high": "Amount",
            "currency": "Currency code",
            "breakdown": {{
                "accommodation": "XX%",
                "activities": "XX%",
                "transportation": "XX%",
                "food": "XX%",
                "miscellaneous": "XX%"
            }}
        }}
    }}
}}

Important Requirements:
1. The response MUST be a valid JSON object
2. All monetary values must include amounts and currency codes
3. All times must be in 24-hour format (HH:MM)
4. All locations must include full addresses
5. All dates must be in YYYY-MM-DD format
6. All arrays must contain at least one item
7. All required fields must be present
8. No placeholder or example values should be in the final output
9. Use currency code for the currency of the departure location. Do not use symbols.
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
- Visa Flexibility: {sanitized_answers.get("visa_flexibility", "Any")}  # Whether they want visa-free or visa-on-arrival options
- Special Requirements: {sanitized_answers.get("special_requirements", "None")}
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