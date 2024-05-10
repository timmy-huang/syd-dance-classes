<template>
  <v-img 
    v-if="studio === 'movement_nation_hurstville'"
    src="/public/movement_nation_hurstville.webp"
  />
  <v-img 
    v-if="studio === 'movement_nation_parramatta'"
    src="/public/movement_nation_parramatta.webp"
  />
  </template>
  
<script lang="ts" setup>
  defineProps({
    studio: String
  })
</script>

<style>
  .v-img {
    width: 100px;
    height: 100px;
  }
</style>