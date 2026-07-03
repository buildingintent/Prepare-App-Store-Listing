# Apple App Store Connect Requirements

Baseline checked against Apple Developer documentation on 2026-07-03. Verify current Apple docs before final delivery when network access is available:

- Screenshot specifications: `https://developer.apple.com/help/app-store-connect/reference/app-information/screenshot-specifications/`
- Upload screenshots/previews: `https://developer.apple.com/help/app-store-connect/manage-app-information/upload-app-previews-and-screenshots/`
- Platform version metadata: `https://developer.apple.com/help/app-store-connect/reference/app-information/platform-version-information/`
- App information: `https://developer.apple.com/help/app-store-connect/reference/app-information/app-information`

## Metadata Limits

- App name: 2-30 characters.
- Subtitle: max 30 characters.
- Promotional text: max 170 characters.
- Description: max 4000 characters, plain text.
- Keywords: max 100 bytes total, comma-separated, each keyword greater than 2 characters, do not duplicate app/company name.
- Privacy Policy URL: required for iOS and macOS apps.

## Screenshots

Upload 1-10 screenshots per supported device size/localization. Accepted formats: `.jpeg`, `.jpg`, `.png`.

If the UI is the same across device sizes and localizations, Apple may scale from the highest required screenshot. Prefer exact exports when the user asks for complete assets.

### iPhone Portrait Sizes

- `iphone-6.9`: `1260x2736`, `1290x2796`, `1320x2868`
- `iphone-6.5`: `1284x2778`, `1242x2688`
- `iphone-6.3`: `1179x2556`, `1206x2622`
- `iphone-6.1`: `1170x2532`, `1125x2436`, `1080x2340`
- `iphone-5.5`: `1242x2208`
- `iphone-4.7`: `750x1334`
- `iphone-4`: `640x1096`, `640x1136`
- `iphone-3.5`: `640x920`, `640x960`

Landscape screenshots use the reversed dimensions.

### iPad Portrait Sizes

- `ipad-13`: `2064x2752`, `2048x2732`
- `ipad-12.9`: `2048x2732`
- `ipad-11`: `1488x2266`, `1668x2420`, `1668x2388`, `1640x2360`
- `ipad-10.5`: `1668x2224`
- `ipad-9.7`: `1536x2008`, `1536x2048`, `768x1004`, `768x1024`

Landscape screenshots use the reversed dimensions.

### Other Platforms

- Mac: `1280x800`, `1440x900`, `2560x1600`, or `2880x1800`.
- Apple TV: `1920x1080` or `3840x2160`.
- Apple Vision Pro: `3840x2160`.
- Apple Watch: one consistent size across localizations: `422x514`, `410x502`, `416x496`, `396x484`, `368x448`, or `312x390`.

## App Icon

For iOS/iPadOS asset catalogs, include an App Store marketing icon as `1024x1024` PNG without transparency. Let Xcode generate smaller app icon sizes when possible.

## Review Safety

- Final screenshots should represent the real app UI and user experience.
- Generated UI mockups belong in `draft-comps/` unless they are composited from real captures.
- Do not invent privacy answers, age ratings, login credentials, legal claims, medical/financial claims, or third-party content rights.
