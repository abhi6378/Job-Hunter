import requests

def get_jobs(role, location="India", experience_type="fresher"):
    url = "https://jsearch.p.rapidapi.com/search"

    # --- 1. SMART KEYWORD INJECTION ---
    # Instead of trusting the API's hidden filter, we put the words right in the search.
    if experience_type == "fresher":
        # Search for: "Python Developer Fresher OR Intern in India"
        query_text = f"{role} (Fresher OR Intern OR Junior OR Entry Level) in {location}"
        api_requirements = None # Don't use strict filter, it kills results
        
    elif experience_type == "experienced":
        query_text = f"Senior {role} in {location}"
        api_requirements = "more_than_3_years_experience" # This works fine for seniors
        
    else:
        # Default/Intermediate
        query_text = f"{role} in {location}"
        api_requirements = None

    print(f"🔎 Searching for: '{query_text}'...")

    querystring = {
        "query": query_text,
        "page": "1",
        "num_pages": "1",
        "country": "in",
        "date_posted": "month" # Relaxed from 'week' to 'month' to find more opportunities
    }
    
    # Only add the strict requirement if we are 100% sure (like for seniors)
    if api_requirements:
        querystring["job_requirements"] = api_requirements

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
    # TEST 1: Find Fresher Jobs (Now using Keyword Injection)
    print("--- 🔍 SEARCHING FOR FRESHER JOBS ---")
    fresher_jobs = get_jobs("Python Developer", "India", "fresher")
    print(f"Found {len(fresher_jobs)} fresher jobs.")
    
    if fresher_jobs:
        job = fresher_jobs[0]
        print(f"Title: {job.get('job_title')}")
        print(f"Company: {job.get('employer_name')}")
        # Check if we got a link this time
        link = job.get('job_apply_link') or job.get('job_google_link') or "No link"
        print(f"Link: {link}")

    # TEST 2: Find Senior Jobs
    print("\n--- 🔍 SEARCHING FOR SENIOR JOBS ---")
    senior_jobs = get_jobs("Python Developer", "India", "experienced")
    print(f"Found {len(senior_jobs)} senior jobs.")