# draw_letter.py
from PIL import Image, ImageDraw, ImageFont

def pick_font(size: int):
    """
    Try to load a common TrueType font. Fall back to PIL's default if not found.
    """
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",   # Linux (common)
        "/Library/Fonts/Arial.ttf",                          # macOS
        "C:/Windows/Fonts/arial.ttf",                        # Windows
        "DejaVuSans.ttf"                                     # sometimes bundled
    ]
    for path in candidates:
        try:
            return ImageFont.truetype(path, size=size)
        except Exception:
            continue
    # Fallback (bitmap font, no stroke support)
    return ImageFont.load_default()

def draw_text_image(
    text: str,
    img_size=(800, 800),
    font_size=400,
    text_color=(0, 0, 0),
    bg_color=(255, 255, 255, 255),  # use (255,255,255,0) for transparent
    stroke_width=6,
    stroke_fill=(0, 0, 0)
):
    # Create image (RGBA so we can support transparency if desired)
    img = Image.new("RGBA", img_size, bg_color)
    draw = ImageDraw.Draw(img)

    font = pick_font(font_size)

    # Get size of text (including stroke) and compute centered position
    # textbbox is accurate with stroke; fallback to textsize if needed
    try:
        bbox = draw.textbbox((0, 0), text, font=font, stroke_width=stroke_width)
        text_w = bbox[2] - bbox[0]
        text_h = bbox[3] - bbox[1]
    except Exception:
        text_w, text_h = draw.textsize(text, font=font)
        bbox = (0, 0, text_w, text_h)

    x = (img.width - text_w) // 2 - bbox[0]
    y = (img.height - text_h) // 2 - bbox[1]

    # Draw text with optional stroke/outline
    draw.text(
        (x, y),
        text,
        font=font,
        fill=text_color,
        stroke_width=stroke_width,
        stroke_fill=stroke_fill
    )

    return img

if __name__ == "__main__":
    # --- Customize here or take input ---
    user_text = input("Enter a letter (or any text): ").strip() or "A"
    out_path = "letter.png"

    # Example: white background, black text with black outline
    img = draw_text_image(
        text=user_text,
        img_size=(800, 800),      # change canvas size if you want
        font_size=500,            # change letter size
        text_color=(0, 0, 0, 255),
        bg_color=(255, 255, 255, 255),   # make last value 0 for transparent background
        stroke_width=8,           # outline thickness
        stroke_fill=(0, 0, 0, 255)
    )

    img.save(out_path)
    print(f"Saved: {out_path}")