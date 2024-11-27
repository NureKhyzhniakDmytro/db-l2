<template>
  <GenericTable
      :headers="['Employee ID', 'Name', 'Title', 'Birth Date', 'Hire Date', 'Address', 'Reports To', 'Total Sales']"
      :data="tableData"
      :metadata="pagination"
      @page-change="fetchData"
  >
    <template #row="{ item }">
      <tr>
        <td class="border border-gray-300 p-2">{{ item.id }}</td>
        <td class="border border-gray-300 p-2">{{ item.name }}</td>
        <td class="border border-gray-300 p-2">{{ item.title }}</td>
        <td class="border border-gray-300 p-2">{{ formatDate(item.birth_date) }}</td>
        <td class="border border-gray-300 p-2">{{ formatDate(item.hire_date) }}</td>
        <td class="border border-gray-300 p-2">
          {{ item.address }}, {{ item.city }}, {{ item.postal_code }}, {{ item.country }}
        </td>
        <td class="border border-gray-300 p-2">
          {{ item.reports_to ? `${item.reports_to.name} (ID: ${item.reports_to.id})` : 'N/A' }}
        </td>
        <td class="border border-gray-300 p-2">${{ item.total_sales.toFixed(2) }}</td>
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

    // Helper function for formatting dates
    const formatDate = (dateStr: string | null) => {
      if (!dateStr) return 'N/A';
      const options: Intl.DateTimeFormatOptions = {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
      };
      return new Date(dateStr).toLocaleDateString(undefined, options);
    };

    // Fetch employees from the API
    const fetchData = async (offset = 0) => {
      try {
        const response = await fetch(
            `https://northwind.yooud.org/api/employees?limit=${pagination.value.limit}&offset=${offset}`
        );
        const { data, metadata } = await response.json();
        tableData.value = data;
        pagination.value = metadata;
      } catch (error) {
        console.error('Failed to fetch data:', error);
      }
    };

    fetchData(); // Initial fetch

    return { tableData, pagination, fetchData, formatDate };
  },
});
</script>
