<template>
  <v-select
    variant="underlined"
    density="comfortable"
    :model-value="value"
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
  import { computed } from 'vue';
  import { studios, styles } from '../utils/consts';

  const emit = defineEmits(["update"]);

  const props = defineProps({
    value: Array,
    type: String
  });

  const items = computed(() => {
    if (props.type === 'Studios') {
      return studios;
    } else {
      return styles;
    }
  });

  const allSelected = computed(() => {
    return props.value.length === items.value.length;
  });

  const someSelected = computed(() => {
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