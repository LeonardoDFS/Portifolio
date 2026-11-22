from pathlib import Path
import numpy as np
from PIL import Image

source = Path(r"C:\Users\Leonardo\.codex\generated_images\01a131df-e371-7d00-a230-7e6b12d4856b\exec-6e1d493f-0268-45d2-9417-8258a62bda2b.png")
out_dir = Path("assets")
out_dir.mkdir(exist_ok=True)
image = Image.open(source).convert("RGBA")
rgba = np.asarray(image)
alpha = rgba[:, :, 3]

# The generated strip has eight separated characters. Detect their x extents
# from visible pixels, ignoring faint alpha specks in the transparent field.
active_columns = np.flatnonzero(((alpha > 10).sum(axis=0)) > 5)
runs = []
if active_columns.size:
    start = previous = int(active_columns[0])
    for x in active_columns[1:]:
        x = int(x)
        if x > previous + 1:
            runs.append((start, previous + 1))
            start = x
        previous = x
    runs.append((start, previous + 1))

if len(runs) != 8:
    raise ValueError(f"Expected 8 separated frames, found {len(runs)}: {runs}")

frames = []
boxes = []
for left, right in runs:
    region = rgba[:, left:right, :]
    mask = region[:, :, 3] >= 128
    ys, xs = np.where(mask)
    if len(xs) == 0:
        raise ValueError(f"Frame at x={left} has no visible pixels")
    box = (int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1)
    crop = Image.fromarray(region).crop(box)
    frames.append(crop)
    boxes.append(crop.size)

# Use one scale for all frames to keep the character size stable, then place
# each frame on a 32x32 transparent cell with a shared foot baseline.
max_w = max(w for w, h in boxes)
max_h = max(h for w, h in boxes)
scale = min(30 / max_w, 30 / max_h)
packed = Image.new("RGBA", (256, 32), (0, 0, 0, 0))
for i, frame in enumerate(frames):
    width = max(1, round(frame.width * scale))
    height = max(1, round(frame.height * scale))
    small = frame.resize((width, height), Image.Resampling.NEAREST)
    arr = np.asarray(small).copy()
    # Pixel art uses hard transparency; remove semi-transparent edge halos.
    arr[:, :, 3] = np.where(arr[:, :, 3] >= 128, 255, 0).astype(np.uint8)
    small = Image.fromarray(arr, "RGBA")
    x = i * 32 + (32 - width) // 2
    y = 31 - height
    packed.alpha_composite(small, (x, y))

# Reduce color noise while retaining a single shared palette across all poses.
rgb = packed.convert("RGB")
palette = rgb.quantize(colors=16, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)
quantized = palette.convert("RGB").convert("RGBA")
quantized.putalpha(packed.getchannel("A"))

output = out_dir / "robot_walk_8f_256x32.png"
quantized.save(output, optimize=True)
preview = quantized.resize((1024, 128), Image.Resampling.NEAREST)
preview.save(Path("tmp") / "robot_walk_8f_preview.png")

check = Image.open(output)
if check.size != (256, 32):
    raise ValueError(f"Unexpected output size: {check.size}")
print(f"Source: {image.size}; detected frame bounds: {runs}; frame crops: {boxes}")
print(f"Output: {output.resolve()} {check.size}")
