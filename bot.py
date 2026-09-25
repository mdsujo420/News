import json
import os
import google.generativeai as genai

# কনফিগারেশন ফাইল লোড করা
with open("config.json", "r", encoding="utf-8") as f:
    config = json.load(f)

# Gemini API সেটআপ
genai.configure(api_key=config["ai_api_key"])

JSON_FILE = "news.json"

def generate_ai_news():
    print("AI is generating a new automated post...")
    
    model = genai.GenerativeModel('gemini-1.5-flash')
    prompt = f"{config['topic_prompt']} Format your response strictly as a valid JSON object with keys 'title' and 'summary'."
    
    try:
        response = model.generate_content(prompt)
        text_data = response.text.strip()
        
        # মার্কডাউন কোড ব্লক থাকলে তা ক্লিন করা
        if text_data.startswith("```json"):
            text_data = text_data[7:-3].strip()
        elif text_data.startswith("```"):
            text_data = text_data[3:-3].strip()
            
        ai_post = json.loads(text_data)
        title = ai_post.get("title", "Breaking News")
        summary = ai_post.get("summary", "Read more for details.")
    except Exception as e:
        print(f"AI Generation Error: {e}")
        return

    # আগের নিউজগুলো লোড করা
    news_list = []
    if os.path.exists(JSON_FILE):
        with open(JSON_FILE, "r", encoding="utf-8") as f:
            try:
                news_list = json.load(f)
            except:
                news_list = []

    # কনফিগার থেকে অ্যাড কোড নিয়ে আসা
    ad_banner = config["ads"]["news_card_ad"]
    
    new_item = {
        "title": title,
        "link": "#",
        "summary": summary,
        "image": "https://via.placeholder.com/600x300/1e1e1e/ff4d4d?text=Adult+News+Today",
        "ad": ad_banner
    }
    
    news_list.insert(0, new_item)
    news_list = news_list[:50] # সর্বোচ্চ ৫০টি পোস্ট সেভ রাখবে

    with open(JSON_FILE, "w", encoding="utf-8") as f:
        json.dump(news_list, f, ensure_ascii=False, indent=4)
    
    print(f"{config['site_name']}: AI post generated and published successfully!")

if __name__ == "__main__":
    generate_ai_news()
