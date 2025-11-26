## 🧾 Devlog 14 — Poster Art Integration & Dynamic Title UI

**Date:** 2025-11-26
**Phase:** Prototype Development — Asset Integration
**Author:** Gil Costa
**Project:** Game Prototype

---

### 🎯 Summary
This entry marks a significant visual upgrade by integrating the **OMDb API** to replace the placeholder colored squares with actual movie poster images. Concurrently, the user interface for the poster titles was polished with dynamic sizing and centering, and a crucial bug regarding post-game session stability was resolved.

---

### 🧩 Key Changes Implemented

1.  **OMDb API Integration:** The `requests` library was added and utilized to perform synchronous API calls to OMDb. The game now searches for the movie title and fetches the corresponding poster image URL.
2.  **Dynamic Poster Display:** The `Poster` class was refactored to accept a pre-loaded `pygame.Surface` object. New helper functions (`get_poster_image`, `load_image_from_url`) handle downloading the image from the URL, scaling it to the required size (`100x140`), and providing a colored fallback surface if the API call or download fails.
3.  **Enhanced Title Readability:** The poster title box was updated to meet new UI requirements:
    * **Dynamic Height:** The title background box now dynamically calculates the total height required by all wrapped lines of text, ensuring the background completely covers the title regardless of its length.
    * **Centered Text:** All wrapped title lines are now horizontally centered within the poster's width for cleaner visual alignment.
4.  **Game-End Stability Fix:** A bug was fixed that allowed the game to continue attempting to load a new movie pair even after the player clicked the "Done!" button and the final summary screen was displayed.

---

### 💻 Code Highlights

**1. Poster Title Centering & Dynamic Box Sizing (in `Poster.draw`):**
```python
# Calculate total text height dynamically
# ...
title_box_height = max(total_text_height, 20)
# ...
# Calculate X position for centering each line
centered_x = title_box_x + (title_box_width - line_surface.get_width()) // 2