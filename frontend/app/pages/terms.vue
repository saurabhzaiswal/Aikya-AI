<template>
  <section class="page-shell py-16 sm:py-24">
    <article class="prose-aikya">
      <p class="eyebrow">
        Terms &amp; conditions
      </p>
      <h1>Terms of service</h1>
      <p>
        These Terms govern access to the public Aikya AI website and the Phase 1 workspace experience made available by the
        Aikya AI team. By using the site, you confirm that you have read and understood these Terms and that you are acting
        within the lawful scope of your authority.
      </p>

      <h2>1. Scope of the service</h2>
      <p>
        Aikya AI currently provides a focused Phase 1 service for text translation and readable translation of supported,
        embedded-text digital PDF documents. The product is an MVP and is intentionally limited in scope. Additional
        features, workflows, integrations, analytics depth, custom compliance controls, and production-grade reliability
        commitments remain outside the current release unless explicitly documented in a separate written agreement.
      </p>

      <h2>2. Lawful and permitted use</h2>
      <p>
        You may use the service only for lawful purposes and only with content that you are authorized to process. You must
        not upload, submit, or transmit material that infringes the rights of others, contains harmful content, or otherwise
        breaches applicable law, contractual terms, or reasonable platform safety boundaries.
      </p>
      <p>
        You must not attempt to reverse-engineer the service, scrape or harvest site content in bulk, abuse the authentication
        or secure workspace flow, or interfere with the integrity, availability, or performance of the website or associated
        operations.
      </p>

      <h2>3. Your content and responsibility</h2>
      <p>
        You remain responsible for the content you provide, the accuracy of the information you submit, and any rights or
        permissions required to translate, store, process, or export that content. Aikya AI retains ownership of the
        software, interface, configuration, and product-specific assets used to provide the service.
      </p>

      <h2>4. Translation quality and limitations</h2>
      <p>
        Machine translation can produce errors, omissions, or output that is not suitable for certified, legal, medical,
        financial, or other regulated use. You must review the translated output before relying on it for formal, contractual,
        legal, or high-stakes decisions.
      </p>

      <h2>5. Availability, security, and account use</h2>
      <p>
        We aim to keep the service available, secure, and understandable, but we do not guarantee uninterrupted access,
        perfect reliability, or the complete absence of failures. You must keep your account credentials confidential and
        promptly notify the team of any suspected misuse or security incident.
      </p>

      <h2>6. Privacy and data handling</h2>
      <p>
        Personal information, workspace activity, translation inputs, document metadata, and related operational logs may be
        processed to operate sign-in, session handling, translation requests, abuse prevention, and service reliability. The
        current privacy posture is described in the <NuxtLink to="/privacy">privacy policy</NuxtLink> and should be reviewed
        before you submit meaningful content.
      </p>

      <h2>7. Changes, suspension, and contact</h2>
      <p>
        These Terms may be updated as the product evolves from MVP into a broader public service. When changes are material,
        they will be announced through the public site or relevant service channels. If the service is suspended, restricted,
        or discontinued, we may provide notice where practicable and reasonable under the circumstances.
      </p>
      <p>
        Questions or support requests can be sent through the verified founder contact details listed on the
        <NuxtLink to="/contact">contact page</NuxtLink>.
      </p>

      <h2>8. Disclaimers and liability</h2>
      <p>
        The service is provided on an as-is basis for the current Phase 1 scope. We do not promise flawless translation,
        exact availability, or future delivery of additional product capabilities. To the maximum extent permitted by law,
        Aikya AI limits liability to the practical extent allowed for a current MVP website and workspace service.
      </p>

      <p class="text-sm text-muted">
        Last updated: 7 May 2026
      </p>
    </article>
  </section>
</template>

<script setup lang="ts">
import { PAGE_METADATA } from '~/seo/metadata'

usePageSeo(PAGE_METADATA.terms)
</script>
