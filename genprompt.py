import random

# Expanded Categories
outfits = [
    "a sleek black cocktail dress",
    "a red summer dress with plunging neckline",
    "lingerie and stockings",
    "a bikini with a sarong",
    "casual jeans and a crop top",
    "a silk evening gown",
    "a leather jacket over a tank top",
    "a sheer blouse with a pencil skirt",
    "a silk robe loosely tied",
    "an athletic yoga outfit",
    # New Additions
    "a fitted white button-down shirt tucked into high-waisted trousers",
    "a short red mini-dress with spaghetti straps",
    "a long flowing floral maxi dress",
    "a tight black leather catsuit",
    "a delicate lace camisole with matching shorts",
    "a stylish trench coat over thigh-high boots",
    "a casual hoodie and denim shorts",
    "a satin slip dress with lace trim",
    "a cropped leather jacket with skinny jeans",
    "a glittering sequin party dress",
    "a sheer mesh top with a bralette underneath",
    "a sporty tennis outfit with a pleated skirt",
    "an elegant qipao-style dress",
    "a business blazer with nothing underneath",
    "a halter-neck cocktail dress",
    "a transparent chiffon blouse tied at the waist",
    "a velvet gown with a high slit",
    "a futuristic cyberpunk bodysuit",
    "a tight ribbed sweater dress",
    "a silk kimono with floral embroidery"
]

settings = [
    "in a neon-lit urban street at night",
    "poolside under bright sunlight",
    "in a luxury bedroom with velvet drapes",
    "leaning against a glass office window",
    "walking down a cobblestone street",
    "standing on a mountain trail at golden hour",
    "sitting at a café table outdoors",
    "lounging on a velvet sofa indoors",
    "by a graffiti wall in the city",
    "near a large window with daylight streaming in",
    # New Additions
    "on a rooftop overlooking the city skyline",
    "inside a modern kitchen with marble counters",
    "by a roaring fireplace in a rustic cabin",
    "in a luxury sports car with leather seats",
    "at the beach with waves crashing behind her",
    "in a rainy alley under a glowing streetlight",
    "inside a neon-lit nightclub dance floor",
    "at a library table surrounded by books",
    "walking down a marble staircase in a grand hall",
    "in a desert landscape with sand dunes behind her",
    "standing under cherry blossoms in full bloom",
    "at a candle-lit dining table with wine glasses",
    "in a futuristic cyberpunk cityscape",
    "on a balcony with city lights in the distance",
    "at a rustic barn with warm sunlight pouring in",
    "inside a private jet with soft ambient light",
    "on a luxury yacht at sunset",
    "standing in front of a glowing bonfire",
    "walking down a fashion runway"
]

expressions = [
    "with a confident smirk",
    "with a playful smile",
    "with a sultry gaze",
    "with a warm and inviting smile",
    "with teasing eye contact",
    "with a bold and daring expression",
    "with a seductive stare",
    "with soft glowing eyes",
    "with a friendly approachable look",
    "with a mischievous grin",
    # New Additions
    "with flushed cheeks and parted lips",
    "with a mysterious half-smile",
    "with dreamy, faraway eyes",
    "with a sharp, commanding stare",
    "with a soft pout",
    "with raised eyebrows in surprise",
    "with a warm laugh caught mid-moment",
    "with a biting-lip expression",
    "with bedroom eyes and slow confidence",
    "with a serene, peaceful smile"
]

shot_types = [
    "eye-level cinematic shot, medium full-body framing",
    "close-up portrait, shallow depth of field, crisp facial detail",
    "three-quarter body shot, cinematic tracking angle",
    "low angle dramatic shot, strong perspective",
    "waist-up portrait, natural composition",
    "over-the-shoulder cinematic framing",
    "slightly high angle glamour shot, detailed and sharp",
    "full-body fashion shot, studio style lighting",
    "candid street photography framing, natural detail",
    "cinematic close-up with ultra-clear focus",
    # New Additions
    "aerial drone-style shot with dynamic perspective",
    "extreme close-up with fine skin detail",
    "wide establishing shot with background emphasis",
    "medium shot with bokeh city lights behind",
    "low angle shot emphasizing dominance and power",
    "profile portrait with sharp side lighting",
    "tracking dolly-style cinematic capture",
    "mirror reflection perspective",
    "shot through glass with subtle reflections",
    "overhead flat-lay style framing"
]

lighting = [
    "golden hour sunlight",
    "soft ambient lounge lighting",
    "neon glow city lights",
    "natural daylight",
    "warm candle-lit tones",
    "dramatic high-contrast lighting",
    "soft studio light",
    "backlit window glow",
    "crisp outdoor sunlight",
    "moody cinematic shadow lighting",
    # New Additions
    "harsh spotlight with deep shadows",
    "glowing fireplace illumination",
    "glittering disco ball reflections",
    "cool blue moonlight",
    "bright fluorescent indoor light",
    "flickering neon signs",
    "gentle overcast daylight",
    "colored gel lighting in magenta and teal",
    "string lights casting warm bokeh",
    "rainy window light with reflections"
]

# Function to generate one caption
def generate_caption(sex, age, body_type):
    outfit = random.choice(outfits)
    setting = random.choice(settings)
    expression = random.choice(expressions)
    shot = random.choice(shot_types)
    light = random.choice(lighting)

    return (
        f"Keep exact same character, a {age}-year-old {sex}, {body_type}, "
        f"wearing {outfit}, {setting}, her full face visible {expression}. "
        f"Shot Type: {shot}, {light}, high fidelity, maintaining original facial features and body structure."
    )

# Interactive prompts
def main():
    print("🔹 WAN Character Caption Generator 🔹")
    sex = input("Enter the character’s sex (e.g., woman, man): ").strip()
    age = input("Enter the character’s age (e.g., 35): ").strip()
    body_type = input("Enter the body type (e.g., slim, curvy, average build): ").strip()
    num_captions = int(input("How many captions do you want to generate?: "))

    captions = [generate_caption(sex, age, body_type) for _ in range(num_captions)]

    with open("wan_character_captions.txt", "w", encoding="utf-8") as f:
        for cap in captions:
            f.write(cap + "\n")

    print(f"✅ Generated {num_captions} captions and saved to wan_character_captions.txt")

if __name__ == "__main__":
    main()



### Every caption is structured, consistent, and creative, while keeping her face visible.   give it a try.  its a real simple python script.    Here is the script since i have no idea how the hell to post a file:  here is the script.