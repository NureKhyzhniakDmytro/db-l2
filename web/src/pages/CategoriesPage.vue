<template>
  <GenericTable
      :headers="['Name', 'Description', 'Count']"
      :data="tableData"
      :metadata="pagination"
      @page-change="fetchData"
  >
    <template #row="{ item }">
      <tr>
        <td class="border border-gray-300 p-2">{{ item.name }}</td>
        <td class="border border-gray-300 p-2">{{ item.description }}</td>
        <td class="border border-gray-300 p-2">{{ item.products_count }}</td>
      </tr>
    </template>
  </GenericTable>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';
import GenericTable from '../components/Table/GenericTable.vue';

export default defineComponent({
  components: { GenericTable },
  setup() {
    const tableData = ref<any[]>([]);
    const pagination = ref({
      total_items: 0,
      limit: 10,
      offset: 0,
    });

    const fetchData = async (offset = 0) => {
      try {
        const response = await fetch(
            `https://northwind.yooud.org/api/categories?limit=${pagination.value.limit}&offset=${offset}`
        );
        const { data, metadata } = await response.json();
        tableData.value = data;
        pagination.value = { ...pagination.value, ...metadata };
      } catch (error) {
        console.error('Failed to fetch data:', error);
      }
    };

    fetchData(); // Initial fetch

    return { tableData, pagination, fetchData };
  },
});
</script>
