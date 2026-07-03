# App Review Risk Checklist

Use this as a compact pre-submission risk pass, not a full legal/compliance audit. It borrows the useful shape from app review audit skills: group likely rejection issues by severity, cite repository evidence, and leave unknowns as questions.

## Critical

- Privacy policy missing from app or App Store metadata.
- App collects, tracks, or shares user data without visible consent or disclosure.
- Digital goods, subscriptions, premium features, credits, or content unlocks bypass StoreKit/IAP.
- App has account creation but no in-app account deletion path.
- Hardcoded production secrets, private keys, or credentials are present in client code.
- Private Apple APIs, dynamic code execution for new features, or hidden behavior are present.
- Submitted screenshots, app name, subtitle, or description misrepresent the actual app.

## High

- Social login exists without Sign in with Apple where Apple requires it.
- Tracking/ad SDKs are present without ATT handling.
- UGC exists without reporting, blocking, moderation, removal, and contact paths.
- Subscriptions lack clear pricing, terms, restore purchases, or cancellation guidance.
- Permission purpose strings are vague or ask for more access than the app needs.
- App requires sign-in before showing enough value, unless the product clearly needs authentication.
- App looks like a thin web wrapper, template clone, or low-functionality app.

## Medium

- Background modes, push notifications, Live Activities, or location are requested without clear product need.
- Placeholder text, debug logs, staging URLs, beta labels, or references to other platforms remain.
- Support URL, marketing URL, privacy URL, or review contact information is missing.
- Age rating, regulated content, health, finance, kids, gambling, VPN, or MDM implications are unclear.

## Output Format

Write `pre-submission-risk.md` with:

- `Critical`: direct blockers with file evidence.
- `High`: likely review questions or risky implementation gaps.
- `Medium`: polish and metadata risks.
- `Needs Human Confirmation`: facts code cannot prove.
- `Clean Checks`: high-risk areas inspected with no issue found.
