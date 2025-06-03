"""
Questions configuration for the trip planner API.
Each section contains carefully curated questions to gather user preferences.
"""

TRIP_QUESTIONS = {
    "trip_basics": {
        "title": "Trip Basics",
        "description": "Tell us about your trip fundamentals",
        "fields": [
            {
                "id": "start_location",
                "question": "Where will you start your trip?",
                "description": "Your starting point, e.g., 'New York City'",
                "type": "text",
                "placeholder": "e.g., New York City",
                "required": True,
            },
            {
                "id": "destinations",
                "question": "Which destinations are you dreaming of visiting?",
                "description": "List 1-5 places you'd like to visit",
                "type": "tags",
                "placeholder": "e.g., Paris, Tokyo, Bali",
                "max": 5,
                "required": True
            },
            {
                "id": "start_date",
                "question": "When do you plan to travel?",
                "description": "For season-specific recommendations",
                "type": "date",
                "required": True
            },
            {
                "id": "end_date",
                "question": "When will your trip end?",
                "description": "For season-specific recommendations",
                "type": "date",
                "required": True
            }
        ]
    },
    "trip_preferences": {
        "title": "Trip Preferences",
        "description": "Let's understand your trip preferences",
        "fields": [
            {
                "id": "group_size",
                "question": "Who's traveling with you?",
                "type": "select",
                "options": [
                    {"value": "solo", "label": "Solo traveler", "icon": "person"},
                    {"value": "couple", "label": "Couple", "icon": "heart"},
                    {"value": "friends", "label": "Friends (3-5)", "icon": "user-group"},
                    {"value": "family", "label": "Family", "icon": "children"},
                    {"value": "large_group", "label": "Large Group (6+)", "icon": "users"}
                ],
                "required": True
            },
            {
                "id": "budget",
                "question": "What's your daily budget per person?",
                "type": "select",
                "options": [
                    {"value": "Budget", "label": "Budget ($0-50/day)", "description": "Hostels, street food, public transport"},
                    {"value": "Mid-range", "label": "Mid-range ($50-150/day)", "description": "3-star hotels, mix of dining options"},
                    {"value": "Luxury", "label": "Luxury ($150-500/day)", "description": "4-5 star hotels, fine dining"},
                    {"value": "Ultra-luxury", "label": "Ultra-luxury ($500+/day)", "description": "Best hotels, private tours"}
                ],
                "required": True
            },
            {
                "id": "pace",
                "question": "What pace do you prefer?",
                "type": "select",
                "options": [
                    {"value": "Relaxed", "label": "Relaxed", "description": "Plenty of downtime"},
                    {"value": "Moderate", "label": "Moderate", "description": "Balanced pace with breaks"},
                    {"value": "Fast-paced", "label": "Fast-paced", "description": "Pack in as much as possible"}
                ],
                "default": "Moderate",
                "required": True
            }
        ]
    },
    "accommodation_and_transportation": {
        "title": "Accommodation and Transportation Preferences",
        "description": "Tell us about your preferred places to stay and how you like to get around",
        "fields": [
            {
                "id": "accommodation",
                "question": "What types of accommodation do you prefer?",
                "description": "Select up to 2",
                "type": "multi-select",
                "options": [
                    {"value": "hotels", "label": "Hotels", "icon": "hotel"},
                    {"value": "hostels", "label": "Hostels", "icon": "bed"},
                    {"value": "vacation_rentals", "label": "Vacation Rentals", "icon": "home"},
                    {"value": "resorts", "label": "Resorts", "icon": "umbrella-beach"},
                    {"value": "boutique", "label": "Boutique Hotels", "icon": "star"},
                    {"value": "camping", "label": "Camping", "icon": "campground"},
                    {"value": "ryokan", "label": "Ryokan (Japan)", "icon": "torii-gate"},
                    {"value": "homestay", "label": "Homestay", "icon": "people-roof"}
                ],
                "max": 2,
                "required": True
            },
            {
                "id": "transportation",
                "question": "How do you prefer to get around?",
                "type": "select",
                "options": [
                    {"value": "public", "label": "Public Transport", "description": "Buses, trains, metro"},
                    {"value": "walking", "label": "Walking & Biking", "description": "For compact cities"},
                    {"value": "rental", "label": "Rental Car", "description": "For road trips or rural areas"},
                    {"value": "taxis", "label": "Taxis/Ride-sharing", "description": "Convenience over cost"},
                    {"value": "tours", "label": "Organized Tours", "description": "Guided experiences"},
                    {"value": "mix", "label": "Mix of Options", "description": "Flexible approach"}
                ],
                "required": True
            }
        ]
    },
    "travel_style": {
        "title": "Travel Style",
        "description": "What kind of experiences interest you?",
        "fields": [
            {
                "id": "travel_style",
                "question": "Which travel styles describe you best?",
                "description": "Select up to 3",
                "type": "multi-select",
                "options": [
                    {"value": "adventure", "label": "Adventure & Outdoor", "icon": "hiking"},
                    {"value": "cultural", "label": "Cultural & Historical", "icon": "museum"},
                    {"value": "relaxation", "label": "Relaxation & Wellness", "icon": "spa"},
                    {"value": "food", "label": "Food & Wine", "icon": "utensils"},
                    {"value": "nightlife", "label": "Nightlife & Entertainment", "icon": "cocktail"},
                    {"value": "family", "label": "Family-friendly", "icon": "children"},
                    {"value": "romantic", "label": "Romantic", "icon": "heart"},
                    {"value": "backpacking", "label": "Budget Backpacking", "icon": "backpack"},
                    {"value": "luxury", "label": "Luxury Experience", "icon": "diamond"},
                    {"value": "offbeat", "label": "Off-the-beaten-path", "icon": "compass"}
                ],
                "max": 3,
                "required": True
            },
            {
                "id": "interests",
                "question": "What are your main interests?",
                "description": "Select up to 5 to prioritize activities",
                "type": "multi-select",
                "options": [
                    {"value": "museums", "label": "Museums & Art", "icon": "palette"},
                    {"value": "beaches", "label": "Beaches & Water Sports", "icon": "water"},
                    {"value": "hiking", "label": "Hiking & Nature", "icon": "mountain"},
                    {"value": "shopping", "label": "Shopping & Markets", "icon": "shopping-bag"},
                    {"value": "photography", "label": "Photography", "icon": "camera"},
                    {"value": "food", "label": "Local Cuisine", "icon": "utensils"},
                    {"value": "nightlife", "label": "Nightlife", "icon": "martini-glass"},
                    {"value": "history", "label": "Historical Sites", "icon": "landmark"},
                    {"value": "adventure", "label": "Adventure Sports", "icon": "parachute-box"},
                    {"value": "wildlife", "label": "Wildlife & Safaris", "icon": "paw"},
                    {"value": "architecture", "label": "Architecture", "icon": "building"},
                    {"value": "festivals", "label": "Music & Festivals", "icon": "music"}
                ],
                "max": 5,
                "required": True
            }
        ]
    },
    "special_requirements": {
        "title": "Special Requirements",
        "description": "Help us accommodate your specific needs",
        "fields": [
            {
                "id": "dietary_restrictions",
                "question": "Any dietary restrictions?",
                "description": "For restaurant recommendations",
                "type": "multi-select",
                "options": [
                    {"value": "none", "label": "None"},
                    {"value": "vegetarian", "label": "Vegetarian"},
                    {"value": "vegan", "label": "Vegan"},
                    {"value": "gluten_free", "label": "Gluten-free"},
                    {"value": "halal", "label": "Halal"},
                    {"value": "kosher", "label": "Kosher"},
                    {"value": "nut_allergy", "label": "Nut Allergy"},
                    {"value": "seafood_allergy", "label": "Seafood Allergy"},
                    {"value": "lactose_intolerant", "label": "Lactose Intolerant"}
                ],
                "required": False
            },
            {
                "id": "special_requirements",
                "question": "Any special requirements?",
                "description": "Tell us about any specific activities or requirements",
                "type": "text",
                "placeholder": "e.g., I want to go skydiving, need wheelchair accessibility",
                "required": False
            }
        ]
    }
} 

