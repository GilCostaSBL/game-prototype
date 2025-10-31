# 🧾 DevLog 8 - Basic Score System

**Date:** 2025-10-31  
**Author:** Gil Costa  

---

### **Summary**
Added a simple **score system** to the game to represent “preferred posters” collected by the player.  
Each time the player collides with an obstacle, the score increases by **+1**, and the obstacle is removed from the screen. The score is displayed visually at the **bottom of the screen**, just below the player sprite.

---

### **Steps Completed**
1. Added `score` and `font` attributes to `Game` class in `src/game.py`.  
2. Modified collision logic:
   - Increment `self.score` on hit.
   - Remove the obstacle (`hit.kill()`).  
3. Rendered score using `pygame.font` in the `draw()` method.  
4. Tested: collisions now increase the score instead of ending the game.

---

### **Next Steps**
- Introduce a “combo” or “streak” system for chained collisions.  
- Add visual feedback (e.g., color flash or sound).  
- Later replace the text-based score with custom UI elements or graphics.
