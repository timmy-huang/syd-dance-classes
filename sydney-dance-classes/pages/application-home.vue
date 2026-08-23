<template>
  <main class="application-page">
    <section class="application-hero">
      <div class="application-shell">
        <p class="eyebrow">Application support</p>
        <h1>Application Home</h1>
        <p class="intro">
          A simple support page for applications developed by Timmy Huang.
        </p>
        <div class="actions">
          <v-btn
            color="primary"
            variant="flat"
            href="mailto:timmyme2@gmail.com"
            prepend-icon="mdi-email-outline"
          >
            Contact support
          </v-btn>
          <v-btn
            color="primary"
            variant="outlined"
            to="/privacy-policy"
            prepend-icon="mdi-shield-account-outline"
          >
            Privacy policy
          </v-btn>
        </div>
      </div>
    </section>

    <section class="application-shell content-grid" aria-label="Application information">
      <article class="info-card">
        <v-icon icon="mdi-application-outline" size="28" />
        <h2>About These Applications</h2>
        <p>
          These applications are built to provide focused, practical tools for users.
          Each app may have its own features, interface, and data requirements.
        </p>
      </article>

      <article class="info-card">
        <v-icon icon="mdi-lifebuoy" size="28" />
        <h2>Support</h2>
        <p>
          For support, questions, deletion requests, or feedback about any related
          application, email the developer using the contact link on this page.
        </p>
      </article>

      <article class="info-card">
        <v-icon icon="mdi-lock-check-outline" size="28" />
        <h2>Privacy</h2>
        <p>
          Applications should only request information needed to provide their
          features. The generic privacy policy explains the default approach.
        </p>
      </article>
    </section>
  </main>
</template>

<script lang="ts" setup>
useHead({
  title: 'Application Home',
  meta: [
    {
      name: 'description',
      content: 'Generic application home and support page for applications developed by Timmy Huang.',
    },
  ],
})
</script>

<style scoped>
.application-page {
  background: #f7f8fb;
  color: #1d2433;
}

.application-hero {
  background: linear-gradient(135deg, #ffffff 0%, #edf3ff 100%);
  border-bottom: 1px solid #dde3ee;
  padding: 72px 16px 56px;
}

.application-shell {
  max-width: 975px;
  margin: 0 auto;
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
  font-size: clamp(2.2rem, 6vw, 4.6rem);
  line-height: 1;
  margin: 0;
}

.intro {
  color: #4c5566;
  font-size: 1.12rem;
  line-height: 1.65;
  margin: 20px 0 0;
  max-width: 680px;
}

.actions {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  margin-top: 28px;
}

.content-grid {
  display: grid;
  gap: 16px;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  padding: 32px 16px 56px;
}

.info-card {
  background: #ffffff;
  border: 1px solid #dde3ee;
  border-radius: 8px;
  padding: 22px;
}

.info-card h2 {
  font-size: 1.1rem;
  margin: 16px 0 10px;
}

.info-card p {
  color: #566173;
  line-height: 1.6;
  margin: 0;
}

@media (max-width: 760px) {
  .application-hero {
    padding-top: 48px;
  }

  .content-grid {
    grid-template-columns: 1fr;
  }
}
</style>
