<template>
  <GenericTable
      :headers="['Order ID', 'Employee', 'Customer', 'Order Date', 'Shipment Details']"
      :data="tableData"
      :metadata="pagination"
      @page-change="fetchData"
  >
    <template #row="{ item }">
      <tr>
        <td class="border border-gray-300 p-2">{{ item.id }}</td>
        <td class="border border-gray-300 p-2">
          {{ item.employee.name }}
        </td>
        <td class="border border-gray-300 p-2">
          {{ item.customer.name }} ({{ item.customer.id }})
        </td>
        <td class="border border-gray-300 p-2">
          {{ formatDate(item.order_date) }}
        </td>
        <td class="border border-gray-300 p-2">
          <strong>Ship Via:</strong> {{ item.shipment.ship_via.name }} <br />
          <strong>Name:</strong> {{ item.shipment.name }} <br />
          <strong>Address:</strong>
          {{ item.shipment.address }}, {{ item.shipment.city }} {{ item.shipment.postal_code }}, {{ item.shipment.country }} <br />
          <strong>Required Date:</strong> {{ formatDate(item.shipment.required_date) }} <br />
          <strong>Shipped Date:</strong> {{ formatDate(item.shipment.shipped_date) }}
        </td>
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

    // Fetch orders from the API
    const fetchData = async (offset = 0) => {
      try {
        const response = await fetch(
            `https://northwind.yooud.org/api/orders?limit=${pagination.value.limit}&offset=${offset}`
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

