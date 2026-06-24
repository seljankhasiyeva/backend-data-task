# Meta Post Performance Analyzer

A Python-based tool that analyzes Facebook post performance using the Meta Graph API.

## Features
- Fetches last 20 posts with likes and comments data
- Identifies top 3 highest engagement posts
- Calculates average likes by day of week
- Provides engagement summary and conclusions

## Installation

1. Clone the repository:
git clone https://github.com/username/meta-post-analyzer.git
cd meta-post-analyzer

2. Install dependencies:
pip install -r requirements.txt

3. Create a `.env` file and add your token:
USER_TOKEN=your_access_token_here

4. Run:
python main.py

## Sample Output

```bash
Total posts loaded: 20

Top 3 posts by likes:
1. This is test post number 15 - 490 likes, 97 comments
2. This is test post number 12 - 414 likes, 0 comments
3. This is test post number 4 - 379 likes, 69 comments

Average likes by day of week:
Saturday: 377.0 likes
Sunday: 344.0 likes
Wednesday: 253.8 likes
Thursday: 238.3 likes
Tuesday: 195.2 likes
Friday: 185.0 likes
Monday: 97.0 likes

Overall Analysis:
Total posts: 20
Total likes: 4510
Total comments: 889
Average likes/post: 225.5
Average comments/post: 44.5
Best performing day: Saturday
Worst performing day: Monday

Conclusion: Posting on Saturday generates the most engagement.
```

## Notes

### Why Mock Data?
This project was built as part of an internship technical assignment requiring Meta Graph API integration.

During development, I successfully:
- Created a Meta Developer App
- Generated a valid User Access Token
- Connected to the Graph API

However, Meta restricts the `user_posts` permission to apps that have completed Meta's official App Review process. This review requires a live production app, privacy policy, and business verification — which is not feasible within the scope of a short-term internship assignment.

To demonstrate the full analytical functionality of the project, I implemented mock data that simulates real Facebook post data (post content, timestamps, likes, comments). The analysis logic, API integration structure, and code quality remain identical to what would be used with real data.

If `user_posts` permission were granted, replacing the mock data with the following API call would be sufficient:

```python
url = "https://graph.facebook.com/v25.0/me/posts"
params = {
    "fields": "message,created_time,likes.summary(true),comments.summary(true)",
    "limit": 20,
    "access_token": token
}
response = requests.get(url, params=params)
data = response.json()
```