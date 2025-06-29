import os
import json
import together

together.api_key = "tgp_v1_EYCunB4_Q7Vu2irdjoCFDsDsPk4FRWEKe-wxb1aUC-Y" 

def compute_neptune_score(rating, reviews, price):
    price_val = float(str(price).replace("$", ""))
    return round((float(rating) * 20 + int(reviews) * 0.03 - price_val * 0.2), 1)

def load_services():
    all_results = []
    for i in range(1, 4):
        file_path = f"data/source{i}.json"
        if os.path.exists(file_path):
            with open(file_path, "r") as f:
                entries = json.load(f)
                for item in entries:
                    item["neptune_score"] = compute_neptune_score(
                        item.get("rating", 0),
                        item.get("reviews", 0),
                        item.get("price", "$999")
                    )
                    all_results.append(item)
    return sorted(all_results, key=lambda x: x["neptune_score"], reverse=True)

def generate(question, services):
    bullet_points = ""
    for s in services[:5]:
        bullet_points += (
            f"- Name: {s['name']}\n"
            f"  Rating: {s['rating']} ({s['reviews']} reviews)\n"
            f"  Price: {s['price']}\n"
            f"  Booking: {s['booking']}\n"
            f"  Neptune Score: {s['neptune_score']}\n\n"
        )

    prompt = f"""
You are a helpful assistant.

The user asked:
"{question}"

You have access to service listings from multiple trusted sources. Based on the following top 5 dishwasher repair listings, write a helpful, human-readable response. Group results clearly by service and summarize their name, rating, reviews, price, booking link, and Neptune Score. Make the tone clear and informative.

Listings:

{bullet_points}

Answer:
"""

    response = together.Complete.create(
        model="meta-llama/Llama-3.3-70B-Instruct-Turbo-Free",
        prompt=prompt,
        max_tokens=512,
        temperature=0.7,
        top_k=50,
        top_p=0.9,
        repetition_penalty=1.1,
    )

    return response["choices"][0]["text"].strip()

def answer_query(question):
    services = load_services()
    if not services:
        return "No service data available."

    top_services = services[:5]
    return generate(question, top_services)