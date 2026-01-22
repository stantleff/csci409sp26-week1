"""
CSCI 409 - API Project
Student: Sawyer Tantleff

Using JSONPlaceholder to practice working with REST APIs in Python.
This script makes 3 different HTTP method requests (GET, POST, PUT),
prints clean output, handles errors, and saves results for submission.
"""

import csv
import json
import sys
from typing import Any, Dict, List

import requests
from requests.exceptions import Timeout, RequestException

BASE_URL = "https://jsonplaceholder.typicode.com"

# Custom headers (requirement: at least one custom header)
HEADERS = {
    "User-Agent": "CSCI409-API-Project/1.0",
    "Accept": "application/json",
}

TIMEOUT_SECONDS = 10


def safe_request(method: str, url: str, **kwargs) -> requests.Response:
    """
    Wrapper around requests so the script doesn't crash in weird ways.
    Handles:
      - timeouts
      - bad status codes (404, 500, etc.)
      - general request errors
    """
    try:
        response = requests.request(method, url, timeout=TIMEOUT_SECONDS, **kwargs)
        response.raise_for_status()
        return response
    except Timeout:
        print(f"[ERROR] Timeout after {TIMEOUT_SECONDS}s -> {method} {url}")
        sys.exit(1)
    except requests.HTTPError as e:
        status = e.response.status_code if e.response is not None else "unknown"
        print(f"[ERROR] HTTP error {status} -> {method} {url}")
        sys.exit(1)
    except RequestException as e:
        print(f"[ERROR] Request failed -> {method} {url}\n{e}")
        sys.exit(1)


def save_json(filename: str, data: Any) -> None:
    """Save data to a JSON file (makes it easy to show your output)."""
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    print(f"[SAVED] {filename}")


def save_posts_csv(filename: str, posts: List[Dict[str, Any]]) -> None:
    """Save posts to CSV so the data is readable in Excel/Sheets."""
    fieldnames = ["userId", "id", "title", "body"]
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for post in posts:
            writer.writerow({k: post.get(k, "") for k in fieldnames})
    print(f"[SAVED] {filename}")


def display_posts(posts: List[Dict[str, Any]], count: int = 5) -> None:
    """Print a small sample so the output isn't just a giant JSON blob."""
    print("\n== Sample Posts ==")
    for p in posts[:count]:
        print(f"- Post {p.get('id')} (User {p.get('userId')}): {p.get('title')}")


def display_users(users: List[Dict[str, Any]], count: int = 5) -> None:
    """Print a few user rows to prove we actually pulled user data."""
    print("\n== Sample Users ==")
    for u in users[:count]:
        name = u.get("name")
        email = u.get("email")
        city = (u.get("address") or {}).get("city")
        print(f"- {name} | {email} | City: {city}")


def main() -> None:
    # ----------------------------
    # Request #1 (GET)
    # ----------------------------
    print("Request #1 (GET): /posts with query param userId=1")
    posts_url = f"{BASE_URL}/posts"

    # Query parameter requirement
    params = {"userId": 1}

    posts_resp = safe_request("GET", posts_url, headers=HEADERS, params=params)
    posts_data = posts_resp.json()

    display_posts(posts_data, count=5)

    # Save outputs (requirement: save response data)
    save_json("posts.json", posts_data)
    save_posts_csv("posts.csv", posts_data)

    # ----------------------------
    # Request #2 (GET)
    # ----------------------------
    print("\nRequest #2 (GET): /users")
    users_url = f"{BASE_URL}/users"

    users_resp = safe_request("GET", users_url, headers=HEADERS)
    users_data = users_resp.json()

    display_users(users_data, count=5)
    save_json("users.json", users_data)

    # ----------------------------
    # Request #3 (POST)
    # ----------------------------
    print("\nRequest #3 (POST): /posts (create a new post)")
    create_url = f"{BASE_URL}/posts"

    new_post_payload = {
        "userId": 1,
        "title": "CSCI 409 API Project Post",
        "body": "This is a test post created using a POST request with requests.",
    }

    created_resp = safe_request("POST", create_url, headers=HEADERS, json=new_post_payload)
    created_post = created_resp.json()

    print("\n== Created Post Response ==")
    print(json.dumps(created_post, indent=2))

    save_json("created_post.json", created_post)

    # ----------------------------
    # Request #4 (PUT)  <-- This makes it 3 different HTTP methods total: GET, POST, PUT
    # ----------------------------
    print("\nRequest #4 (PUT): /posts/1 (update an existing post)")
    update_url = f"{BASE_URL}/posts/1"

    update_payload = {
        "id": 1,
        "userId": 1,
        "title": "Updated Title (PUT)",
        "body": "Updating a post using PUT to satisfy the 3-method requirement.",
    }

    updated_resp = safe_request("PUT", update_url, headers=HEADERS, json=update_payload)
    updated_post = updated_resp.json()

    print("\n== Updated Post Response ==")
    print(json.dumps(updated_post, indent=2))

    save_json("updated_post.json", updated_post)

    print("\nDone. Saved files: posts.json, posts.csv, users.json, created_post.json, updated_post.json")


if __name__ == "__main__":
    main()
