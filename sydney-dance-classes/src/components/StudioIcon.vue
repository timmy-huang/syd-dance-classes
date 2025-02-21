<template>
  <div class="img-container">
    <v-img 
      v-if="studio === 'Movement Nation Hurstville'"
      src="/public/movement_nation_hurstville.webp"
    />
    <v-img 
      v-if="studio === 'Movement Nation Parramatta'"
      src="/public/movement_nation_parramatta.webp"
    />
    <v-img
      v-if="studio === 'IMI'"
      class="imi pa-2"
      src="/public/imi.png"
    />
    <v-img
      v-if="studio === 'Crossover'"
      src="/public/xo.jpg"
    />
    <v-img
      v-if="studio === 'IX'"
      src="/public/ix.png"
    />
    <v-img
      v-if="studio === 'PDC'"
      src="/public/pdc.jpg"
    />
  </div>
</template>
  
<script lang="ts" setup>
  defineProps({
    studio: String,
    mobile: {
      type: Boolean,
      default: false
    }        
  })
</script>

<style>
  .img-container {
    height: 100px;
    width: 100px;
  }

  .v-img {
    width: 100%;
    height: 100%;
    flex-grow: 0;
  }

  .imi {
    background-color: black;
  }

@media screen and (max-width: 600px) {
  .img-container {
    height: 50px;
    width: 50px;
  }
  
}
</style>