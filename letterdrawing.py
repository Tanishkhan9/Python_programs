# save as draw_text_pillow.py
from PIL import Image, ImageDraw, ImageFont

def draw_text_to_image(text="Hello, World!",
                       font_path=None,   # e.g. "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
                       font_size=120,
                       padding=20,
                       output="letters.png"):
    # choose font: use default if font_path is None
    if font_path:
        font = ImageFont.truetype(font_path, font_size)
    else:
        font = ImageFont.load_default()

    # measure text size
    dummy = Image.new("RGB", (1,1))
    draw = ImageDraw.Draw(dummy)
    w, h = draw.textsize(text, font=font)

    img = Image.new("RGB", (w + 2*padding, h + 2*padding), "white")
    draw = ImageDraw.Draw(img)
    draw.text((padding, padding), text, font=font, fill="black")

    img.save(output)
    print(f"Saved: {output}")

if __name__ == "__main__":
    # Example usage:
    draw_text_to_image("HELLO", font_size=200, output="hello.png")