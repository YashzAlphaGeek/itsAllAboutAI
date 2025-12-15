# 🦇 Shadows of Shadow Falls

**Shadows of Shadow Falls** is a **locally-run AI-powered interactive text adventure** inspired by *The Vampire Diaries*. The game uses **Ollama + LLaMA 3** as the Game Master, generating dynamic story events, supernatural encounters, and narrative twists based on player input. Health and Fear stats are tracked in real-time, making every playthrough unique.

---

## Features

* **AI-driven storytelling:** The AI acts as a Game Master, creating suspenseful events and immersive narrative.
* **Player stats tracking:** Health and Fear are visually displayed as bars, updating based on player actions and AI responses.
* **Emergent gameplay:** No two games are the same; the AI generates new storylines dynamically.
* **Interactive text adventure:** Play directly in the terminal with free-form commands.

---

## Installation

1. Make sure you have **Python 3.10+** installed.
2. Install **Ollama** locally and download the LLaMA 3 model:

   ```bash
   ollama pull llama3
   ```
3. Save the game script as `shadows_of_shadow_falls.py`.

---

## How to Play

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
   ```
4. The AI will respond with the next part of the story, and stats will update dynamically.
5. Game ends when:

   * Health ≤ 0 → GAME OVER
   * Fear ≥ 100 → GAME OVER
   * Or you type `quit`

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
* The AI **updates stats numerically** in its output; the Python script reads these values and updates the bars.

---

## Requirements

* Python 3.10+
* Ollama (local LLaMA 3 model)
* Terminal or command-line interface

---
