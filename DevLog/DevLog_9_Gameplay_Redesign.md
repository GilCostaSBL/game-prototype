# 🧾 DevLog 9 - Gameplay Redesign: Movie Pair Selection

**Date:** 2025-10-31  
**Author:** Gil Costa  

---

### **Summary**
Redesigned the gameplay loop to focus on the **movie selection mechanic**, aligning with the prototype’s main concept:  
> “Pick your favorite movie from each pair!”

At the start, a short **title message** is shown. Then, two “movie posters” (colored squares with text labels) drop from the top — one in each lane. The player moves left or right to select their preferred movie by colliding with it. The chosen movie increases the score by **+1**, and the other disappears. A new pair appears after a short delay.

---

### **Steps Completed**
1. Added a **title screen** message displayed for 2 seconds at the start.  
2. Replaced obstacle logic with **MoviePoster** sprites, each showing a random movie title.  
3. Created a **pair spawn system**:
   - Always spawns two posters, one per lane.  
   - Spawns a new pair only after the previous selection.  
4. Adjusted movement speed of posters for readability.  
5. Updated the score logic to track how many selections were made.  
6. Added simple print feedback (console) when a movie is selected.

---

### **Next Steps**
- Replace colored squares with actual poster images.  
- Store user’s movie choices for analytics or training.  
- Add transition or animation effects between rounds.  
- Consider showing results after a set number of pairs.
