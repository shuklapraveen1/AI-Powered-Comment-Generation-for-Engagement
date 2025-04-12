import os, openai
from textblob import TextBlob
openai.api_key = os.getenv("OPENAI_API_KEY")
def analyze_post(post):
    return openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": f"Analyze this LinkedIn post (tone, key points, engagement potential):\n\n{post}"}]
    )['choices'][0]['message']['content']
def generate_comment(post, style="professional"):
    return openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": f"Write a {style} LinkedIn comment (2-3 sentences) for this post:\n{post}"}]
    )['choices'][0]['message']['content']
def evaluate_comment(comment):
    analysis = TextBlob(comment)
    return "Approved" if analysis.sentiment.polarity > -0.1 and 10 <= len(comment.split()) <= 35 else "Needs revision"
def engage_with_post(post, comment_style="professional"):
    analysis = analyze_post(post)
    comment = generate_comment(post, comment_style)
    evaluation = evaluate_comment(comment)
    print(f"Analysis:\n{analysis}\n\nComment:\n{comment}\nStatus: {evaluation}")
    with open("linkedin_engagement.txt", "a") as f:
        f.write(f"\nPost:\n{post}\nComment:\n{comment}\nStatus: {evaluation}\n")
if __name__ == "__main__":
    engage_with_post(input("Paste LinkedIn post: "))