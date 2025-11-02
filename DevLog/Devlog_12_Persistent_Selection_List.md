## 🧾 Devlog 12 — Persistent Selection List & Final Summary Fix  

**Date:** 2025-10-31  
**Author:** Gil Costa  
**Project:** Game Prototype  

---

### 🎯 Summary
This update refines the end-of-round flow by ensuring the player’s movie choices persist and display correctly on the final screen. Previously, only the last five selections (from the side panel) were visible at the end. Now, every selected movie is tracked and displayed once the player finishes the session.  

---

### 🧩 Changes Implemented
1. **SelectionPanel Class**
   - Added a new list, `all_selected_titles`, to store every chosen movie.
   - The existing `selected_titles` list continues to show only the last five picks on the right panel.
   - Adjusted the `add_title()` method to insert into both lists.

2. **Final Summary Screen**
   - The game now draws from `all_selected_titles` instead of the truncated `selected_titles`.
   - Ensures all past selections are visible once the player clicks **“Done!”**.

3. **Gameplay Behavior**
   - The side panel remains a live feed of the last few picks.
   - The **final summary** now displays every movie selected in order of choice.

---

### 💻 Code Highlights
**Updated SelectionPanel:**
```python
self.selected_titles = []       # last 5 shown
self.all_selected_titles = []   # full history
```

**Persistent summary display:**
```python
for t in panel.all_selected_titles:
    text = summary_font.render(t, True, WHITE)
    screen.blit(text, (100, y))
    y += 50
```

---

### 🧠 Notes
This change improves session continuity and prepares for future export features (e.g., saving player preferences or generating results).  
Next, we’ll focus on **Step 11 visual polish**, including proper movie poster art integration.
