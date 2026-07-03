#!/usr/bin/env python3
"""Small helpers for manual App Store Connect listing packages."""

from __future__ import annotations

import argparse
import binascii
import json
import struct
import sys
import tempfile
import zlib
from pathlib import Path


FIELD_LIMITS = {
    "name": 30,
    "subtitle": 30,
    "promotional_text": 170,
    "description": 4000,
}

SCREENSHOT_TARGETS = {
    "iphone-6.9": {(1260, 2736), (1290, 2796), (1320, 2868)},
    "iphone-6.5": {(1284, 2778), (1242, 2688)},
    "iphone-6.3": {(1179, 2556), (1206, 2622)},
    "iphone-6.1": {(1170, 2532), (1125, 2436), (1080, 2340)},
    "iphone-5.5": {(1242, 2208)},
    "iphone-4.7": {(750, 1334)},
    "iphone-4": {(640, 1096), (640, 1136)},
    "iphone-3.5": {(640, 920), (640, 960)},
    "ipad-13": {(2064, 2752), (2048, 2732)},
    "ipad-12.9": {(2048, 2732)},
    "ipad-11": {(1488, 2266), (1668, 2420), (1668, 2388), (1640, 2360)},
    "ipad-10.5": {(1668, 2224)},
    "ipad-9.7": {(1536, 2008), (1536, 2048), (768, 1004), (768, 1024)},
    "mac": {(1280, 800), (1440, 900), (2560, 1600), (2880, 1800)},
    "apple-tv": {(1920, 1080), (3840, 2160)},
    "vision-pro": {(3840, 2160)},
    "apple-watch": {(422, 514), (410, 502), (416, 496), (396, 484), (368, 448), (312, 390)},
}

IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg"}
REVERSIBLE_TARGETS = {target for target in SCREENSHOT_TARGETS if target.startswith(("iphone-", "ipad-"))}


def allowed_sizes(target: str) -> set[tuple[int, int]]:
    sizes = SCREENSHOT_TARGETS[target]
    if target in REVERSIBLE_TARGETS:
        return sizes | {(h, w) for w, h in sizes}
    return sizes


def png_info(path: Path) -> dict[str, object] | None:
    data = path.read_bytes()
    if not data.startswith(b"\x89PNG\r\n\x1a\n"):
        return None
    if data[12:16] != b"IHDR":
        raise ValueError(f"{path}: invalid PNG header")
    width, height = struct.unpack(">II", data[16:24])
    color_type = data[25]
    alpha = color_type in (4, 6) or b"tRNS" in data
    return {"format": "png", "width": width, "height": height, "alpha": alpha}


def jpeg_info(path: Path) -> dict[str, object] | None:
    data = path.read_bytes()
    if not data.startswith(b"\xff\xd8"):
        return None
    i = 2
    while i < len(data):
        if data[i] != 0xFF:
            i += 1
            continue
        marker = data[i + 1]
        i += 2
        if marker in (0xD8, 0xD9):
            continue
        length = struct.unpack(">H", data[i : i + 2])[0]
        if marker in {0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7, 0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF}:
            height, width = struct.unpack(">HH", data[i + 3 : i + 7])
            return {"format": "jpeg", "width": width, "height": height, "alpha": False}
        i += length
    raise ValueError(f"{path}: JPEG size marker not found")


def image_info(path: Path) -> dict[str, object]:
    info = png_info(path) or jpeg_info(path)
    if not info:
        raise ValueError(f"{path}: unsupported image format")
    return info


def field_errors(fields: dict[str, object]) -> list[str]:
    errors = []
    for key, limit in FIELD_LIMITS.items():
        value = str(fields.get(key, ""))
        if value and len(value) > limit:
            errors.append(f"app-store-fields.json:{key} is {len(value)} chars, max {limit}")
    keywords = str(fields.get("keywords", ""))
    keyword_bytes = len(keywords.encode("utf-8"))
    if keyword_bytes > 100:
        errors.append(f"app-store-fields.json:keywords is {keyword_bytes} bytes, max 100")
    short_keywords = [word.strip() for word in keywords.split(",") if 0 < len(word.strip()) <= 2]
    if short_keywords:
        errors.append(f"app-store-fields.json:keywords has short terms: {', '.join(short_keywords)}")
    return errors


