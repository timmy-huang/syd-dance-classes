<template>
  <div class="img-container">
    <a :href="`https://www.instagram.com/movementnationdancestudio`" target="_blank" rel="noopener">
      <v-img 
        v-if="studio === 'Movement Nation Hurstville'"
        src="/public/movement_nation_hurstville.webp"
    />
    </a>

    <a :href="`https://www.instagram.com/movementnation.parramatta`" target="_blank" rel="noopener">
      <v-img 
        v-if="studio === 'Movement Nation Parramatta'"
        src="/public/movement_nation_parramatta.webp"
      />
    </a>
    

    <a :href="`https://www.instagram.com/crossoverdance`" target="_blank" rel="noopener">
      <v-img
        v-if="studio === 'Crossover'"
        src="/public/xo.jpg"
      />
    </a>

    <a :href="`https://www.instagram.com/ixdancestudio`" target="_blank" rel="noopener">
      <v-img
        v-if="studio === 'IX'"
        src="/public/ix.png"
      />
    </a>

    <a :href="`https://www.instagram.com/pdc_dance_studio`" target="_blank" rel="noopener">
    <v-img
      v-if="studio === 'PDC'"
        src="/public/pdc.jpg"
      />
    </a>

    <a :href="`https://www.instagram.com/dutistudios`" target="_blank" rel="noopener">
      <v-img
        v-if="studio === 'DUTI'"
        src="/public/duti.png"
      />  
    </a>

    <a :href="`https://www.instagram.com/endlessdancesydney`" target="_blank" rel="noopener">
      <v-img
        v-if="studio === 'Endless'"
        src="/public/endless.jpg"
      />
    </a>

    <div v-if="studio === 'KCC' || studio === 'IMI'" class="pa-2 transparent-container">
      <a :href="`https://www.instagram.com/kcc_studio`" target="_blank" rel="noopener">
        <v-img
          v-if="studio === 'KCC'"
          src="/public/kcc.webp"
        />
      </a>

      <a :href="`https://www.instagram.com/imidance`" target="_blank" rel="noopener">
        <v-img
          v-if="studio === 'IMI'"
          src="/public/imi.png"
        />
      </a>
    </div>
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

  .transparent-container {
    width: 100%;
    height: 100%;
    background-color: black;
  }

@media screen and (max-width: 600px) {
  .img-container {
    height: 50px;
    width: 50px;
  }
  
}
</style>