<template>
  <div style="display: flex; justify-content: center; flex-direction: column; align-items: center; background-color: #f5f5f5; width: 100%" class="pt-5 px-5">
    <v-text-field 
      variant="solo"
      label="Search..."
      style="width: 100%"
      :model-value="search"
      @input="$emit('update:search', $event)"
    />
    <div class="justify-space-between d-flex align-center filter-options" style="width: 100%">
      <div class="justify-space-between d-flex align-center filter-options" style="width: 100%">
        <div class="d-flex flex-wrap">
          <v-checkbox
            label="Youth"
            density="comfortable"
            :model-value="youth"
            :onchange="() => $emit('update:youth')"
          />
          <v-checkbox
            label="Beginner"
            density="comfortable"
            :model-value="beg"
            :onchange="() => $emit('update:beg')"
          />
          <v-checkbox
            label="Intermediate"
            density="comfortable"
            :model-value="inte"
            :onchange="() => $emit('update:inte')"
          />
          <v-checkbox
            label="Advanced"
            density="comfortable"
            :model-value="adv"
            :onchange="() => $emit('update:adv')"
          />
          <v-checkbox
            label="Pop Up"
            density="comfortable"
            :model-value="popUp"
            :onchange="() => $emit('update:popUp')"
          />
        </div>
      </div>
      <div class="d-flex px-1">
        <MultiSelect :value="selectedStyles" @update="($event) => $emit('update:selectedStyles', $event)" type="Styles" />
        <MultiSelect :value="selectedStudios" @update="($event) => $emit('update:selectedStudios', $event)" type="Studios" />
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
  import { computed } from 'vue';
  import { studios } from '../utils/consts';
  import MultiSelect from './MultiSelect.vue';

  const emit = defineEmits(["update:selectedStudios", "update:selectedStyles", "update:adv", "update:inte", "update:beg", "update:search", "update:youth", "update:popUp"]);

  const props = defineProps({
    youth: Boolean,
    beg: Boolean,
    inte: Boolean,
    adv: Boolean,
    popUp: Boolean,
    search: String,
    selectedStudios: Array,
    selectedStyles: Array
  });

</script>

<style>
@media screen and (max-width: 600px) {
  .filter-options {
    flex-direction: column;
  }
  
}
</style>