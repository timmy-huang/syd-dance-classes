<template>
  <div style="display: flex; justify-content: center; flex-direction: column; align-items: center; background-color: #f5f5f5; width: 100%" class="pt-5 px-5">
    <v-text-field 
      variant="solo"
      label="Search..."
      style="width: 100%"
      :model-value="search"
      @input="$emit('update:search', $event)"
    />
    <div class="justify-space-between d-flex align-center" style="width: 100%">
      <div class="d-flex">
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
      </div>
      <!-- <div class="d-flex ">
        <v-select
          variant="underlined"
          density="comfortable"
          v-model="favorites"
          :items="cleanedStudios"
          label="Studios"
          multiple
          persistent-hint
          style="min-width: 150px"
        >
          <template v-slot:prepend-item>
            <v-list-item
              title="Select All"
              @click="toggle"
            >
              <template v-slot:prepend>
                <v-checkbox-btn
                  :indeterminate="likesSomeFruit && !likesAllFruit"
                  :model-value="likesAllFruit"
                ></v-checkbox-btn>
              </template>
            </v-list-item>

            <v-divider class="mt-2"></v-divider>
          </template>
        </v-select> -->
      <!-- </div> -->
    </div>
  </div>
</template>

<script lang="ts" setup>
  import { studios } from '../utils/consts'

  const cleanedStudios = studios.map((studio) => {
    if (studio == "imi") {
      return "IMI"
    }
    return studio.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())
  })

  const props = defineProps({
    beg: Boolean,
    inte: Boolean,
    adv: Boolean,
    search: String
  });
</script>