<template>
  <div class="flex justify-center items-center space-x-2 mt-4">
    <!-- First Button -->
    <button
        :disabled="metadata.offset === 0"
        @click="changePage(0)"
        class="flex items-center px-4 py-2 text-sm font-medium text-gray-600 bg-white border border-gray-300 rounded shadow-sm hover:bg-gray-100 disabled:opacity-50 disabled:cursor-not-allowed"
    >
      First
    </button>

    <!-- Previous Button -->
    <button
        :disabled="metadata.offset === 0"
        @click="changePage(metadata.offset - metadata.limit)"
        class="flex items-center px-4 py-2 text-sm font-medium text-gray-600 bg-white border border-gray-300 rounded shadow-sm hover:bg-gray-100 disabled:opacity-50 disabled:cursor-not-allowed"
    >
      <svg xmlns="http://www.w3.org/2000/svg" class="w-4 h-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
      </svg>
      Prev
    </button>

    <!-- Page Indicator -->
    <span class="text-sm text-gray-700">
      Page <span class="font-semibold">{{ currentPage }}</span> of <span class="font-semibold">{{ totalPages }}</span>
    </span>

    <!-- Next Button -->
    <button
        :disabled="metadata.offset + metadata.limit >= metadata.total_items"
        @click="changePage(metadata.offset + metadata.limit)"
        class="flex items-center px-4 py-2 text-sm font-medium text-gray-600 bg-white border border-gray-300 rounded shadow-sm hover:bg-gray-100 disabled:opacity-50 disabled:cursor-not-allowed"
    >
      Next
      <svg xmlns="http://www.w3.org/2000/svg" class="w-4 h-4 ml-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
      </svg>
    </button>

    <!-- Last Button -->
    <button
        :disabled="metadata.offset + metadata.limit >= metadata.total_items"
        @click="changePage((totalPages - 1) * metadata.limit)"
        class="flex items-center px-4 py-2 text-sm font-medium text-gray-600 bg-white border border-gray-300 rounded shadow-sm hover:bg-gray-100 disabled:opacity-50 disabled:cursor-not-allowed"
    >
      Last
    </button>
  </div>
</template>

<script lang="ts">
import { defineComponent, computed } from 'vue';

export default defineComponent({
  props: {
    metadata: Object as () => {
      total_items: number;
      limit: number;
      offset: number;
    },
  },
  emits: ['page-change'],
  setup(props, { emit }) {
    const totalPages = computed(() => Math.ceil(props.metadata.total_items / props.metadata.limit));
    const currentPage = computed(() => Math.floor(props.metadata.offset / props.metadata.limit) + 1);

    const changePage = (newOffset: number) => {
      emit('page-change', newOffset);
    };

    return { totalPages, currentPage, changePage };
  },
});
</script>
