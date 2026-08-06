import os
from PIL import Image, ImageDraw, ImageFont

# Let's create a stunning, modern, aesthetic, premium app logo for 'CashPilot'
# Dimensions for high-res PNG
width = 1024
height = 1024

# Create image with a subtle dark luxury/modern financial gradient or deep rich background
# Let's use a deep midnight navy/slate background with a rich teal/emerald glowing accent (representing money/pilot/navigation)
img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
draw = ImageDraw.Draw(img)

# Draw rounded rectangle for app icon base
# Corner radius approx 22% of size (standard modern icon radius)
radius = 226
margin = 0
shape_box = [margin, margin, width - margin, height - margin]

# Create background with a sleek gradient or solid rich dark tone
# Deep space navy / charcoal: #0B132B / #1C2541 with a subtle radial gradient feel
# Let's draw a rounded rectangle with a sophisticated dark gradient or solid color + glow
for i in range(radius * 2):
    pass # we can draw solid with smooth antialiasing using PIL's rounded rectangle if available, or custom mask

# Let's create a high quality mask for rounded corners
mask = Image.new("L", (width, height), 0)
mask_draw = ImageDraw.Draw(mask)
mask_draw.rounded_rectangle([0, 0, width, height], radius=240, fill=255)

# Background color: Deep luxury slate/navy #0F172A
bg_layer = Image.new("RGBA", (width, height), (15, 23, 42, 255))

# Let's draw modern aesthetic geometric financial / pilot elements:
# A stylized 'C' combined with a paper airplane / financial upward growth trajectory / compass / jet stream.
# "CashPilot": Cash (money, green/teal/gold) + Pilot (navigation, wings, upward trajectory, clean lines)

content_layer = Image.new("RGBA", (width, height), (0, 0, 0, 0))
c_draw = ImageDraw.Draw(content_layer)

# Center of canvas
cx, cy = width // 2, height // 2 - 30

# Draw a sleek futuristic glowing gradient circle or abstract ring as background HUD / radar / coin
# Outer ring subtle glow
c_draw.ellipse([cx - 320, cy - 320, cx + 320, cy + 320], outline=(30, 41, 59, 255), width=4)
c_draw.arc([cx - 360, cy - 360, cx + 360, cy + 360], start=200, end=380, fill=(16, 185, 129, 40), width=12)

# Let's design the core symbol: An elegant financial arrow / paper airplane formed by sleek geometric facets, 
# representing cashflow going UP and forward, intertwined with a minimalist 'C' shape.
# Coordinates for the main upward soaring jet / financial arrow:
# Tip pointing top-right (growth, piloting forward)
# Let's create polygon coordinates for a stunning origami-style sleek jet / paper airplane in vibrant emerald & mint gradient
points_wing_left = [(cx - 180, cy + 120), (cx - 40, cy - 40), (cx - 40, cy + 180)]
points_wing_right = [(cx + 180, cy - 140), (cx - 40, cy - 40), (cx - 40, cy + 180)]
points_center = [(cx - 40, cy - 40), (cx + 180, cy - 140), (cx + 60, cy + 60)]

# Using smooth gradients or solid rich modern colors (Emerald #10B981, Mint #34D399, Cyan #06B6D4)
# Left wing (deep emerald)
c_draw.polygon([(cx - 160, cy + 100), (cx - 20, cy - 80), (cx - 20, cy + 160)], fill=(16, 185, 129, 230))
# Right wing (vibrant bright mint/cyan gradient look)
c_draw.polygon([(cx + 160, cy - 120), (cx - 20, cy - 80), (cx - 20, cy + 160)], fill=(52, 211, 153, 255))
# Center crease / highlight line simulating cashflow upward chart bar / origami fold
c_draw.polygon([(cx - 20, cy - 80), (cx + 160, cy - 120), (cx + 40, cy + 40)], fill=(110, 231, 183, 255))

# Add a subtle currency symbol ($) or cashflow wave integrated gracefully into the tail or background, 
# or keep it ultra-clean and modern like top fintech apps (Stripe, Revolut, Mercury style).
# Let's add a sleek upward cashflow trend line crossing through
c_draw.arc([cx - 280, cy - 280, cx + 280, cy + 280], start=130, end=250, fill=(6, 182, 212, 200), width=8)

# Add text "CASHPILOT" below the icon in clean modern typography
try:
    # Try loading a clean sans-serif font if available, otherwise default
    font_large = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 72)
    font_sub = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 28)
except:
    font_large = ImageFont.load_default()
    font_sub = ImageFont.load_default()

# Draw "CASHPILOT" text with tracking/spacing feel
text = "CASHPILOT"
# We can draw text centered near the bottom
text_bbox = c_draw.textbbox((0, 0), text, font=font_large)
tw = text_bbox[2] - text_bbox[0]
th = text_bbox[3] - text_bbox[1]
tx = (width - tw) // 2
ty = height - 160

# Draw subtle glow under text
c_draw.text((tx, ty), text, fill=(255, 255, 255, 240), font=font_large)

# Subtitle / Tagline
subtext = "CASHFLOW NAVIGATION"
sub_bbox = c_draw.textbbox((0, 0), subtext, font=font_sub)
sw = sub_bbox[2] - sub_bbox[0]
sx = (width - sw) // 2
sy = ty + 85
c_draw.text((sx, sy), subtext, fill=(148, 163, 184, 255), font=font_sub)

# Composite background with mask
final_img = Image.composite(bg_layer, Image.new("RGBA", (width, height), (0, 0, 0, 0)), mask)
# Paste content over background
final_img.alpha_composite(content_layer)

# Save PNG
png_path = "cashpilot_logo.png"
final_img.save(png_path, "PNG")

# Save ICO (multi-resolution for standard .ico formats: 256x256, 128x128, 64x64, 32x32, 16x16)
ico_path = "cashpilot_logo.ico"
icon_sizes = [(256, 256), (128, 128), (64, 64), (32, 32), (16, 16)]
final_img.save(ico_path, format="ICO", sizes=icon_sizes)

print("Logo generated successfully in both PNG and ICO formats.")