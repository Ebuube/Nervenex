#!/usr/bin/python3
"""
Simple test script to verify error pages work correctly
"""

import requests
import sys

def test_error_pages():
    """
    Test the error pages by accessing invalid URLs
    """
    base_url = "http://localhost:5000"
    
    # Test 404 error
    print("Testing 404 error page...")
    try:
        response = requests.get(f"{base_url}/non-existent-page")
        print(f"Status Code: {response.status_code}")
        if "404" in response.text and "Page Not Found" in response.text:
            print("✅ 404 error page working correctly")
        else:
            print("❌ 404 error page not working properly")
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to the server. Make sure the app is running on localhost:5000")
        return False
    
    # Test accessing a protected resource (might trigger 403)
    print("\nTesting potential 403 error...")
    try:
        response = requests.get(f"{base_url}/quiz_history/invalid-user-id")
        print(f"Status Code: {response.status_code}")
        if response.status_code in [403, 404]:
            print("✅ Protected resource handling working")
        else:
            print(f"ℹ️ Response status: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to the server")
        return False
    
    return True

if __name__ == "__main__":
    print("🧪 Testing Nervenex Error Pages")
    print("="*40)
    success = test_error_pages()
    if success:
        print("\n✅ Error page testing completed!")
        print("👉 Start the server with: python3 web_dynamic/app.py")
        print("👉 Then visit http://localhost:5000/test-404 to see the 404 page")
    else:
        print("\n❌ Testing failed. Please start the server first.")
    sys.exit(0 if success else 1)