def scaffold(root: Path) -> None:
    for child in [
        "brand",
        "screenshots/iphone-6.9",
        "screenshots/iphone-6.5",
        "screenshots/ipad-13",
        "draft-comps",
    ]:
        (root / child).mkdir(parents=True, exist_ok=True)

    fields = root / "app-store-fields.json"
    if not fields.exists():
        fields.write_text(
            json.dumps(
                {
                    "name": "",
                    "subtitle": "",
                    "promotional_text": "",
                    "description": "",
                    "keywords": "",
                    "category": "",
                    "support_url": "",
                    "marketing_url": "",
                    "version_notes": "",
                    "copyright": "",
                },
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )

    for name, title in {
        "app-store-fields.md": "App Store Fields",
        "upload-checklist.md": "Upload Checklist",
        "review-notes.md": "Review Notes",
        "privacy-and-compliance-questions.md": "Privacy and Compliance Questions",
    }.items():
        path = root / name
        if not path.exists():
            path.write_text(f"# {title}\n\n", encoding="utf-8")


def validate(root: Path) -> int:
    errors: list[str] = []
    warnings: list[str] = []

    fields_path = root / "app-store-fields.json"
    if fields_path.exists():
        errors.extend(field_errors(json.loads(fields_path.read_text(encoding="utf-8"))))

    icon_path = root / "brand" / "app-icon-1024.png"
    if icon_path.exists():
        info = image_info(icon_path)
        if (info["width"], info["height"]) != (1024, 1024):
            errors.append(f"{icon_path}: expected 1024x1024, got {info['width']}x{info['height']}")
        if info["format"] != "png":
            errors.append(f"{icon_path}: expected PNG")
        if info["alpha"]:
            errors.append(f"{icon_path}: expected no alpha/transparency")
    else:
        warnings.append(f"{icon_path}: missing")

    screenshots = root / "screenshots"
    for image in screenshots.rglob("*"):
        if not image.is_file() or image.suffix.lower() not in IMAGE_SUFFIXES:
            continue
        target = next((part for part in image.parts if part in SCREENSHOT_TARGETS), None)
        if not target:
            warnings.append(f"{image}: screenshot folder does not name a known target")
            continue
        info = image_info(image)
        size = (int(info["width"]), int(info["height"]))
        if size not in allowed_sizes(target):
            allowed = ", ".join(f"{w}x{h}" for w, h in sorted(allowed_sizes(target)))
            errors.append(f"{image}: got {size[0]}x{size[1]}, expected one of {allowed}")

    report = root / "validation-report.md"
    lines = ["# Validation Report", ""]
    lines += [f"- ERROR: {error}" for error in errors]
    lines += [f"- WARN: {warning}" for warning in warnings]
    if not errors and not warnings:
        lines.append("- OK")
    report.write_text("\n".join(lines) + "\n", encoding="utf-8")

    for line in lines:
        print(line)
    return 1 if errors else 0


def resize(source: Path, output: Path, width: int, height: int, mode: str) -> None:
    try:
        from PIL import Image, ImageOps
    except ImportError as exc:
        raise SystemExit("Pillow is required for resize: python3 -m pip install Pillow") from exc

    image = Image.open(source)
    if mode == "cover":
        resized = ImageOps.fit(image, (width, height), method=Image.Resampling.LANCZOS)
    else:
        resized = image.copy()
        resized.thumbnail((width, height), Image.Resampling.LANCZOS)
        canvas = Image.new("RGB", (width, height), "white")
        x = (width - resized.width) // 2
        y = (height - resized.height) // 2
        if resized.mode in ("RGBA", "LA"):
            canvas.paste(resized.convert("RGBA"), (x, y), resized.convert("RGBA"))
        else:
            canvas.paste(resized.convert("RGB"), (x, y))
        resized = canvas

    if resized.mode in ("RGBA", "LA"):
        flattened = Image.new("RGB", resized.size, "white")
        flattened.paste(resized, mask=resized.getchannel("A"))
        resized = flattened
    else:
        resized = resized.convert("RGB")

    output.parent.mkdir(parents=True, exist_ok=True)
    if output.suffix.lower() in {".jpg", ".jpeg"}:
        resized.save(output, quality=95, optimize=True)
    else:
        resized.save(output, optimize=True)


def check_keywords(keywords: str) -> int:
    errors = field_errors({"keywords": keywords})
    if errors:
        print("\n".join(errors))
        return 1
    print(f"OK: {len(keywords.encode('utf-8'))}/100 bytes")
    return 0


def png_bytes(width: int, height: int, color_type: int = 2) -> bytes:
    channels = 4 if color_type == 6 else 3
    row = b"\x00" + (b"\xff" * (width * channels))
    raw = row * height

    def chunk(kind: bytes, payload: bytes) -> bytes:
        checksum = binascii.crc32(kind + payload) & 0xFFFFFFFF
        return struct.pack(">I", len(payload)) + kind + payload + struct.pack(">I", checksum)

    ihdr = struct.pack(">IIBBBBB", width, height, 8, color_type, 0, 0, 0)
    return b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", ihdr) + chunk(b"IDAT", zlib.compress(raw)) + chunk(b"IEND", b"")


def self_test() -> int:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        rgb = root / "rgb.png"
        rgba = root / "rgba.png"
        rgb.write_bytes(png_bytes(1242, 2688, 2))
        rgba.write_bytes(png_bytes(1024, 1024, 6))
        assert image_info(rgb)["width"] == 1242
        assert image_info(rgb)["height"] == 2688
        assert image_info(rgb)["alpha"] is False
        assert image_info(rgba)["alpha"] is True
        assert (2778, 1284) in allowed_sizes("iphone-6.5")
        assert (800, 1280) not in allowed_sizes("mac")
        assert not field_errors({"keywords": "focus,notes,writing"})
        assert field_errors({"keywords": "x" * 101})
    print("OK")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("scaffold")
    p.add_argument("root", type=Path)

    p = sub.add_parser("validate")
    p.add_argument("root", type=Path)

    p = sub.add_parser("resize")
    p.add_argument("source", type=Path)
    p.add_argument("output", type=Path)
    p.add_argument("width", type=int)
    p.add_argument("height", type=int)
    p.add_argument("--mode", choices=["cover", "contain"], default="cover")

    p = sub.add_parser("check-keywords")
    p.add_argument("keywords")

    sub.add_parser("self-test")

    args = parser.parse_args(argv)
    if args.cmd == "scaffold":
        scaffold(args.root)
        return 0
    if args.cmd == "validate":
        return validate(args.root)
    if args.cmd == "resize":
        resize(args.source, args.output, args.width, args.height, args.mode)
        return 0
    if args.cmd == "check-keywords":
        return check_keywords(args.keywords)
    if args.cmd == "self-test":
        return self_test()
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
