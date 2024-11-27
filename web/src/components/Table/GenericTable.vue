<template>
  <div class="w-full p-4">
    <div class="overflow-x-auto">
      <table class="table-auto w-full border-collapse border border-gray-200">
        <thead>
        <tr>
          <th v-for="(header, index) in headers" :key="index" class="border border-gray-300 p-2">
            {{ header }}
          </th>
        </tr>
        </thead>
        <tbody>
        <slot name="row" v-for="(item, index) in data" :key="index" :item="item" />
        </tbody>
      </table>
    </div>
    <Pagination
        :metadata="metadata"
        @page-change="$emit('page-change', $event)"
    />
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import Pagination from './Pagination.vue';

export default defineComponent({
  components: { Pagination },
  props: {
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
