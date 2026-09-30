from .catalog import search_links

def home_recommendations(data: dict) -> dict:
    rooms = data["rooms"]
    per_room = data["budget"] // len(rooms)
    recs = []
    for room in rooms:
        recs.append({
            "name": f"{data['style']} {room} essentials",
            "category": room,
            "estimated_price": f"₹{int(per_room*0.5):,} - ₹{int(per_room*0.8):,}",
            "reason": f"A practical {data['style'].lower()} option for the {room.lower()} within the room allocation.",
            "links": search_links(f"{data['style']} {room} decor", ["Amazon", "IKEA", "Flipkart"]),
        })
    return {
        "source": "fallback",
        "summary": f"Home plan for {len(rooms)} room(s) within ₹{data['budget']:,}.",
        "allocations": [{"category": r, "amount": per_room} for r in rooms],
        "recommendations": recs,
        "tips": ["Buy essentials first.", "Compare dimensions and return policies.", "Keep a small buffer for delivery and installation."],
    }

def party_recommendations(data: dict) -> dict:
    budget = data["budget"]
    food = int(budget*0.50)
    venue = int(budget*0.25)
    decoration = int(budget*0.15)
    buffer = budget-food-venue-decoration
    return {
        "source": "fallback",
        "summary": f"{data['event_type']} plan for {data['guests']} guests within ₹{budget:,}.",
        "allocations": [
            {"category":"Food/Catering", "amount":food},
            {"category":"Venue", "amount":venue},
            {"category":"Decoration", "amount":decoration},
            {"category":"Entertainment/Buffer", "amount":buffer},
        ],
        "recommendations": [
            {"name":f"{data['event_type']} catering", "category":"Food/Catering", "estimated_price":f"₹{food:,}", "reason":"Largest allocation is kept for food because guest count directly affects catering cost.", "links":search_links(f"{data['event_type']} catering {data['guests']} guests {data['location']}",["Swiggy","Zomato"])},
            {"name":"Event venue options", "category":"Venue", "estimated_price":f"₹{venue:,}", "reason":"Venue spending is kept below the food allocation to protect the overall budget.", "links":search_links(f"{data['event_type']} venue {data['location']}",["OYO"])},
            {"name":"Party decoration", "category":"Decoration", "estimated_price":f"₹{decoration:,}", "reason":"A controlled decoration budget leaves room for essential event costs.", "links":search_links(f"{data['event_type']} decoration",["Amazon","Flipkart"])},
        ],
        "tips":["Confirm venue capacity and included services.","Ask caterers for per-person pricing.","Keep the final buffer for unexpected expenses."],
    }

def jewelry_recommendations(data: dict) -> dict:
    budget = data["budget"]
    main = int(budget*0.70)
    accessories = int(budget*0.20)
    buffer = budget-main-accessories
    query = f"{data['style']} {data['metal']} jewelry {data['occasion']}"
    return {
        "source":"fallback",
        "summary":f"Jewelry plan for {data['occasion']} within ₹{budget:,}.",
        "allocations":[{"category":"Main jewelry","amount":main},{"category":"Accessories","amount":accessories},{"category":"Buffer","amount":buffer}],
        "recommendations":[
            {"name":f"{data['style']} {data['metal']} jewelry", "category":"Main jewelry", "estimated_price":f"₹{int(budget*0.30):,} - ₹{int(budget*0.70):,}", "reason":"Matches the selected occasion, style and metal preference.", "links":search_links(query,["Amazon","Flipkart"])},
            {"name":"Matching earrings/accessories", "category":"Accessories", "estimated_price":f"₹{int(budget*0.10):,} - ₹{int(budget*0.20):,}", "reason":"Adds coordination while keeping the main jewelry within budget.", "links":search_links(f"{data['style']} matching earrings {data['occasion']}",["Amazon","Flipkart"])},
        ],
        "tips":["Consider outfit neckline and colors.","Verify material, purity and invoice details for precious metals.","Use the buffer for matching accessories or delivery charges."],
    }
