"""Script to seed the backend with sample data for testing."""
import requests
import json

BASE_URL = "http://localhost:8000/api/v1"

def create_sample_interviews():
    """Create sample interviews with participants and code."""
    
    print("🌱 Seeding backend with sample data...\n")
    
    # Sample 1: Python Interview
    print("Creating Python interview...")
    response = requests.post(
        f"{BASE_URL}/interviews",
        json={
            "title": "Senior Python Developer Interview",
            "language": "python",
            "creatorName": "Alice Johnson"
        }
    )
    python_interview = response.json()
    python_id = python_interview["id"]
    print(f"✅ Created interview: {python_id}")
    
    # Add a candidate
    requests.post(
        f"{BASE_URL}/interviews/{python_id}/join",
        json={
            "participantName": "Bob Smith",
            "role": "candidate"
        }
    )
    print("✅ Added candidate: Bob Smith")
    
    # Add some code
    python_code = """def fibonacci(n):
    \"\"\"Calculate the nth Fibonacci number.\"\"\"
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

# Test the function
print(fibonacci(10))
"""
    participant_id = python_interview["participants"][0]["id"]
    requests.put(
        f"{BASE_URL}/interviews/{python_id}/code",
        json={
            "code": python_code,
            "participantId": participant_id
        }
    )
    print("✅ Added Python code\n")
    
    # Sample 2: JavaScript Interview
    print("Creating JavaScript interview...")
    response = requests.post(
        f"{BASE_URL}/interviews",
        json={
            "title": "Frontend Engineer - React Interview",
            "language": "javascript",
            "creatorName": "Carol Davis"
        }
    )
    js_interview = response.json()
    js_id = js_interview["id"]
    print(f"✅ Created interview: {js_id}")
    
    # Add candidates
    requests.post(
        f"{BASE_URL}/interviews/{js_id}/join",
        json={
            "participantName": "David Lee",
            "role": "candidate"
        }
    )
    print("✅ Added candidate: David Lee")
    
    # Add some code
    js_code = """// Implement a debounce function
function debounce(func, delay) {
    let timeoutId;
    return function(...args) {
        clearTimeout(timeoutId);
        timeoutId = setTimeout(() => {
            func.apply(this, args);
        }, delay);
    };
}

// Test it
const log = debounce(() => console.log('Hello!'), 1000);
log();
"""
    participant_id = js_interview["participants"][0]["id"]
    requests.put(
        f"{BASE_URL}/interviews/{js_id}/code",
        json={
            "code": js_code,
            "participantId": participant_id
        }
    )
    print("✅ Added JavaScript code\n")
    
    # Sample 3: TypeScript Interview
    print("Creating TypeScript interview...")
    response = requests.post(
        f"{BASE_URL}/interviews",
        json={
            "title": "Full Stack TypeScript Developer",
            "language": "typescript",
            "creatorName": "Eve Martinez"
        }
    )
    ts_interview = response.json()
    ts_id = ts_interview["id"]
    print(f"✅ Created interview: {ts_id}")
    
    # Add some code
    ts_code = """interface User {
    id: number;
    name: string;
    email: string;
}

function greetUser(user: User): string {
    return `Hello, ${user.name}!`;
}

const user: User = {
    id: 1,
    name: "John Doe",
    email: "john@example.com"
};

console.log(greetUser(user));
"""
    participant_id = ts_interview["participants"][0]["id"]
    requests.put(
        f"{BASE_URL}/interviews/{ts_id}/code",
        json={
            "code": ts_code,
            "participantId": participant_id
        }
    )
    print("✅ Added TypeScript code\n")
    
    # Summary
    print("=" * 50)
    print("✨ Sample data created successfully!\n")
    print("Created interviews:")
    print(f"1. Python Interview: {python_id}")
    print(f"2. JavaScript Interview: {js_id}")
    print(f"3. TypeScript Interview: {ts_id}")
    print("\nYou can now test the frontend with this data!")
    print(f"View all interviews: {BASE_URL}/interviews")
    print("=" * 50)

if __name__ == "__main__":
    try:
        create_sample_interviews()
    except requests.exceptions.ConnectionError:
        print("❌ Error: Could not connect to backend server.")
        print("Make sure the server is running: uv run uvicorn app.main:app --port 8000")
    except Exception as e:
        print(f"❌ Error: {e}")
