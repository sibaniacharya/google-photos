import json
import os
from PIL import Image, ImageDraw, ImageFont

scenarios = [
    # 1. Beach / coastal trips
    {"id": "001", "loc": "Amalfi Coast", "ppl": ["friends"], "evt": "beach trip", "obj": ["yellow car"], "vis": "friends near a yellow vintage car overlooking the sea at sunset", "ctx": "summer road trip", "time": "sunset, summer"},
    {"id": "002", "loc": "Malibu", "ppl": ["friends"], "evt": "beach trip", "obj": ["surfboard"], "vis": "group of friends surfing on a sunny day", "ctx": "summer vacation", "time": "daytime, summer"},
    {"id": "003", "loc": "Miami Beach", "ppl": [], "evt": "beach walk", "obj": ["seashells"], "vis": "empty beach with seashells at sunrise", "ctx": "morning walk", "time": "sunrise"},
    {"id": "004", "loc": "Coastal Highway", "ppl": ["Maya", "Leo"], "evt": "road trip", "obj": ["yellow car", "sunglasses"], "vis": "driving a yellow car along the coast", "ctx": "weekend getaway", "time": "afternoon"},
    {"id": "005", "loc": "Beachside Restaurant", "ppl": ["friends", "family"], "evt": "dinner", "obj": ["wine glasses", "seafood"], "vis": "seafood dinner by the beach at sunset", "ctx": "birthday celebration", "time": "sunset, evening"},
    
    # 2. Travel
    {"id": "006", "loc": "Paris", "ppl": ["wife"], "evt": "vacation", "obj": ["Eiffel Tower", "camera"], "vis": "standing in front of the Eiffel Tower on a cloudy day", "ctx": "anniversary trip", "time": "daytime, spring"},
    {"id": "007", "loc": "Tokyo", "ppl": ["friends"], "evt": "city exploration", "obj": ["neon signs", "umbrellas"], "vis": "walking through rainy neon streets", "ctx": "winter trip", "time": "night, winter"},
    {"id": "008", "loc": "Kyoto", "ppl": [], "evt": "temple visit", "obj": ["cherry blossoms", "temple"], "vis": "traditional temple surrounded by pink cherry blossoms", "ctx": "spring travel", "time": "morning, spring"},
    {"id": "009", "loc": "Swiss Alps", "ppl": ["family", "kids"], "evt": "ski trip", "obj": ["skis", "snow"], "vis": "family skiing down a snowy mountain", "ctx": "winter holiday", "time": "daytime, winter"},
    
    # 3. Family gatherings
    {"id": "010", "loc": "Home", "ppl": ["parents", "grandparents"], "evt": "Thanksgiving dinner", "obj": ["turkey", "dining table"], "vis": "large family sitting around a thanksgiving feast", "ctx": "holiday gathering", "time": "evening, fall"},
    {"id": "011", "loc": "Backyard", "ppl": ["cousins", "uncle"], "evt": "BBQ", "obj": ["grill", "burgers"], "vis": "family barbecue in the backyard on a sunny day", "ctx": "summer cookout", "time": "afternoon, summer"},
    {"id": "012", "loc": "Living Room", "ppl": ["siblings"], "evt": "Christmas morning", "obj": ["presents", "Christmas tree"], "vis": "opening presents under the christmas tree", "ctx": "christmas", "time": "morning, winter"},
    
    # 4. Birthday
    {"id": "013", "loc": "Indoor Cafe", "ppl": ["Maya", "friends"], "evt": "birthday party", "obj": ["birthday cake", "candles"], "vis": "blowing out candles on a chocolate cake indoors", "ctx": "25th birthday", "time": "evening"},
    {"id": "014", "loc": "Park", "ppl": ["kids", "family"], "evt": "birthday picnic", "obj": ["balloons", "picnic blanket"], "vis": "outdoor birthday picnic with balloons and cake", "ctx": "kids birthday", "time": "afternoon, spring"},
    {"id": "015", "loc": "Fancy Restaurant", "ppl": ["husband"], "evt": "birthday dinner", "obj": ["wine", "steak"], "vis": "romantic birthday dinner at a dimly lit restaurant", "ctx": "milestone birthday", "time": "night"},
    
    # 5. Friends
    {"id": "016", "loc": "Downtown", "ppl": ["best friends"], "evt": "night out", "obj": ["drinks", "neon lights"], "vis": "group selfie on a busy downtown street at night", "ctx": "weekend night out", "time": "night"},
    {"id": "017", "loc": "Apartment", "ppl": ["roommates"], "evt": "game night", "obj": ["board games", "pizza"], "vis": "playing board games and eating pizza on the floor", "ctx": "casual hangout", "time": "evening"},
    {"id": "018", "loc": "Coffee Shop", "ppl": ["colleague"], "evt": "coffee catchup", "obj": ["coffee cups", "laptop"], "vis": "two people chatting over coffee near a window", "ctx": "afternoon break", "time": "afternoon"},
    
    # 6. Restaurant / dinner
    {"id": "019", "loc": "Italian Restaurant", "ppl": ["family"], "evt": "dinner", "obj": ["pizza", "pasta"], "vis": "eating large pizzas at an authentic italian place", "ctx": "family dinner", "time": "evening"},
    {"id": "020", "loc": "Sushi Bar", "ppl": ["friends"], "evt": "dinner", "obj": ["sushi rolls", "chopsticks"], "vis": "colorful sushi platter on a wooden counter", "ctx": "celebration dinner", "time": "night"},
    {"id": "021", "loc": "Street Food Market", "ppl": [], "evt": "food tour", "obj": ["tacos", "food truck"], "vis": "tacos from a brightly lit food truck", "ctx": "night market", "time": "night"},
    
    # 7. Wedding
    {"id": "022", "loc": "Church", "ppl": ["bride", "groom"], "evt": "wedding ceremony", "obj": ["wedding dress", "flowers"], "vis": "bride and groom walking down the aisle", "ctx": "wedding day", "time": "daytime"},
    {"id": "023", "loc": "Banquet Hall", "ppl": ["friends", "newlyweds"], "evt": "wedding reception", "obj": ["dance floor", "suit"], "vis": "friends dancing enthusiastically at a wedding reception", "ctx": "wedding party", "time": "night"},
    {"id": "024", "loc": "Outdoor Garden", "ppl": ["bridesmaids"], "evt": "wedding photoshoot", "obj": ["bouquets", "pink dresses"], "vis": "bridesmaids posing in a lush green garden", "ctx": "wedding prep", "time": "afternoon, summer"},
    
    # 8. Office / work
    {"id": "025", "loc": "Office", "ppl": ["coworkers"], "evt": "team meeting", "obj": ["whiteboard", "laptops"], "vis": "team brainstorming around a whiteboard", "ctx": "project planning", "time": "morning"},
    {"id": "026", "loc": "Conference Center", "ppl": ["colleagues"], "evt": "tech conference", "obj": ["badges", "stage"], "vis": "group photo wearing conference lanyards", "ctx": "annual summit", "time": "daytime"},
    {"id": "027", "loc": "Home Office", "ppl": ["me"], "evt": "working from home", "obj": ["monitor", "coffee mug", "cat"], "vis": "desk setup with a monitor and a cat sleeping on the keyboard", "ctx": "remote work", "time": "daytime"},
    
    # 9. College
    {"id": "028", "loc": "University Campus", "ppl": ["friends", "classmates"], "evt": "graduation", "obj": ["caps", "gowns", "diplomas"], "vis": "throwing graduation caps in the air in front of a brick building", "ctx": "college graduation", "time": "daytime, spring"},
    {"id": "029", "loc": "Library", "ppl": ["study group"], "evt": "exam prep", "obj": ["textbooks", "highlighters"], "vis": "stressed students surrounded by piles of books late at night", "ctx": "finals week", "time": "night"},
    {"id": "030", "loc": "Dorm Room", "ppl": ["roommate"], "evt": "moving in", "obj": ["boxes", "posters"], "vis": "unpacking cardboard boxes in a small dorm room", "ctx": "freshman year", "time": "daytime, fall"},
    
    # 10. Festival
    {"id": "031", "loc": "Desert", "ppl": ["friends"], "evt": "music festival", "obj": ["ferris wheel", "sunglasses", "glitter"], "vis": "crowd watching a stage with a brightly lit ferris wheel in the background", "ctx": "coachella", "time": "sunset, summer"},
    {"id": "032", "loc": "City Park", "ppl": [], "evt": "food festival", "obj": ["food tents", "crowd"], "vis": "busy outdoor food festival with colorful tents", "ctx": "local festival", "time": "afternoon"},
    {"id": "033", "loc": "Concert Arena", "ppl": ["friends"], "evt": "concert", "obj": ["stage lights", "confetti"], "vis": "blinding stage lights and confetti falling on a cheering crowd", "ctx": "live music", "time": "night"},
    
    # 11. Road trip
    {"id": "034", "loc": "Desert Highway", "ppl": ["friends"], "evt": "road trip", "obj": ["convertible car", "cactus"], "vis": "driving a convertible through a desert landscape", "ctx": "cross country trip", "time": "daytime, summer"},
    {"id": "035", "loc": "Mountain Pass", "ppl": ["Maya"], "evt": "road trip", "obj": ["mountains", "snow"], "vis": "car parked at a scenic mountain overlook with snowy peaks", "ctx": "mountain drive", "time": "morning, winter"},
    {"id": "036", "loc": "Gas Station", "ppl": ["friends"], "evt": "pit stop", "obj": ["gas pump", "snacks"], "vis": "buying snacks at a retro gas station", "ctx": "late night drive", "time": "night"},
    
    # 12. Sunset
    {"id": "037", "loc": "City Skyline", "ppl": [], "evt": "sightseeing", "obj": ["skyscrapers", "sun"], "vis": "sun setting behind a dramatic city skyline", "ctx": "golden hour", "time": "sunset"},
    {"id": "038", "loc": "Lake", "ppl": ["dog"], "evt": "evening walk", "obj": ["water", "trees"], "vis": "silhouette of a dog sitting by a calm lake at sunset", "ctx": "peaceful evening", "time": "sunset, fall"},
    
    # 13. Indoor gatherings
    {"id": "039", "loc": "Apartment", "ppl": ["friends"], "evt": "house party", "obj": ["red cups", "speaker"], "vis": "crowded house party with red solo cups", "ctx": "new years eve", "time": "night, winter"},
    {"id": "040", "loc": "Dining Room", "ppl": ["family"], "evt": "dinner party", "obj": ["fancy plates", "candles"], "vis": "elegant indoor dinner setup with candles", "ctx": "hosting friends", "time": "evening"},
    
    # 14. Outdoor gatherings
    {"id": "041", "loc": "Local Park", "ppl": ["friends"], "evt": "picnic", "obj": ["picnic basket", "frisbee"], "vis": "group of friends sitting on the grass playing frisbee", "ctx": "sunny weekend", "time": "afternoon, spring"},
    {"id": "042", "loc": "Campsite", "ppl": ["family", "kids"], "evt": "camping", "obj": ["tent", "campfire"], "vis": "roasting marshmallows over a campfire near a green tent", "ctx": "weekend camping trip", "time": "night, summer"},
    
    # 15. Childhood / old memories
    {"id": "043", "loc": "Childhood Home", "ppl": ["me", "mom"], "evt": "first day of school", "obj": ["backpack", "yellow school bus"], "vis": "faded old photo of a kid with a huge backpack waiting for the bus", "ctx": "childhood", "time": "morning, fall"},
    {"id": "044", "loc": "Theme Park", "ppl": ["family"], "evt": "vacation", "obj": ["rollercoaster", "cotton candy"], "vis": "vintage grainy photo of a family eating cotton candy near a rollercoaster", "ctx": "disney trip", "time": "daytime, summer"},
    
    # 16. Pets
    {"id": "045", "loc": "Living Room", "ppl": ["cat"], "evt": "sleeping", "obj": ["sofa", "sunbeam"], "vis": "orange tabby cat sleeping in a patch of sunlight on the sofa", "ctx": "lazy sunday", "time": "afternoon"},
    {"id": "046", "loc": "Dog Park", "ppl": ["dog", "other dogs"], "evt": "playing", "obj": ["tennis ball", "grass"], "vis": "golden retriever running with a tennis ball in its mouth", "ctx": "dog park visit", "time": "morning"},
    {"id": "047", "loc": "Bed", "ppl": ["puppy"], "evt": "cuddling", "obj": ["blanket"], "vis": "tiny puppy wrapped in a fuzzy blanket", "ctx": "new puppy", "time": "night"},
    
    # 17. Screenshots / documents
    {"id": "048", "loc": "", "ppl": [], "evt": "", "obj": ["receipt", "text"], "vis": "screenshot of an online order receipt for concert tickets", "ctx": "ticket purchase", "time": ""},
    {"id": "049", "loc": "", "ppl": [], "evt": "", "obj": ["map", "directions"], "vis": "screenshot of google maps directions to a hiking trail", "ctx": "trip planning", "time": ""},
    {"id": "050", "loc": "", "ppl": [], "evt": "", "obj": ["funny meme", "text"], "vis": "screenshot of a funny internet meme about waking up early", "ctx": "meme stash", "time": ""}
]

