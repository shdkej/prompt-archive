#!/usr/bin/env python3
import argparse
import datetime as dt
import hashlib
import json
import os
import re
import textwrap
from pathlib import Path

import requests
from PIL import Image, ImageDraw, ImageFont


UPLOAD_ENDPOINT = "https://upload.shdkej.com?kind=derived"
FONT_REGULAR = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
FONT_BOLD = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"


def slugify(value):
    value = re.sub(r"[^0-9A-Za-z가-힣]+", "-", value).strip("-")
    return value[:48] or "travel-content"


def load_font(path, size):
    return ImageFont.truetype(path, size)


def wrap_by_width(draw, text, font, max_width):
    lines = []
    for paragraph in text.split("\n"):
        current = ""
        for ch in paragraph:
            candidate = current + ch
            if draw.textbbox((0, 0), candidate, font=font)[2] <= max_width:
                current = candidate
            else:
                if current:
                    lines.append(current)
                current = ch
        if current:
            lines.append(current)
    return lines


def draw_text_block(draw, xy, lines, font, fill, line_gap):
    x, y = xy
    for line in lines:
        draw.text((x, y), line, font=font, fill=fill)
        bbox = draw.textbbox((x, y), line, font=font)
        y += (bbox[3] - bbox[1]) + line_gap
    return y


def measure_lines(draw, lines, font, line_gap):
    height = 0
    width = 0
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        width = max(width, bbox[2] - bbox[0])
        height += (bbox[3] - bbox[1]) + line_gap
    return width, max(0, height - line_gap)


def fit_wrapped_text(draw, text, font_path, start_size, min_size, max_width, max_lines):
    for size in range(start_size, min_size - 1, -2):
        font = load_font(font_path, size)
        lines = wrap_by_width(draw, text, font, max_width)
        if len(lines) <= max_lines:
            return font, lines
    font = load_font(font_path, min_size)
    lines = wrap_by_width(draw, text, font, max_width)
    return font, lines[:max_lines]


def render_card(context, out_dir):
    width, height = 1080, 1350
    img = Image.new("RGB", (width, height), "#030405")
    draw = ImageDraw.Draw(img)

    location = context.get("location", "오늘의 여행지")
    title = context.get("title", "세계여행은 휴가가 아니었습니다")
    copy = context.get("copy", "낯선 도시를 지날 때마다, 내가 뭘 좋아하고 뭘 남기고 싶은지 더 선명해졌습니다.")
    angle = context.get("angle", "여행은 휴가가 아니라 기준을 만드는 실험이다")
    date_text = context.get("date", dt.datetime.now().strftime("%Y-%m-%d"))

    accent = "#20d9df"
    white = "#f4f7f7"
    muted = "#9aa2a6"
    left = 108
    max_width = 840

    title_font, title_lines = fit_wrapped_text(draw, title, FONT_BOLD, 64, 48, max_width, 2)
    body_source = copy.strip() or angle.strip()
    body_source = re.sub(r"\s+", " ", body_source)
    body_font, body_lines = fit_wrapped_text(draw, body_source, FONT_REGULAR, 53, 40, max_width, 5)

    title_height = measure_lines(draw, title_lines, title_font, 16)[1]
    body_height = measure_lines(draw, body_lines, body_font, 18)[1]
    block_height = title_height + 74 + body_height
    y = max(330, int((height - block_height) * 0.52))

    draw_text_block(draw, (left, y), title_lines, title_font, accent, 16)
    y += title_height + 74

    for idx, line in enumerate(body_lines):
        fill = accent if idx == 1 and len(body_lines) >= 3 else white
        draw.text((left, y), line, font=body_font, fill=fill)
        bbox = draw.textbbox((left, y), line, font=body_font)
        y += (bbox[3] - bbox[1]) + 18

    if context.get("show_context_footer"):
        footer_font = load_font(FONT_REGULAR, 28)
        draw.text((left, 1212), f"{date_text} · {location}", font=footer_font, fill=muted)

    out_dir.mkdir(parents=True, exist_ok=True)
    seed = f"{date_text}-{location}-{title}-{copy}"
    digest = hashlib.sha1(seed.encode("utf-8")).hexdigest()[:8]
    run_id = f"{date_text}-{slugify(location)}-{digest}"
    image_path = out_dir / f"{run_id}.png"
    img.save(image_path, "PNG", optimize=True)
    return run_id, image_path


def upload_image(image_path):
    token = os.environ.get("CLOUDFLARE_IMAGE_UPLOAD_TOKEN")
    if not token:
        return None
    with open(image_path, "rb") as f:
        response = requests.post(
            UPLOAD_ENDPOINT,
            data=f,
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "image/png",
            },
            timeout=45,
        )
    response.raise_for_status()
    text = response.text.strip()
    try:
        data = response.json()
        for key in ("url", "publicUrl", "public_url", "href"):
            if key in data:
                return data[key]
    except Exception:
        pass
    return text


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--context-json", required=True)
    parser.add_argument("--out-dir", required=True)
    parser.add_argument("--no-upload", action="store_true")
    args = parser.parse_args()

    with open(args.context_json, "r", encoding="utf-8") as f:
        context = json.load(f)

    out_dir = Path(args.out_dir)
    run_id, image_path = render_card(context, out_dir)
    upload_url = None if args.no_upload else upload_image(image_path)

    metadata = {
        "run_id": run_id,
        "created_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "image_path": str(image_path),
        "upload_url": upload_url,
        "context": context,
    }
    metadata_path = out_dir / f"{run_id}.json"
    metadata_path.write_text(json.dumps(metadata, ensure_ascii=False, indent=2), encoding="utf-8")

    print(json.dumps({"run_id": run_id, "image_path": str(image_path), "upload_url": upload_url, "metadata_path": str(metadata_path)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
