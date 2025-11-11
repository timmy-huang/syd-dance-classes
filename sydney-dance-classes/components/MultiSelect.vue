<template>
  <v-select
    variant="underlined"
    density="comfortable"
    :model-value="value || []"
    @update:model-value="$emit('update', $event)"
    :items="items"
    :label="type"
    multiple
    persistent-hint
    class="ml-2 select"
  >
    <template v-slot:selection="{ item, index }">
      <span
        v-if="allSelected && index === 0"
        class="d-inline-block"
      >
        All {{ type }}
      </span>
      <span
        v-if="!allSelected && index === 0"
        class="d-inline-block"
      >
        Selected {{ type }}
      </span>
    </template>
    <template v-slot:prepend-item>
      <v-list-item
        title="Select All"
        @click="toggle"
      >
        <template v-slot:prepend>
          <v-checkbox-btn
            :indeterminate="someSelected && !allSelected"
            :model-value="allSelected"
          ></v-checkbox-btn>
        </template>
      </v-list-item>

      <v-divider class="mt-2"></v-divider>
    </template>
  </v-select>
</template>

<script lang="ts" setup>
  import { computed, onMounted, watch } from 'vue';
  import { styles } from '../utils/consts';
  const { studios, fetchStudios } = useStudios();

  const emit = defineEmits(["update"]);

  const props = defineProps<{
    value?: string[];
    type: string;
  }>();

  // Track if we've initialized studios to avoid re-initializing
  let studiosInitialized = false;

  // Fetch studios on mount
  onMounted(async () => {
    if (props.type === 'Studios') {
      // After fetching studios, set the value to the studios
      await fetchStudios();
    }
  });

  const items = computed(() => {
    if (props.type === 'Studios') {
      return studios.value;
    } else {
      return styles;
    }
  });

  // Watch for when studios are loaded and initialize selection
  watch(items, (newItems) => {
    if (props.type === 'Studios' && newItems.length > 0 && !studiosInitialized) {
      studiosInitialized = true;
      
      // Check localStorage for saved selection
      const savedStudios = localStorage.getItem('selectedStudios');
      
      if (savedStudios) {
        try {
          const parsedStudios = JSON.parse(savedStudios);
          // Validate that saved studios are still in the current list
          const validStudios = parsedStudios.filter((studio: string) => newItems.includes(studio));
          if (validStudios.length > 0) {
            emit('update', validStudios);
            return;
          }
        } catch (e) {
          console.error('Error parsing saved studios from localStorage:', e);
        }
      }
      
      // If no valid saved selection, select all studios
      emit('update', [...newItems]);
    }
  }, { immediate: true });

  const allSelected = computed(() => {
    if (!props.value || props.value.length === 0) return false;
    return props.value.length === items.value.length;
  });

  const someSelected = computed(() => {
    if (!props.value) return false;
    return props.value.length > 0 && props.value.length < items.value.length;
  });

  const toggle = () => {
    if (allSelected.value) {
      emit('update', []);
    } else {
      emit('update', items.value);
    }
  };
</script>

<style>
  .select {
    width: 200px;
  }

  @media screen and (max-width: 600px) {
    .select {
      width: 150px;
    }
  }
</style>