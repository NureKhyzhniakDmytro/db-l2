<template>
  <div class="flex justify-center items-center mt-4">
    <button
        :disabled="metadata.offset === 0"
        @click="changePage(metadata.offset - metadata.limit)"
        class="px-3 py-1 mx-1 border border-gray-400 bg-gray-200 disabled:opacity-50"
    >
      Prev
    </button>
    <span class="mx-2">Page {{ currentPage }} of {{ totalPages }}</span>
    <button
        :disabled="metadata.offset + metadata.limit >= metadata.total_items"
        @click="changePage(metadata.offset + metadata.limit)"
        class="px-3 py-1 mx-1 border border-gray-400 bg-gray-200 disabled:opacity-50"
    >
      Next
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