output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend", "public", "demo-photos")
os.makedirs(output_dir, exist_ok=True)

library = []

colors = ["#FFB3BA", "#FFDFBA", "#FFFFBA", "#BAFFC9", "#BAE1FF", "#E6B3FF", "#B3FFF1"]

for i, s in enumerate(scenarios):
    photo_id = f"photo_{s['id']}"
    filename = f"{photo_id}.jpg"
    filepath = os.path.join(output_dir, filename)
    
    # Create simple solid color image with text
    img = Image.new('RGB', (800, 600), color=colors[i % len(colors)])
    d = ImageDraw.Draw(img)
    
    try:
        font = ImageFont.truetype("arial.ttf", 36)
    except:
        font = ImageFont.load_default()
        
    text = f"{photo_id}\n{s['vis']}"
    # Simple text wrap
    wrapped_text = ""
    words = text.split()
    line = ""
    for word in words:
        if len(line) + len(word) > 40:
            wrapped_text += line + "\n"
            line = word + " "
        else:
            line += word + " "
    wrapped_text += line
    
    d.text((50, 250), wrapped_text, fill=(0,0,0), font=font)
    img.save(filepath, "JPEG")
    
    record = {
        "photo_id": photo_id,
        "image": f"/demo-photos/{filename}",
        "date": "2023-07-18",
        "approximate_time": s["time"],
        "location": s["loc"],
        "people": s["ppl"],
        "event": s["evt"],
        "objects": s["obj"],
        "visual_description": s["vis"],
        "context": s["ctx"]
    }
    library.append(record)
    
with open(os.path.join(os.path.dirname(__file__), "demo_library.json"), "w") as f:
    json.dump(library, f, indent=2)

print(f"Generated {len(library)} images and updated demo_library.json")
