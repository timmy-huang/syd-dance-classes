<script lang="ts" setup>
// Redirect root path to /classes
onMounted(() => {
  navigateTo('/classes', { redirectCode: 301, replace: true })
})
</script>