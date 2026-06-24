from flask import Flask
from dotenv import load_dotenv
import os
import random
from datetime import datetime, timedelta
from collections import defaultdict

load_dotenv()
app = Flask(__name__)

@app.route("/")
def analyze():
    random.seed(42)
    posts = []
    for i in range(20):
        date = datetime.now() - timedelta(days=random.randint(1, 90))
        posts.append({
            "id": f"post_{i+1}",
            "message": f"This is test post number {i+1}",
            "created_time": date.strftime("%Y-%m-%dT%H:%M:%S"),
            "day_of_week": date.strftime("%A"),
            "likes": random.randint(0, 500),
            "comments": random.randint(0, 100)
        })

    top_3 = sorted(posts, key=lambda x: x["likes"], reverse=True)[:3]

    day_likes = defaultdict(list)
    for post in posts:
        day_likes[post["day_of_week"]].append(post["likes"])
    day_avg = {day: sum(likes)/len(likes) for day, likes in day_likes.items()}
    day_avg_sorted = sorted(day_avg.items(), key=lambda x: x[1], reverse=True)

    total_likes = sum(p["likes"] for p in posts)
    total_comments = sum(p["comments"] for p in posts)
    best_day = day_avg_sorted[0][0]
    worst_day = day_avg_sorted[-1][0]

    html = f"""
    <h1>Meta Post Performance Analyzer</h1>
    <h2>Top 3 Posts by Likes</h2>
    <ol>
    {"".join(f"<li>{p['message']} - {p['likes']} likes, {p['comments']} comments</li>" for p in top_3)}
    </ol>
    <h2>Average Likes by Day of Week</h2>
    <ul>
    {"".join(f"<li>{day}: {avg:.1f} likes</li>" for day, avg in day_avg_sorted)}
    </ul>
    <h2>Overall Analysis</h2>
    <p>Total posts: {len(posts)}</p>
    <p>Total likes: {total_likes}</p>
    <p>Total comments: {total_comments}</p>
    <p>Average likes/post: {total_likes/len(posts):.1f}</p>
    <p>Best performing day: <b>{best_day}</b></p>
    <p>Worst performing day: <b>{worst_day}</b></p>
    <p><b>Conclusion: Posting on {best_day} generates the most engagement.</b></p>
    """
    return html

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)