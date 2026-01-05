import requests

def get_jobs(role, location="India", experience_type="fresher"):
    url = "https://jsearch.p.rapidapi.com/search"

    # 1. Map user inputs to JSearch specific requirements
    # Options available in API: 'no_experience', 'under_3_years_experience', 'more_than_3_years_experience'
    
    api_requirement = "no_experience" # Default for fresher
    query_modifier = "Fresher"

    if experience_type == "experienced":
        api_requirement = "more_than_3_years_experience"
        query_modifier = "Senior"
    elif experience_type == "intermediate":
        api_requirement = "under_3_years_experience"
        query_modifier = "Associate"

    # 2. Construct the smart query
    # We add the modifier to the text query AND use the strict API filter
    query_text = f"{query_modifier} {role} in {location}"

    querystring = {
        "query": query_text,
        "page": "1",
        "num_pages": "1",
        "country": "in",
        "date_posted": "week",
        "job_requirements": api_requirement  # <--- The new strict filter
    }

    headers = {
        "X-RapidAPI-Key": "YOUR_ACTUAL_API_KEY_HERE",
        "X-RapidAPI-Host": "jsearch.p.rapidapi.com"
    }

    try:
        response = requests.get(url, headers=headers, params=querystring)
        data = response.json()
        
        if "data" in data:
            return data["data"]
        else:
            return []
            
    except Exception as e:
        print(f"Error: {e}")
        return []

if __name__ == "__main__":
    # TEST 1: Find Fresher Jobs
    print("--- 🔍 SEARCHING FOR FRESHER JOBS ---")
    fresher_jobs = get_jobs("Python Developer", "India", "fresher")
    print(f"Found {len(fresher_jobs)} fresher jobs.")
    
    if fresher_jobs:
        print(f"Example: {fresher_jobs[0].get('job_title')} at {fresher_jobs[0].get('employer_name')}")

    # TEST 2: Find Experienced Jobs
    print("\n--- 🔍 SEARCHING FOR SENIOR JOBS ---")
    senior_jobs = get_jobs("Python Developer", "India", "experienced")
    print(f"Found {len(senior_jobs)} senior jobs.")
    
    if senior_jobs:
        print(f"Example: {senior_jobs[0].get('job_title')} at {senior_jobs[0].get('employer_name')}")