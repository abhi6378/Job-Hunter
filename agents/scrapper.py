import requests

# 1. Map common names to JSearch 2-letter ISO codes
COUNTRY_CODES = {
    "india": "in",
    "usa": "us",
    "united states": "us",
    "uk": "gb",
    "united kingdom": "gb",
    "canada": "ca",
    "australia": "au",
    "germany": "de",
    "france": "fr"
}

def get_jobs(role, city=None, country="India", experience_type="fresher"):
    url = "https://jsearch.p.rapidapi.com/search"

    # --- 1. HANDLE COUNTRY CODE ---
    # Convert "India" -> "in", default to "us" if unknown
    country_code = COUNTRY_CODES.get(country.lower(), "us")

    # --- 2. BUILD THE QUERY STRING ---
    # If city is provided: "Python Developer in Jaipur, India"
    # If no city: "Python Developer in India"
    if city:
        location_text = f"{city}, {country}"
    else:
        location_text = country

    # --- 3. KEYWORD INJECTION FOR EXPERIENCE ---
    if experience_type == "fresher":
        query_text = f"{role} (Fresher OR Intern OR Junior) in {location_text}"
        api_requirements = None
    elif experience_type == "experienced":
        query_text = f"Senior {role} in {location_text}"
        api_requirements = "more_than_3_years_experience"
    else:
        query_text = f"{role} in {location_text}"
        api_requirements = None

    print(f"🔎 Searching: '{query_text}' (Region: {country_code.upper()})...")

    querystring = {
        "query": query_text,
        "page": "1",
        "num_pages": "1",
        "country": country_code, # Strict country filter
        "date_posted": "month"
    }
    
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
    # --- TEST CASES ---
    
    # Case 1: Specific City in India
    print("--- CASE 1: Jaipur, India ---")
    jobs_jaipur = get_jobs("Python Developer", city="Jaipur", country="India")
    if jobs_jaipur:
        print(f"Found: {jobs_jaipur[0].get('job_title')} at {jobs_jaipur[0].get('employer_name')} ({jobs_jaipur[0].get('job_city')})")

    # Case 2: Whole Country (India)
    print("\n--- CASE 2: All India ---")
    jobs_india = get_jobs("Python Developer", city=None, country="India")
    print(f"Found {len(jobs_india)} jobs in India.")

    # Case 3: USA (Remote or Specific)
    print("\n--- CASE 3: USA ---")
    jobs_usa = get_jobs("React Developer", city="New York", country="USA")
    if jobs_usa:
        print(f"Found: {jobs_usa[0].get('job_title')} in {jobs_usa[0].get('job_city')}")