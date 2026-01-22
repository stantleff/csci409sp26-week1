# CSCI 409 - Public API Script Project

## API I Chose
I used **JSONPlaceholder**, which is a free public REST API meant for testing/practice.
Base URL: https://jsonplaceholder.typicode.com

## What My Script Does
This script uses Python requests library to make multiple API calls, pull the response data, and save it so it can be submitted as proof.

It uses three different methods:
1. **GET** /posts (with a query parameter userId=1)
2. **GET** /users
3. **POST** /posts (creates a new post)
4. **PUT** /posts/1 (updates an existing post)

I also included:
- Custom request headers (User-Agent + Accept)
- Basic error handling for timeouts and HTTP errors (like 404/500)
- Clean printed output so it’s readable
- Saved output files for submission


## Output Files It Creates
- posts.json
- posts.csv
- users.json
- created_post.json
- updated_post.json

## Challenges
The biggest thing was making sure I was meeting the requirement of three different methods. Also making sure the script fails in a readable way when something goes wrong instead of throwing a random error.
