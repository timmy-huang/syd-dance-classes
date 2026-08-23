<template>
  <main class="terms-page">
    <article class="terms-shell">
      <p class="eyebrow">Generic application terms</p>
      <h1>Terms of Service</h1>
      <p class="updated">Effective date: 23 August 2026</p>

      <section>
        <h2>Overview</h2>
        <p>
          These terms of service are general terms for applications developed by
          Timmy Huang. By accessing or using one of these applications, users agree
          to use the application responsibly and in accordance with these terms.
        </p>
      </section>

      <section>
        <h2>Use of Applications</h2>
        <p>
          Applications are provided for lawful, personal, professional, or internal
          use as applicable to each app. Users must not misuse the applications,
          interfere with their operation, attempt unauthorized access, or use them
          in a way that harms others.
        </p>
      </section>

      <section>
        <h2>Accounts and Access</h2>
        <p>
          Some applications may require an account, sign-in, or third-party
          authorization. Users are responsible for maintaining the security of their
          accounts and for activity that occurs through their access.
        </p>
      </section>

      <section>
        <h2>User Content</h2>
        <p>
          Users are responsible for any content, data, or information they submit to
          an application. Users should only submit content they have the right to
          provide and should avoid submitting unlawful, harmful, or infringing
          material.
        </p>
      </section>

      <section>
        <h2>Third-Party Services</h2>
        <p>
          Applications may connect to third-party services for hosting,
          authentication, analytics, storage, payments, communications, or other
          features. Use of those services may be subject to separate terms and
          policies from those providers.
        </p>
      </section>

      <section>
        <h2>Availability and Changes</h2>
        <p>
          Applications may be updated, changed, suspended, or discontinued at any
          time. While reasonable care is taken to keep applications working, no
          guarantee is made that they will always be available, secure, or error
          free.
        </p>
      </section>

      <section>
        <h2>Disclaimers</h2>
        <p>
          Applications are provided on an "as is" and "as available" basis. To the
          fullest extent permitted by law, warranties of merchantability, fitness
          for a particular purpose, and non-infringement are disclaimed.
        </p>
      </section>

      <section>
        <h2>Limitation of Liability</h2>
        <p>
          To the fullest extent permitted by law, the developer is not liable for
          indirect, incidental, consequential, special, exemplary, or punitive
          damages, or for loss of data, profits, revenue, or business arising from
          use of the applications.
        </p>
      </section>

      <section>
        <h2>Termination</h2>
        <p>
          Access to an application may be suspended or terminated if a user violates
          these terms, misuses the application, creates security or legal risk, or
          if continued operation is no longer practical.
        </p>
      </section>

      <section>
        <h2>Privacy</h2>
        <p>
          Use of the applications may involve processing information as described in
          the <NuxtLink to="/privacy-policy">privacy policy</NuxtLink>.
        </p>
      </section>

      <section>
        <h2>Contact</h2>
        <p>
          For questions about these terms or any related application, email
          <a href="mailto:timmyme2@gmail.com">timmyme2@gmail.com</a>.
        </p>
      </section>
    </article>
  </main>
</template>

<script lang="ts" setup>
useHead({
  title: 'Terms of Service',
  meta: [
    {
      name: 'description',
      content: 'Generic terms of service for applications developed by Timmy Huang.',
    },
  ],
})
</script>

<style scoped>
.terms-page {
  background: #f7f8fb;
  color: #1d2433;
  padding: 48px 16px 64px;
}

.terms-shell {
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

a {
  color: #345995;
  font-weight: 600;
}

@media (max-width: 640px) {
  .terms-page {
    padding-top: 28px;
  }

  .terms-shell {
    padding: 26px 20px;
  }
}
</style>
