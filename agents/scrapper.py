import requests

def get_jobs(role, location="India", experience="Fresher"):
    url = "https://jsearch.p.rapidapi.com/search"

    # 1. SMART QUERY: Combine Role + Experience + Location
    # Example: "Python Developer Fresher in India"
    # This acts as a natural filter for entry-level jobs.
    query_text = f"{role} {experience} in {location}"

    querystring = {
        "query": query_text,
        "page": "1",
        "num_pages": "5",
        "country": "in", 
        "date_posted": "week" 
    }

    headers = {
        "X-RapidAPI-Key": "6b07e5f9d6mshf5143992e92e26cp17ea79jsne37d6e582818",
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
    # Example: Search for "Python" jobs for "Freshers" in "India"
    jobs = get_jobs("AI engineer", "India", "Fresher")
    
    print(f"Found {len(jobs)} jobs.")
    
    if jobs:
        job = jobs[0]
        print("--------------------------------------------------")
        print(f"ROLE: {job.get('job_title')}")
        apply_link = job.get('job_apply_link') or job.get('job_google_link') or "No link found"
        print(f"Apply Link: {apply_link}")
        print(f"COMPANY: {job.get('employer_name')}")
        print("--------------------------------------------------")
        
        # This is the FULL REQUIREMENT text Agent 2 will need
        description = job.get('job_description', 'No description found.')
        
        print(f"FULL REQUIREMENTS (First 500 chars):\n{description[:500]}...") 
        print("--------------------------------------------------")