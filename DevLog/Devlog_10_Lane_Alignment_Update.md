## 🧾 Devlog 10 – Lane Alignment Update

**Date:** 2025-10-31  
**Focus:** Aligning player position with poster lanes for smoother gameplay.

### 🎮 Summary
This update improves gameplay precision by **aligning the player’s position** with the movie poster lanes. Before, the player could appear slightly off-center relative to the falling posters, causing awkward or inconsistent collisions. Now, the player snaps perfectly under each lane, ensuring clear feedback when selecting a movie.

### 🧠 Key Changes
- **Player movement** simplified to two fixed lanes (left/right).  
- Lane coordinates now **match exactly** with the poster drop lanes:
  ```python
  SCREEN_WIDTH // 4      # Left lane
  (SCREEN_WIDTH * 3)//4  # Right lane
  ```
- **No free movement:** player only switches lanes when space allows.  
- Updated `player.py` logic for clean lane switching.

### 🧩 Gameplay Impact
- Collisions feel cleaner and more intentional.  
- Visual alignment makes choices clearer for players.  
- Paves the way for future polish (animations, visuals, etc.).

### 🔍 Next Steps
- Add subtle animations for lane switching.  
- Implement visual feedback (highlight chosen poster).  
- Possibly introduce a central “neutral” lane for later gameplay ideas.
