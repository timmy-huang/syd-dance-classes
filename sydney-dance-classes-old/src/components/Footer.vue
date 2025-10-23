<template>
  <footer class="footer">
    <div class="footer-content">
      <p class="made-by">Made by Timmy Huang</p>
      <a href="mailto:timmyme2@gmail.com" class="email-link">Suggestions or Concerns? Email me at timmyme2@gmail.com</a>
      <!-- <div class="social-links">
        <a href="#" class="social-link" aria-label="GitHub">
          <i class="fab fa-github"></i>
        </a>
        <a href="#" class="social-link" aria-label="LinkedIn">
          <i class="fab fa-linkedin"></i>
        </a>
      </div> -->
    </div>
  </footer>
</template>

<script lang="ts" setup>
</script>

<style scoped>
.footer {
  background-color: #f8f9fa;
  padding: 1.5rem 0;
  margin-top: 2rem;
  border-top: 1px solid #e9ecef;
}

.footer-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}

.made-by {
  margin-bottom: 0.5rem;
  font-weight: 500;
}

.email-link {
  color: #6c757d;
  text-decoration: none;
  margin-bottom: 1rem;
  transition: color 0.2s;
}

.email-link:hover {
  color: #007bff;
}

.social-links {
  display: flex;
  gap: 1rem;
}

.social-link {
  color: #6c757d;
  font-size: 1.25rem;
  transition: color 0.2s;
}

.social-link:hover {
  color: #007bff;
}

@media (min-width: 768px) {
  .footer-content {
    flex-direction: row;
    justify-content: space-between;
  }
  
  .made-by {
    margin-bottom: 0;
  }
  
  .email-link {
    margin-bottom: 0;
  }
}
</style>