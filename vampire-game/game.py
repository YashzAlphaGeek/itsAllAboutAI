import ollama

# --- SYSTEM PROMPT: The AI Game Master ---
SYSTEM_PROMPT = """
You are the Game Master for a vampire mystery text adventure inspired by The Vampire Diaries.

Rules:
- Setting: small town at night (Shadow Falls)
- Tone: suspenseful, supernatural, and mysterious
- Player is a teenager
- Track:
  - Health (start at 100)
  - Fear (start at 0)
- Increase fear during vampire or supernatural encounters
- If health reaches 0 → GAME OVER
- If fear reaches 100 → player panics and loses
- Do NOT control player actions
- Keep responses under 120 words
- Provide vivid descriptions to immerse the player
"""

# --- INITIAL PLAYER STATS ---
player_stats = {
    "Health": 100,
    "Fear": 0
}

# --- INITIAL GAME STATE ---
game_state = """
Player:
- Health: 100
- Fear: 0

Location:
- Bedroom in Shadow Falls
- Moonlight filters through the window
- You hear a faint whisper outside
"""

# --- FUNCTION TO DISPLAY STAT BARS ---
def display_stats(stats):
    def bar(value):
        total = 20
        filled = int((value / 100) * total)
        return "[" + "#" * filled + "-" * (total - filled) + "]"
    print(f"Health: {bar(stats['Health'])} {stats['Health']}/100")
    print(f"Fear  : {bar(stats['Fear'])} {stats['Fear']}/100\n")

# --- FUNCTION TO PROCESS AI TURNS ---
def ai_turn(player_input, game_state):
    prompt = f"""
Game state:
{game_state}

Player action:
{player_input}

Update health and fear numerically and describe what happens next.
"""
    response = ollama.chat(
        model="llama3",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ]
    )
    return response["message"]["content"]

# --- GAME INTRO ---
print("\n🦇 SHADOWS OF SHADOW FALLS")
print("Type actions like: investigate noise, peek outside, use flashlight")
print("Type 'quit' to exit\n")

display_stats(player_stats)

# --- MAIN GAME LOOP ---
while True:
    player_input = input("> ")

    if player_input.lower() == "quit":
        print("You gave up. Shadow Falls remains shrouded in darkness...")
        break

    ai_output = ai_turn(player_input, game_state)
    print("\n" + ai_output + "\n")

    # Update game state
    game_state += f"\nPlayer action: {player_input}\n{ai_output}"


    import re
    health_match = re.search(r"Health[:= ](\d+)", ai_output)
    fear_match = re.search(r"Fear[:= ](\d+)", ai_output)
    if health_match:
        player_stats["Health"] = max(0, min(100, int(health_match.group(1))))
    if fear_match:
        player_stats["Fear"] = max(0, min(100, int(fear_match.group(1))))

    display_stats(player_stats)

    if player_stats["Health"] <= 0 or player_stats["Fear"] >= 100 or "GAME OVER" in ai_output.upper():
        print("💀 GAME OVER")
        break
