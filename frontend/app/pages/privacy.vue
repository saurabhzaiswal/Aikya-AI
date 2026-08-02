<template>
  <section class="page-shell py-16 sm:py-24">
    <article class="prose-aikya">
      <p class="eyebrow">
        Privacy policy
      </p>
      <h1>Privacy policy</h1>
      <p>
        Aikya AI respects the privacy of people who use the public website, authentication flow, and private workspace.
        This page explains the current privacy posture for the Phase 1 MVP and how personal, account, and translation-related
        information is handled within the service boundary that is available today.
      </p>

      <h2>1. What information we process</h2>
      <p>
        We may process account details such as your name, email address, workspace identifiers, translation input, uploaded
        digital PDF documents, generated translation output, security challenge metadata, and limited operational logs required
        to keep the product secure and functional.
      </p>

      <h2>2. How the information is used</h2>
      <p>
        We use this information to provide sign-in, workspace session management, document translation, activity tracking,
        abuse prevention, and service reliability. Translation content may be sent to a configured translation provider for
        processing as part of the workflow. Optional AI features are not used unless a future release expressly discloses and
        enables that capability.
      </p>

      <h2>3. Access, control, and retention</h2>
      <p>
        Access to workspace data is limited to the authenticated organization and session context that created it. Document
        retention is short-lived by design for the current Phase 1 MVP. Active deletion, retention cleanup automation, and
        formal production data-handling procedures remain part of the acceptance work that follows the current launch stage.
      </p>

      <h2>4. Cookies and local session data</h2>
      <p>
        The site may store browser-level preferences and localized account/session state needed to support browsing and secure
        access. Where a cookie or similar storage is required for security or private-route operation, it is used only for the
        necessary product function.
      </p>

      <h2>5. Security and incident handling</h2>
      <p>
        We apply reasonable security safeguards, including authenticated session handling, signed state, rate limiting,
        tenant-scope checks, and access-control boundaries. While we take reasonable care, no system can guarantee the
        absolute prevention of every data loss or unauthorized disclosure.
      </p>

      <h2>6. Sharing and international transfer</h2>
      <p>
        Information may be shared only with service operators, infrastructure providers, and security or reliability partners
        that are necessary to deliver the current product. When needed for operational support, information may be processed in
        systems or jurisdictions outside the country in which you first submitted it. We will apply reasonable steps to protect
        that information under the current legal and technical posture of the service.
      </p>

      <h2>7. Your rights and questions</h2>
      <p>
        If you have questions about your account data, the current privacy posture, or a suspected incident, contact the
        verified founder public channels listed on the <NuxtLink to="/contact">contact page</NuxtLink>. A formal production
        privacy contact, subprocessors list, and full rights-management process remain part of the legal acceptance work that
        follows this MVP stage.
      </p>

      <p class="text-sm text-muted">
        Last updated: 7 May 2026
      </p>
    </article>
  </section>
</template>

<script setup lang="ts">
import { PAGE_METADATA } from '~/seo/metadata'

usePageSeo(PAGE_METADATA.privacy)
</script>
