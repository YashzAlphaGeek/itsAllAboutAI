import streamlit as st
import ollama
import re

# --- SYSTEM PROMPT ---
SYSTEM_PROMPT = """
You are the Game Master for a vampire mystery text adventure inspired by The Vampire Diaries.
Rules:
- Setting: small town at night (Shadow Falls)
- Tone: suspenseful, supernatural, and mysterious
- Player is a teenager
- Track:
  - Health (start at 100)
  - Fear (start at 0)
  - Inventory (empty list)
- Increase fear during supernatural encounters
- Health decreases if attacked
- If health reaches 0 → GAME OVER
- If fear reaches 100 → player panics and loses
- Provide updated stats in the output in the format: Health: <value>, Fear: <value>, Inventory: <list>
"""

# --- Initialize Session State ---
if 'player_stats' not in st.session_state:
    st.session_state.player_stats = {"Health": 100, "Fear": 0, "Inventory": []}
if 'game_state' not in st.session_state:
    st.session_state.game_state = {
        "location": "Bedroom in Shadow Falls",
        "events": ["Moonlight filters through the window", "You hear a faint whisper outside"]
    }
if 'story' not in st.session_state:
    st.session_state.story = []

# --- Function to Call AI ---
def ai_turn(player_input):
    stats = st.session_state.player_stats
    game_state = st.session_state.game_state

    prompt = f"""
Game state:
Location: {game_state['location']}
Events: {', '.join(game_state['events'])}
Player Stats: Health={stats['Health']}, Fear={stats['Fear']}, Inventory={stats['Inventory']}

Player action:
{player_input}

Respond with narrative and updated Health/Fear/Inventory in the format:
Health: <value>, Fear: <value>, Inventory: <list>
"""
    response = ollama.chat(
        model="llama3",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ]
    )
    return response["message"]["content"]

# --- Layout ---
st.title("🦇 Shadows of Shadow Falls")
st.markdown("**AI-powered vampire mystery text adventure**")

# --- Display Story ---
story_container = st.container()
for entry in st.session_state.story:
    story_container.markdown(entry)

# --- Stats Display ---
def display_stats(stats):
    st.progress(stats["Health"], text=f"Health: {stats['Health']}")
    st.progress(stats["Fear"], text=f"Fear: {stats['Fear']}")
    st.markdown(f"**Inventory:** {', '.join(stats['Inventory']) if stats['Inventory'] else 'Empty'}")

display_stats(st.session_state.player_stats)

# --- Handle Actions ---
action = None

# Quick Action Buttons
st.markdown("### Quick Actions")
cols = st.columns(4)
quick_actions = ["peek outside", "investigate noise", "use flashlight", "open closet"]
for i, act in enumerate(quick_actions):
    if cols[i % 4].button(act):
        action = act

# Text input for custom action
text_input = st.text_input("Or type a custom action:")
if st.button("Submit") and text_input.strip():
    action = text_input.strip()

# --- Process Action ---
if action:
    if action.lower() == "quit":
        st.session_state.story.append("You gave up. Shadow Falls remains shrouded in darkness...")
        st.stop()

    st.session_state.story.append(f"**> {action}**")
    ai_output = ai_turn(action)
    st.session_state.story.append(ai_output)

    # Extract stats
    stats = st.session_state.player_stats
    health_match = re.search(r"Health[:= ](\d+)", ai_output)
    fear_match = re.search(r"Fear[:= ](\d+)", ai_output)
    inventory_match = re.search(r"Inventory[:= ]\[(.*?)\]", ai_output)

    if health_match:
        stats["Health"] = max(0, min(100, int(health_match.group(1))))
    if fear_match:
        stats["Fear"] = max(0, min(100, int(fear_match.group(1))))
    if inventory_match:
        items = [i.strip().strip("'\"") for i in inventory_match.group(1).split(",") if i.strip()]
        stats["Inventory"] = items

    # Update game state
    st.session_state.game_state['events'].append(f"Player action: {action}")

    # Check end-game
    if stats["Health"] <= 0:
        st.session_state.story.append("💀 You have died. GAME OVER")
        st.stop()
    if stats["Fear"] >= 100:
        st.session_state.story.append("😱 Panic overwhelms you. GAME OVER")
        st.stop()

    # Refresh stats display
    display_stats(stats)
