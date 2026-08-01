# Pricing and Entitlements Strategy

Status: Proposal; no public prices approved

## Principles

- Price the outcome while metering the underlying cost drivers.
- Make limits understandable before upload and visible during use.
- Never market infrastructure-backed features as literally unlimited.
- Separate translation quality/privacy tiers explicitly.
- Version entitlements so plan changes do not rewrite active subscriptions.
- Do not finalize currency or price points until provider benchmarks and customer interviews establish unit economics.

## Proposed packaging

| Capability | Free | Pro | Business | Enterprise |
|---|---:|---:|---:|---:|
| Plain-text translation | limited | included | included | contracted |
| Document pages/month | small allowance | higher allowance | pooled allowance | committed volume |
| OCR | bounded | included | included | policy-controlled |
| Quality/provider tier | standard | enhanced | enhanced | configured/private |
| File size/page limit | low | medium | high | negotiated |
| Processing priority/concurrency | standard/1 | priority/small | pooled | reserved capacity |
| History and retention | short | configurable | organization policy | custom/residency |
| Comparison | preview | full | full | full |
| AI and audio | trial/none | metered | pooled | configured |
| Glossary/translation memory | none | personal | organization | governed/importable |
| Members/RBAC | personal | personal | team | enterprise |
| API access | none | optional | included tier | contract/SLA |
| SSO, SCIM, audit export | none | none | optional | included/contracted |

## Metering model

The product may present a simple “page allowance,” but backend accounting records the actual cost drivers:

- Translation characters by quality/provider tier.
- OCR pages or image megapixels.
- Render pages and resource class.
- AI input/output units.
- Speech characters or generated seconds.
- Storage byte-days and download egress where relevant.

A displayed page unit needs a documented normalization rule. A page with extreme character density, very high resolution, or OCR complexity may consume more than one unit only if disclosed before processing.

## Quota behavior

Before starting a job, reserve estimated units. On completion, settle actual units and release the balance. On permanent failure caused by Aikya/provider infrastructure, do not charge unproduced output. User-invalid files may consume only explicitly disclosed validation cost, preferably zero during beta.

Soft limits warn and invite upgrade. Hard limits prevent new work but do not block access to existing data. Organization admins see pooled usage, top consumers, limits, reset dates, and forecast.

## Price discovery

Before assigning prices:

1. Benchmark provider/compute/storage/support cost by workload.
2. Set gross-margin targets by plan and stress provider price changes.
3. Interview users about value and preferred metric.
4. Run willingness-to-pay tests with real landing/checkout intent.
5. Pilot a small set of price points and measure activation, conversion, workload mix, support, and retention.

## Billing rules to define

- Trial length and whether payment method is required.
- Monthly/annual discounts, regional currencies, tax collection, and invoice requirements.
- Upgrade/downgrade effective dates and proration.
- Overage opt-in, spend caps, prepaid credits, and expiration.
- Failed-payment grace period and read-only behavior.
- Refund policy and consumer cancellation rights.
- Enterprise minimum commitment and service credits.

## Abuse and cost protection

Rate limit by identity, organization, network, API key, and job class. Enforce concurrency and daily burst limits even when monthly allowance remains. Detect automation abuse and stolen credentials without inspecting document text. Provider circuit breakers and budget alarms stop cost cascades.
