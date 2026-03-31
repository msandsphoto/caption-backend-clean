import random

fitness_hooks = [
    "Your progress deserves to be seen.",
    "Strong body. Calm mind.",
    "This is what discipline looks like."
]

fitness_bodies = [
    "A shoot like this is about capturing the work, effort and consistency behind the result.",
    "Great fitness imagery is not just about looking strong, it is about showing the mindset behind it.",
    "You have put in too much work not to document this stage properly."
]

fitness_ctas = [
    "DM me if you want to plan your own shoot.",
    "Message me if you are ready to book a session.",
    "Get in touch if you want to create something strong."
]

fitness_hashtags = [
    "#fitnessphotography #physiquephotography #fitnessshoot #gymmotivation",
    "#mensfitness #bodytransformation #fitnessjourney #MSandsPhotography",
    "#fitnessbranding #personaltrainer #fitnesscontent #fitnessphotoshoot"
]

portrait_hooks = [
    "A strong portrait changes how people see you.",
    "Confidence starts with how you present yourself.",
    "Your image should work as hard as you do."
]

portrait_bodies = [
    "I work with you to create clean, confident images that feel natural and intentional.",
    "A well-planned portrait session gives you images you can use across social media, websites and branding.",
    "This is about creating images with impact, without making it feel forced."
]

portrait_ctas = [
    "DM me if you would like to update your portraits.",
    "Message me if you want to book a portrait session.",
    "Get in touch if you are ready for stronger images."
]

portrait_hashtags = [
    "#portraitphotography #personalbranding #brandingphotography #headshots",
    "#mensportrait #portraitsession #creativeportrait #MSandsPhotography",
    "#personalbrand #confidence #brandingshoot #portraitwork"
]

mindset_hooks = [
    "Pause. Notice. Create.",
    "Sometimes the best thing you can do is slow down for a moment.",
    "When life feels noisy, small moments of focus can help."
]

mindset_bodies = [
    "My Mindset Photography Workshop is about using photography to slow down, focus the mind and reconnect with the present moment.",
    "This is not about taking perfect photos. It is about using photography as a simple tool to feel calmer and more grounded.",
    "Photography becomes the tool, not the goal."
]

mindset_ctas = [
    "Message me if you would like to know more about the workshop.",
    "DM me if you are interested in joining a future workshop.",
    "If this speaks to you, drop me a message."
]

mindset_hashtags = [
    "#mindsetphotography #pauseandnotice #mindfulphotography #presentmoment",
    "#slowdown #creativewellbeing #quietthemind #mentalwellbeing",
    "#PauseNoticeCreate #calmmind #awarenesspractice #MSandsPhotography"
]

print("What type of caption do you want?")
print("1 - Fitness")
print("2 - Portrait")
print("3 - Mindset")

choice = input("Enter 1, 2 or 3: ")

if choice == "1":
    hooks = fitness_hooks
    bodies = fitness_bodies
    ctas = fitness_ctas
    hashtags_list = fitness_hashtags
elif choice == "2":
    hooks = portrait_hooks
    bodies = portrait_bodies
    ctas = portrait_ctas
    hashtags_list = portrait_hashtags
elif choice == "3":
    hooks = mindset_hooks
    bodies = mindset_bodies
    ctas = mindset_ctas
    hashtags_list = mindset_hashtags
else:
    print("Invalid choice")
    exit()

hook = random.choice(hooks)
body = random.choice(bodies)
cta = random.choice(ctas)
hashtags = random.choice(hashtags_list)

print(f"{hook}\n")
print(f"{body}\n")
print(f"{cta}\n")
print(hashtags)