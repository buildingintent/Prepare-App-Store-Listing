# Prepare App Store Listing

Codex skill for preparing manual App Store Connect listing packages. It creates metadata drafts, brand assets, screenshot export targets, reviewer notes, privacy questions, and validation reports. It does not upload to App Store Connect.

## Install

From GitHub with the open skills CLI:

```bash
npx skills add buildingintent/Prepare-App-Store-Listing --skill prepare-app-store-listing -g -a codex -y
```

After publishing to npm:

```bash
npx prepare-app-store-listing-skill
```

Restart Codex, then run:

```text
/store:prepare
```

## Commands

- `/store:prepare`: full package
- `/store:copy`: text fields and review notes
- `/store:assets`: branding and screenshot assets
- `/store:icon`: 1024 icon only
- `/store:shots`: screenshots only
- `/store:review`: pre-submission risk notes
- `/store:validate`: validate generated package
