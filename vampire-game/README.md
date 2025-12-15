# 🦇 Shadows of Shadow Falls

**Shadows of Shadow Falls** is a **locally-run AI-powered interactive text adventure** inspired by *The Vampire Diaries*. The game uses **Ollama + LLaMA 3** as the Game Master, generating dynamic story events, supernatural encounters, and narrative twists based on player input. Health and Fear stats are tracked in real-time, making every playthrough unique.

<img width="440" height="519" alt="image" src="https://github.com/user-attachments/assets/723f0de5-3c55-4ec2-bd73-058ba05653a4" />

---

## Features

* **AI-driven storytelling:** The AI acts as a Game Master, creating suspenseful events and immersive narrative.
* **Player stats tracking:** Health and Fear are visually displayed as bars, updating based on player actions and AI responses.
* **Emergent gameplay:** No two games are the same; the AI generates new storylines dynamically.
* **Interactive text adventure:** Play directly in the terminal with free-form commands.
* **Optional Web UI:** Streamlit-based browser interface with clickable actions and dynamic stats display.

---

## Installation

1. Make sure you have **Python 3.10+** installed.
2. Install **Ollama** locally and download the LLaMA 3 model:

   ```bash
   ollama pull llama3
   ```
3. Install **Streamlit** if you want the web UI version:

   ```bash
   pip install streamlit
   ```
---

## How to Play

### Terminal Version

1. Run the game from your terminal:

   ```bash
   python shadows_of_shadow_falls.py
   ```
2. You will see the introduction and initial stats: Health and Fear bars.
3. Type actions such as:

   ```
   investigate noise
   peek outside
   use flashlight
   open closet
   hide under the bed
   ```
4. The AI will respond with the next part of the story, and stats will update dynamically.
5. Game ends when:

   * Health ≤ 0 → GAME OVER
   * Fear ≥ 100 → GAME OVER
   * Or you type `quit`

### Web UI Version (Streamlit)

1. Run the Streamlit app:

   ```bash
   streamlit run shadows_of_shadow_falls.py
   ```
2. Your browser will open with the game interface.
3. You can type actions in the input box or click predefined action buttons.
4. Health, Fear, and Inventory stats update dynamically, and the story scrolls in the browser.
5. End conditions are the same as the terminal version.

---

## Example Commands

* `peek outside`
* `open the closet`
* `hide under the bed`
* `run to the street`
* `use flashlight`

---

## Gameplay Mechanics

* **Health:** Starts at 100; decreases if the player encounters danger or makes risky choices.
* **Fear:** Starts at 0; increases with supernatural events, scary encounters, or suspenseful situations.
* **Inventory:** Items collected during the game; dynamically updated by AI.
* The AI **updates stats numerically** in its output; the Python script reads these values and updates bars or displays.

---

## Requirements

* Python 3.10+
* Ollama (local LLaMA 3 model)
* Terminal or command-line interface (for terminal version)
* Browser (for Streamlit web UI version)
* Streamlit (`pip install streamlit`) for web UI

---

## Notes

* The AI generates dynamic events, so no two playthroughs are identical.
* You can mix free-form typed actions with predefined buttons in the web UI for enhanced interactivity.
* Make sure Ollama and LLaMA 3 are properly installed and accessible locally for the game to run.
