<template>
  <div class="w-full p-4">
    <div class="flex justify-between items-center mb-4">
      <h1 class="text-2xl font-bold text-gray-800">{{ title }}</h1>
      <!-- Slot for custom buttons -->
      <div>
        <slot name="actions"></slot>
      </div>
    </div>
    <div class="overflow-x-auto shadow border border-gray-200 rounded-lg">
      <table class="table-auto w-full border-collapse">
        <thead class="bg-gray-100 text-gray-600 uppercase text-sm">
        <tr>
          <th
              v-for="(header, index) in headers"
              :key="index"
              class="p-4 text-left border-b border-gray-300"
          >
            {{ header }}
          </th>
        </tr>
        </thead>
        <tbody>
        <slot name="row" v-for="(item, index) in data" :key="index" :item="item" />
        </tbody>
      </table>
    </div>
    <Pagination :metadata="metadata" @page-change="$emit('page-change', $event)" />
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import Pagination from './Pagination.vue';

export default defineComponent({
  components: { Pagination },
  props: {
    title: String,
    headers: Array as () => string[],
    data: Array as () => any[],
    metadata: Object as () => {
      total_items: number;
      limit: number;
      offset: number;
    },
  },
  emits: ['page-change'],
});
</script>