VACATION_QUESTIONS = {
    "vacation_basics": {
        "title": "Vacation Basics",
        "description": "Tell us about your vacation fundamentals",
        "fields": [
            {
                "id": "departure_location",
                "question": "Where will you start your vacation?",
                "description": "Your starting point, e.g., 'New York City'",
                "type": "text",
                "placeholder": "e.g., New York City",
                "required": True
            },
            {
                "id": "preferred_region",
                "question": "What region or country are you interested in?",
                "type": "text",
                "placeholder": "e.g., Europe, Asia, Africa",
                "required": True
            },
            {
                "id": "start_date",
                "question": "When do you plan to travel?",
                "description": "For season-specific recommendations",
                "type": "date",
                "required": True
            },
            {
                "id": "end_date",
                "question": "When will your vacation end?",
                "description": "For season-specific recommendations",
                "type": "date",
                "required": True
            }
        ]
    },
    "vacation_preferences": {
        "title": "Vacation Preferences",
        "description": "Let's understand your vacation style and preferences",
        "fields": [
            {
                "id": "group_size",
                "question": "Who's traveling with you?",
                "type": "select",
                "options": [
                    {"value": "solo", "label": "Solo traveler", "icon": "person"},  
                    {"value": "couple", "label": "Couple", "icon": "heart"},
                    {"value": "friends", "label": "Friends (3-5)", "icon": "user-group"},
                    {"value": "family", "label": "Family", "icon": "children"},
                    {"value": "large_group", "label": "Large Group (6+)", "icon": "users"}
                ],
                "required": True
            },
            {
                "id": "budget",
                "question": "What's your total budget for the trip per person?",
                "type": "select",
                "options": [
                    {"value": "Budget", "label": "Budget ($0-50/day)", "description": "Budget-friendly trip includes hostels, street food, public transport"},
                    {"value": "Mid-range", "label": "Mid-range ($50-150/day)", "description": "Moderate budget trip includes 3-star hotels, mix of dining options"},
                    {"value": "Luxury", "label": "Luxury ($150-500/day)", "description": "Luxury trip includes 4-5 star hotels, fine dining"},
                    {"value": "Ultra-luxury", "label": "Ultra-luxury ($500+/day)", "description": "Ultra-luxury trip includes best hotels, private tours"}
                ],
                "required": True
            },
            {
                "id": "vacation_style",
                "question": "What kind of vacation are you looking for?",
                "description": "Select up to 3",
                "type": "multi-select",
                "options": [
                    {"value": "beach", "label": "Beach", "icon": "umbrella-beach"},
                    {"value": "adventure", "label": "Adventure", "icon": "hiking"},
                    {"value": "culture", "label": "Culture", "icon": "museum"},
                    {"value": "romantic", "label": "Romantic", "icon": "heart"},
                    {"value": "family", "label": "Family", "icon": "children"},
                    {"value": "party", "label": "Party", "icon": "cocktail"}   
                ],
                "max": 3,
                "required": True
            }
        ]
    },
    "travel_requirements": {
        "title": "Travel Requirements",
        "description": "Help us plan according to your travel requirements",
        "fields": [
            {
                "id": "visa_flexibility",
                "question": "Do you need visa-free or visa-on-arrival options?",
                "type": "select",
                "options": [
                    {"value": "visa-free", "label": "Visa-free", "description": "Visa-free travel"},
                    {"value": "visa-on-arrival", "label": "Visa-on-arrival", "description": "Visa-on-arrival travel"},
                    {"value": "any", "label": "Any", "description": "I'm flexible"}
                ],
                "required": True
            },
            {
                "id": "dietary_restrictions",
                "question": "Any dietary restrictions?",
                "description": "For restaurant recommendations",
                "type": "multi-select",
                "options": [
                    {"value": "none", "label": "None"},
                    {"value": "vegetarian", "label": "Vegetarian"},
                    {"value": "vegan", "label": "Vegan"},
                    {"value": "gluten_free", "label": "Gluten-free"},
                    {"value": "halal", "label": "Halal"},
                    {"value": "kosher", "label": "Kosher"}
                ],
                "required": False
            },
            {
                "id": "special_requirements",
                "question": "Any special requirements or activities?",
                "description": "Tell us about any specific activities or requirements",
                "type": "text",
                "placeholder": "e.g., I want to go skydiving, need wheelchair accessibility",
                "required": False
            }
        ]
    }
}