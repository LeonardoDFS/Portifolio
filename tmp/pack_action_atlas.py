from pathlib import Path
import numpy as np
from PIL import Image

source = Path(r"C:\Users\Leonardo\.codex\generated_images\01a131df-e371-7d00-a230-7e6b12d4856b\exec-b93e4051-8804-46f5-b366-03feba330c4e.png")
image = Image.open(source).convert("RGBA")
if image.size != (1536, 1024):
    raise ValueError(f"Expected 6x4 square-cell source atlas, got {image.size}")

rgba = np.asarray(image)
alpha = rgba[:, :, 3]
atlas = Image.new("RGBA", (192, 128), (0, 0, 0, 0))

# Preserve the original cell-relative movement while reducing each cell to 32x32.
# Transparent background haze is removed; pixel boundaries stay hard.
frames_per_row = [4, 4, 6, 2]
for row in range(4):
    for col in range(6):
        if col >= frames_per_row[row]:
            continue
        cell = Image.fromarray(rgba[row * 256:(row + 1) * 256, col * 256:(col + 1) * 256, :])
        if np.asarray(cell.getchannel("A")).max() < 40:
            continue
        small = cell.resize((32, 32), Image.Resampling.NEAREST)
        arr = np.asarray(small).copy()
        arr[:, :, 3] = np.where(arr[:, :, 3] >= 128, 255, 0).astype(np.uint8)
        small = Image.fromarray(arr, "RGBA")
        atlas.alpha_composite(small, (col * 32, row * 32))

# Shared compact palette across all frames, retaining transparent pixels.
palette = atlas.convert("RGB").quantize(colors=16, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)
result = palette.convert("RGB").convert("RGBA")
result.putalpha(atlas.getchannel("A"))

out_dir = Path("assets")
out_dir.mkdir(exist_ok=True)
output = out_dir / "robot_actions_32px.png"
result.save(output, optimize=True)
preview = result.resize((768, 512), Image.Resampling.NEAREST)
preview.save(Path("tmp") / "robot_actions_32px_preview.png")

check = Image.open(output).convert("RGBA")
if check.size != (192, 128):
    raise ValueError(f"Unexpected output size: {check.size}")
print(f"Output: {output.resolve()} {check.size}, 6 columns x 4 rows, 32x32 per frame")
print("Rows: idle 4 frames; jump 4 frames; empty-handed arm gesture 6 frames; hurt 2 frames.")
print("Alpha extrema:", check.getchannel("A").getextrema())
