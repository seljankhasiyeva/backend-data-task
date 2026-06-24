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

    html = html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Meta Post Performance Analyzer</title>
    <style>
        body {{ font-family: Arial, sans-serif; max-width: 800px; margin: 40px auto; padding: 20px; background: #f5f5f5; }}
        h1 {{ color: #1877f2; border-bottom: 3px solid #1877f2; padding-bottom: 10px; }}
        h2 {{ color: #333; margin-top: 30px; }}
        .card {{ background: white; border-radius: 10px; padding: 20px; margin: 15px 0; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }}
        .post-item {{ padding: 10px; border-left: 4px solid #1877f2; margin: 10px 0; background: #f0f7ff; }}
        .stat {{ display: inline-block; background: #1877f2; color: white; padding: 8px 16px; border-radius: 20px; margin: 5px; }}
        .best {{ color: #28a745; font-weight: bold; }}
        .worst {{ color: #dc3545; font-weight: bold; }}
        .day-bar {{ background: #1877f2; height: 20px; border-radius: 4px; margin: 5px 0; }}
        table {{ width: 100%; border-collapse: collapse; }}
        td, th {{ padding: 10px; text-align: left; border-bottom: 1px solid #eee; }}
        th {{ background: #1877f2; color: white; }}
    </style>
</head>
<body>
    <h1>Meta Post Performance Analyzer</h1>

    <div class="card">
        <h2>Top 3 Posts by Likes</h2>
        {"".join(f'<div class="post-item"><b>#{i+1}</b> {p["message"]} &nbsp; <span class="stat">{p["likes"]} likes</span> <span class="stat">{p["comments"]} comments</span></div>' for i, p in enumerate(top_3))}
    </div>

    <div class="card">
        <h2>Average Likes by Day of Week</h2>
        <table>
            <tr><th>Day</th><th>Average Likes</th><th>Performance</th></tr>
            {"".join(f'<tr><td>{day}</td><td>{avg:.1f}</td><td><div class="day-bar" style="width:{int(avg/4)}px"></div></td></tr>' for day, avg in day_avg_sorted)}
        </table>
    </div>

    <div class="card">
        <h2>Overall Analysis</h2>
        <p>Total posts: <b>{len(posts)}</b></p>
        <p>Total likes: <b>{total_likes}</b></p>
        <p>Total comments: <b>{total_comments}</b></p>
        <p>Average likes/post: <b>{total_likes/len(posts):.1f}</b></p>
        <p>Best performing day: <span class="best">{best_day}</span></p>
        <p>Worst performing day: <span class="worst">{worst_day}</span></p>
        <p><b>Conclusion: Posting on {best_day} generates the most engagement.</b></p>
    </div>
</body>
</html>
"""
    return html

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)