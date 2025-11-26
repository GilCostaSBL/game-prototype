# Devlog 13 — Poster & Title Box Refactor

**Date:** 2025-11-19  
**Author:** Gil Costa  
**Project:** Game Prototype  

---

## 🎯 Summary
This devlog documents the refactoring of the movie poster UI to support properly structured poster areas, dedicated title boxes, and automatic multi‑line word-wrapping. This improves readability, layout consistency, and prepares the interface for future artwork.

---

## 🧩 Key Changes Implemented

### 1. Poster UI Refactor
- Posters now include two distinct sections:
  - **Poster Box:** the visual card that will later hold actual poster artwork.
  - **Title Box:** a transparent text container under the poster.
- Title boxes now support:
  - Automatic **multi-line text wrapping** for long movie titles.
  - **Top-aligned text** inside the title box.
  - Clean spacing and padding.
  - A soft transparent dark overlay for readability.

### 2. Multi-line Text Wrapping System
A new helper function `wrap_text_multi` was introduced to:
- Break long titles into as many lines as needed.
- Respect maximum width constraints.
- Provide consistent layout across the UI.

### 3. Unified UI Improvements Across the Game
The new text-box system is now used in:
- Poster title areas  
- The selection panel (right side)  
- The final summary screen  

This brings a consistent presentation style across all parts of the game.

---

## 📁 Files Updated
- `src/game.py` — Major refactor of the poster and title layout  
- Helper functions for text wrapping and rendering  

---

## 🧠 Notes & Next Steps
With the new UI structure:
- Adding real poster artwork will be easier.
- Title presentation is now clear and consistent.
- This prepares the foundation for category selection UI.

Next steps will focus on integrating art assets and polishing transitions.

