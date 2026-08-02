---
title: Phase 1 user guide
description: Understand the current Aikya AI MVP workflow, limits, privacy posture, and where the product is intentionally scoped today.
---

# Phase 1 user guide

Aikya AI Phase 1 is a focused translation workspace. It is designed to handle the most important core actions clearly and reliably: text translation, readable document translation for supported PDFs, and private work-session flow for authenticated users.

## What is currently supported

Phase 1 supports:

- text translation with source-language detection or a manually selected source language
- translation into a supported target language
- translation of digital PDFs that contain embedded text
- a short-lived document download flow after processing completes
- basic workspace activity and account access boundaries for the private MVP release

## Translate text

1. Open the translation workspace from the main product flow.
2. Choose the source language manually or leave auto-detection enabled.
3. Select the target language.
4. Enter up to 10,000 characters of source text.
5. Submit the translation and review the generated output.

## Translate a digital PDF

1. Upload a PDF file that contains embedded text.
2. Select the target language for the translation run.
3. Follow the step-by-step processing stages shown in the workspace.
4. When the translation is ready, use the short-lived download link to retrieve the readable export.

## Current operational limits

- PDF files only
- Maximum 50 MB file size
- Maximum 100 pages per uploaded document
- Scanned PDFs are not supported yet
- Readable export does not preserve the original visual layout exactly
- The service is intentionally limited to the MVP scope described in the public roadmap and product notes

## Privacy and data handling

Document content is sent to the translation provider configured by the service operator for the requested workflow. Optional AI features are not invoked in Phase 1.

## Quality expectation

The output should be reviewed by the user before it is used for formal, legal, contractual, medical, financial, or other high-stakes decisions. Machine translation is helpful, but it is not a substitute for human review in regulated or sensitive contexts.

## What remains outside Phase 1

OCR for scanned pages, layout-preserving PDF rendering, billing, account-scale lifecycle orchestration, and other future capability work are intentionally left out of this release. They will be added only after the core workflow is stable, explainable, and operationally reliable.

## Support and contact

If you have questions about the workflow, a current limitation, or support availability, use the verified founder contact details listed on the public contact page.
