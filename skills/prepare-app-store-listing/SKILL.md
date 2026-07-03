---
name: prepare-app-store-listing
description: Prepare App Store Connect listing packages for Apple platform apps. Use when the user types /store:prepare, /store:copy, /store:assets, /store:icon, /store:shots, /store:review, or /store:validate, or asks to analyze an app repository and generate App Store metadata, branding, app icons, screenshots, image assets, review notes, privacy/compliance prompts, pre-submission review risks, or an upload-ready manual submission folder; especially when Codex image generation is needed for logos, icons, or marketing imagery.
---

# Prepare App Store Listing

## Commands

Treat these as user prompt aliases:

- `/store:prepare`: run the full workflow for the current repository.
- `/store:copy`: generate or refresh only App Store text fields and reviewer/privacy notes.
- `/store:assets`: generate or refresh only brand assets, icon source art, and screenshot export targets.
- `/store:icon`: generate or resize only `brand/app-icon-1024.png`.
- `/store:shots`: prepare screenshot folders, screenshot plan, and resized screenshots from provided captures.
- `/store:review`: create or refresh `pre-submission-risk.md` with likely App Review blockers.
- `/store:validate`: run `asc_assets.py validate` and fix package issues when source files are available.

## Workflow

Create a manual App Store Connect submission package in `app-store-listing/`. Do not upload to App Store Connect or manage API credentials.

1. Inspect the repository first: README, package manifests, app config, `Info.plist`, Xcode projects, route/view files, screenshots, icons, and existing brand assets.
2. Read `references/apple-requirements.md` before finalizing metadata or image sizes. Read `references/review-risk-checklist.md` before writing review notes or `/store:review`. If network access is available, verify current Apple docs because screenshot targets change.
3. Run `python3 <skill>/scripts/asc_assets.py scaffold app-store-listing` to create the output shape.
4. Draft `app-store-fields.md` and `app-store-fields.json` with app name, subtitle, promotional text, description, keywords, category guess, support URL, marketing URL, version notes, and copyright.
5. Draft `review-notes.md` with reviewer instructions, demo account needs, sign-in notes, subscriptions/IAP notes, and any permissions the app requests.
6. Draft `pre-submission-risk.md` with likely rejection blockers found from repository evidence. Do not claim the app is compliant unless each risk is actually checked.
7. Draft `privacy-and-compliance-questions.md` for anything that cannot be proven from code, such as data collection, tracking, encryption export compliance, age rating, regulated content, and regional compliance.
8. Prefer existing brand assets. Generate new source art only when assets are missing or the user asks for a refresh.
9. Prefer real app screenshots. If the app cannot be run, create `screenshot-plan.md` and put any generated mockups under `draft-comps/`, clearly marked as not final App Store screenshots.
10. Export final images with `asc_assets.py resize` and verify with `asc_assets.py validate`.
11. Finish with `upload-checklist.md`, including every file path the user should upload or paste into App Store Connect.

## Image Rules

- Use image generation for source artwork: logo concepts, icon source art, brand board, and optional marketing backgrounds.
- Do not rely on image generation for exact App Store dimensions. Generate larger source images, then resize/crop with `asc_assets.py`.
- App screenshots should show the real app experience. Generated screenshots are drafts unless derived from actual app captures.
- Use plain PNG/JPG outputs. Flatten alpha for App Store icon exports.

## Script

Use the bundled script:

```bash
python3 <skill>/scripts/asc_assets.py scaffold app-store-listing
python3 <skill>/scripts/asc_assets.py resize source.png app-store-listing/brand/app-icon-1024.png 1024 1024 --mode cover
python3 <skill>/scripts/asc_assets.py resize source.png app-store-listing/screenshots/iphone-6.5/01.png 1242 2688 --mode cover
python3 <skill>/scripts/asc_assets.py validate app-store-listing
```

`resize` requires Pillow. If Pillow is unavailable, tell the user the exact install command and still produce metadata/checklists.

## Output Contract

Create this folder:

```text
app-store-listing/
  app-store-fields.md
  app-store-fields.json
  upload-checklist.md
  review-notes.md
  pre-submission-risk.md
  privacy-and-compliance-questions.md
  brand/
    app-icon-1024.png
    logo-source.png
    palette.json
    brand-board.png
  screenshots/
    iphone-6.9/
    iphone-6.5/
    ipad-13/
  draft-comps/
  validation-report.md
```

If a file is not applicable, omit it and say why in `upload-checklist.md`.
