# Devlog 11 — Selection Panel & Done Button Integration

**Date:** 2025-11-18  
**Author:** Gil Costa  
**Project:** Game Prototype  

---

## 🎯 Summary
This devlog covers the addition of the **Selection Panel**, the **Done Button**, and the **layout adjustments** needed to support a right‑side UI panel. These improvements allow players to see the last five selected movie titles and end the game cleanly.

---

## 🧩 Key Features Added

### 1. Selection Panel (Right-Side UI)
- Displays the **last five** selected movie titles.
- Updates as players choose posters.
- Titles stack top‑down with spacing.
- Independent from core gameplay area.

### 2. Persistent Storage of Final Selections
- Every selection is stored in a full list.
- Summary screen uses the full list, not the last five.

### 3. “Done!” Button
- Located at the bottom of the right-side panel.
- Clicking it:
  - Ends gameplay loop.
  - Freezes animations.
  - Shows a final summary screen with all selections.

### 4. Layout Adjustments
- Main play area reduced to ~65% width.
- Right-side panel uses remaining screen space.
- Player and posters now remain confined to the left gameplay area.

---

## 💻 Implementation Notes
- Introduced `SelectionPanel` class to manage UI.
- Integrated click detection for the Done button.
- Modified collision handling so selections update the panel.
- Added a summary screen after Done is clicked.

---

## 🧠 Next Steps
- Integrate JSON-based movie loading.
- Add category selection screen.
- Improve visuals for the panel and buttons.

