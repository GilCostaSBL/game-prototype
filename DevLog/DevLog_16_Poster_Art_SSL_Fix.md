
## 🧾 Devlog 16 — Poster Scaling, Alignment, and Final Network Fix

**Date:** 2025-11-26  
**Phase:** Visual & Stability Polish  
**Author:** Gil Costa  
**Project:** Game Prototype

-----

### 🎯 Summary

This update brings the visual display of the movie posters closer to final specifications by introducing **dynamic, aspect-ratio-correct scaling** and updating the vertical alignment. Crucially, a persistent network error was resolved by applying the SSL bypass fix to both API calls required for poster data and image download.

-----

### 🧩 Key Changes Implemented

1.  **Network Stability Hardened:** The initial SSL bypass fix was only applied to the OMDb metadata request. This devlog addresses a subsequent `SSLError` that occurred when downloading the image file from the image host (Amazon/IMDb). The `verify=False` flag was applied to the `requests.get` call inside `load_image_from_url` to completely eliminate certificate verification failures for all external network activity.

2.  **Dynamic Poster Sizing:** The poster dimensions are now responsive to the image's original aspect ratio:

      * **Fixed Width:** Posters are scaled to a fixed width of **216 pixels**.
      * **Height Constraint:** The height is calculated proportionally but is capped at a maximum of **320 pixels**.
      * This ensures that tall posters do not occupy excessive screen space while all images retain their correct aspect ratio.

3.  **Visual Alignment Refactor:** The `Poster` class initialization was updated to align the poster sprite by its **bottom edge** to the specified starting position, ensuring the image begins dropping with its entire body immediately visible on the screen.

      * The property `self.rect.bottom` is now set to `0` at instantiation.

-----

### 💻 Code Highlights

**1. Complete SSL Bypass (in `load_image_from_url`):**

```python
def load_image_from_url(url, width, height_limit):
    # ...
    response = requests.get(url, verify=False) # Fix applied to image download
    # ...
```

**2. Proportional Scaling and Clamping (in `load_image_from_url`):**

```python
# Calculate new height based on fixed width and aspect ratio
new_height = int(width * (original_height / original_width))

# Apply the height limit (320)
final_height = min(new_height, height_limit)

return pygame.transform.scale(image_surface, (width, final_height))
```

**3. Poster Bottom Alignment (in `Poster.__init__`):**

```python
class Poster(pygame.sprite.Sprite):
    def __init__(self, lane, title, image_surface): 
        # ...
        # Aligns the bottom of the poster to the top of the screen (Y=0)
        self.rect.bottom = 0 
        # ...
```

-----

### 🧠 Next Steps

The game now features full-resolution posters and a functional scrolling end screen. The immediate next steps should involve further visual polish, such as introducing subtle animations or transitions for lane switching (as noted in Devlog 10) and potentially building out the category selection UI.

```
```