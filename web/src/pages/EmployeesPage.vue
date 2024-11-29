<template>
  <div>
    <GenericTable
        title="Employees"
        :headers="['Employee ID', 'Name', 'Title', 'Birth Date', 'Hire Date', 'Address', 'Reports To', 'Total Sales']"
        :data="tableData"
        :metadata="pagination"
        @page-change="fetchData"
    >
      <template #actions>
        <button
            class="flex items-center bg-red-600 text-white py-2 px-4 rounded-md shadow hover:bg-red-700"
            @click="showPopup = true"
        >
          <span class="mr-2">Delete Employees</span>
        </button>
      </template>
      <template #row="{ item }">
        <tr class="bg-white border-b hover:bg-gray-50">
          <td class="p-2 font-medium text-gray-900">{{ item.id }}</td>
          <td class="flex items-center space-x-4 p-2">
            <div>
              <div class="font-medium">{{ item.name }}</div>
              <div class="text-sm text-gray-500">{{ item.title }}</div>
            </div>
          </td>
          <td class="p-2 text-gray-500">{{ item.title }}</td>
          <td class="p-2">{{ formatDate(item.birth_date) }}</td>
          <td class="p-2">{{ formatDate(item.hire_date) }}</td>
          <td class="p-2 text-sm text-gray-500">
            {{ item.address }}, {{ item.city }}, {{ item.postal_code }}, {{ item.country }}
          </td>
          <td class="p-2">
            {{ item.reports_to.name ? `${item.reports_to.name} (ID: ${item.reports_to.id})` : 'N/A' }}
          </td>
          <td class="p-2 text-right">
            <div class="text-gray-900 font-medium">${{ item.total_sales.toFixed(2) }}</div>
          </td>
        </tr>
      </template>
    </GenericTable>

    <!-- Popup Window -->
    <div
        v-if="showPopup"
        class="fixed inset-0 bg-gray-800 bg-opacity-50 flex items-center justify-center"
        aria-label="Delete employees confirmation"
    >
      <div class="bg-white p-6 rounded-md shadow-lg w-96">
        <h3 class="text-lg font-semibold mb-4">Delete Employees</h3>
        <label for="threshold" class="block text-gray-600 mb-2">Sales Threshold:</label>
        <input
            v-model.number="threshold"
            type="number"
            id="threshold"
            class="w-full p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
        <div class="flex justify-end mt-4">
          <button
              class="px-4 py-2 bg-gray-300 text-gray-700 rounded-md mr-2 hover:bg-gray-400"
              @click="showPopup = false"
          >
            Cancel
          </button>
          <button
              class="px-4 py-2 bg-red-600 text-white rounded-md hover:bg-red-700"
              @click="deleteEmployees"
          >
            Confirm
          </button>
        </div>
      </div>
    </div>

    <!-- Notification -->
    <transition name="fade">
      <div
          v-if="notification.visible"
          class="fixed top-4 right-4 bg-green-600 text-white p-4 rounded-md shadow-lg"
          v-bind:class="notification.type === 'error' ? 'bg-red-600' : 'bg-green-600'"
      >
        <span>{{ notification.message }}</span>
      </div>
    </transition>
  </div>
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

    const showPopup = ref(false);
    const threshold = ref<number | null>(null);

    const notification = ref({
      visible: false,
      message: '',
      type: 'success' as 'success' | 'error',
    });

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

    const deleteEmployees = async () => {
      if (threshold.value === null) return;
      try {
        const response = await fetch(
            `https://northwind.yooud.org/api/employees?threshold=${threshold.value}`,
            {
              method: 'DELETE',
              headers: {
                'Content-Type': 'application/json',
              },
            }
        );
        const result = await response.json();
        if (response.ok && result.status) {
          notification.value = {
            visible: true,
            message: 'Employees deleted successfully!',
            type: 'success',
          };
          // Hide notification after 3 seconds
          setTimeout(() => {
            notification.value.visible = false;
          }, 3000);
          await fetchData(); // Refresh data after deletion
        } else {
          notification.value = {
            visible: true,
            message: 'Failed to delete employees.',
            type: 'error',
          };
          // Hide notification after 3 seconds
          setTimeout(() => {
            notification.value.visible = false;
          }, 3000);
        }
      } catch (error) {
        console.error('Error during deletion:', error);
        notification.value = {
          visible: true,
          message: 'An error occurred while deleting employees.',
          type: 'error',
        };
        // Hide notification after 3 seconds
        setTimeout(() => {
          notification.value.visible = false;
        }, 3000);
      } finally {
        showPopup.value = false;
        threshold.value = null;
      }
    };

    fetchData();

    return {
      tableData,
      pagination,
      fetchData,
      formatDate,
      showPopup,
      threshold,
      deleteEmployees,
      notification,
    };
  },
});
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s ease;
}
.fade-enter, .fade-leave-to {
  opacity: 0;
}
</style>
