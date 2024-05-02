<template>
  <v-card>
    <template v-slot:title>
      {{ title }}
    </template>

    <template v-slot:subtitle>
      {{ subtitle }}
    </template>

    <template v-slot:text>
      {{ text }}
    </template>
    </v-card>
</template>
  
<script lang="ts" setup>
  defineProps(['title', 'subtitle', 'text'])
</script>