<template>
  <main class="policy-page">
    <article class="policy-shell">
      <p class="eyebrow">Generic application policy</p>
      <h1>Privacy Policy</h1>
      <p class="updated">Effective date: 23 August 2026</p>

      <section>
        <h2>Overview</h2>
        <p>
          This privacy policy is a general policy for applications developed by
          Timmy Huang. It explains how information may be collected, used, and
          protected when someone uses one of these applications.
        </p>
      </section>

      <section>
        <h2>Information Collected</h2>
        <p>
          Applications may collect information that users provide directly, such as
          account details, preferences, form submissions, support requests, or other
          content needed for the application to work.
        </p>
        <p>
          Applications may also collect technical information such as device type,
          browser type, IP address, usage logs, crash reports, and analytics data.
        </p>
      </section>

      <section>
        <h2>How Information Is Used</h2>
        <p>
          Information may be used to provide app functionality, maintain and improve
          the service, respond to support requests, protect against misuse, comply
          with legal obligations, and understand how applications are performing.
        </p>
      </section>

      <section>
        <h2>Third-Party Services</h2>
        <p>
          Applications may use third-party services for hosting, authentication,
          analytics, databases, payments, messaging, or other operational needs.
          Those services may process information according to their own privacy
          policies and terms.
        </p>
      </section>

      <section>
        <h2>Data Sharing</h2>
        <p>
          Personal information is not sold. Information may be shared with service
          providers that help operate the applications, when required by law, or
          when necessary to protect users, the public, or the applications.
        </p>
      </section>

      <section>
        <h2>Data Retention</h2>
        <p>
          Information is retained only as long as reasonably needed for the purposes
          described in this policy, unless a longer retention period is required or
          permitted by law.
        </p>
      </section>

      <section>
        <h2>Security</h2>
        <p>
          Reasonable technical and organizational measures are used to protect
          information. No online service can guarantee perfect security, but care is
          taken to reduce risk and respond to issues appropriately.
        </p>
      </section>

      <section>
        <h2>User Choices</h2>
        <p>
          Users may request access, correction, or deletion of their personal
          information where applicable. Some information may need to be retained for
          legal, security, or operational reasons.
        </p>
      </section>

      <section>
        <h2>Children</h2>
        <p>
          These applications are not intended to knowingly collect personal
          information from children without appropriate consent. If such information
          has been provided, contact support to request review or deletion.
        </p>
      </section>

      <section>
        <h2>Changes</h2>
        <p>
          This policy may be updated from time to time. Changes will be reflected
          by updating the effective date on this page.
        </p>
      </section>

      <section>
        <h2>Contact</h2>
        <p>
          For privacy questions, support requests, or deletion requests, email
          <a href="mailto:timmyme2@gmail.com">timmyme2@gmail.com</a>.
        </p>
      </section>
    </article>
  </main>
</template>

<script lang="ts" setup>
useHead({
  title: 'Privacy Policy',
  meta: [
    {
      name: 'description',
      content: 'Generic privacy policy for applications developed by Timmy Huang.',
    },
  ],
})
</script>

<style scoped>
.policy-page {
  background: #f7f8fb;
  color: #1d2433;
  padding: 48px 16px 64px;
}

.policy-shell {
  background: #ffffff;
  border: 1px solid #dde3ee;
  border-radius: 8px;
  margin: 0 auto;
  max-width: 860px;
  padding: 40px;
}

.eyebrow {
  color: #345995;
  font-size: 0.82rem;
  font-weight: 700;
  letter-spacing: 0;
  margin: 0 0 12px;
  text-transform: uppercase;
}

h1 {
  font-size: clamp(2rem, 5vw, 3.4rem);
  line-height: 1.08;
  margin: 0;
}

.updated {
  color: #667085;
  margin: 14px 0 32px;
}

section {
  border-top: 1px solid #e4e9f2;
  padding-top: 24px;
}

section + section {
  margin-top: 24px;
}

h2 {
  font-size: 1.16rem;
  margin: 0 0 10px;
}

p {
  color: #4c5566;
  line-height: 1.7;
  margin: 0;
}

p + p {
  margin-top: 12px;
}

a {
  color: #345995;
  font-weight: 600;
}

@media (max-width: 640px) {
  .policy-page {
    padding-top: 28px;
  }

  .policy-shell {
    padding: 26px 20px;
  }
}
</style>
