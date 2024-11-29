<template>
  <div>
    <!-- Orders Table -->
    <GenericTable
        title="Orders"
        :headers="['Order ID', 'Employee', 'Customer', 'Order Date']"
        :data="tableData"
        :metadata="pagination"
        @page-change="fetchData"
    >
      <template #row="{ item }">
        <tr
            class="bg-white border-b hover:bg-gray-50 transition-all cursor-pointer"
            @click="openOrderPopup(item)"
        >
          <td class="p-4 text-sm font-medium text-gray-900">{{ item.id }}</td>
          <td class="p-4 text-sm text-gray-700">{{ item.employee.name }}</td>
          <td class="p-4 text-sm text-gray-700">{{ item.customer.name }} ({{ item.customer.id }})</td>
          <td class="p-4 text-sm text-gray-700">{{ formatDate(item.order_date) }}</td>
        </tr>
      </template>
    </GenericTable>

    <!-- Order Details Popup -->
    <div
        v-if="showPopup"
        class="fixed inset-0 bg-gray-800 bg-opacity-50 flex items-center justify-center"
        aria-label="Order Details"
    >
      <div class="bg-white p-6 rounded-md shadow-lg w-96 overflow-y-auto">
        <h3 class="text-lg font-semibold mb-4">Order Details - #{{ selectedOrder?.id }}</h3>

        <div v-if="selectedOrder?.shipment">
          <h4 class="font-medium">Shipment Details</h4>
          <p><strong>Name:</strong> {{ selectedOrder?.shipment.name }}</p>
          <p><strong>Ship Via:</strong> {{ selectedOrder?.shipment.ship_via.name }}</p>
          <p><strong>Address:</strong> {{ selectedOrder?.shipment.address }}, {{ selectedOrder?.shipment.city }} {{ selectedOrder?.shipment.postal_code }}, {{ selectedOrder?.shipment.country }}</p>
          <p><strong>Required Date:</strong> {{ formatDate(selectedOrder?.shipment.required_date) }}</p>
          <p><strong>Shipped Date:</strong> {{ formatDate(selectedOrder?.shipment.shipped_date) }}</p>
        </div>

        <div v-if="orderProducts.length > 0" class="mt-4">
          <h4 class="font-medium">Products</h4>
          <ul>
            <li v-for="product in orderProducts" :key="product.id" class="border-b py-2">
              <div class="flex justify-between">
                <span>{{ product.name }}</span>
                <span class="text-sm text-gray-500"><strong>{{ $currency(product.total_price) }}</strong></span>
              </div>
              <div class="text-xs text-gray-500">
                Quantity: {{ product.quantity }} | Discount: {{ parseFloat(product.discount).toFixed(2) }}%
              </div>
              <div class="text-xs text-gray-500">
                Unit Price {{ $currency(product.unit_price) }}
              </div>
            </li>
          </ul>
        </div>

        <div class="mt-4">
          <h4 class="font-medium">Order Total Price</h4>
          <p>{{ $currency(selectedOrder?.total_price) }}</p>
        </div>

        <div class="flex justify-end mt-4">
          <button
              class="px-4 py-2 bg-gray-300 text-gray-700 rounded-md mr-2 hover:bg-gray-400"
              @click="showPopup = false"
          >
            Close
          </button>
        </div>
      </div>
    </div>
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
    const selectedOrder = ref<any>(null);
    const orderProducts = ref<any[]>([]);

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

    // Fetch products for a specific order
    const fetchOrderProducts = async (orderId: number) => {
      try {
        const response = await fetch(
            `https://northwind.yooud.org/api/orders/${orderId}/products`
        );
        const { data } = await response.json();
        orderProducts.value = data;
      } catch (error) {
        console.error('Failed to fetch products:', error);
      }
    };

    // Fetch order total price
    const fetchOrderTotalPrice = async (orderId: number) => {
      try {
        const response = await fetch(
            `https://northwind.yooud.org/api/orders/${orderId}/price`
        );
        const { result } = await response.json();
        selectedOrder.value.total_price = result;
      } catch (error) {
        console.error('Failed to fetch total price:', error);
      }
    };

    // Open the order details popup
    const openOrderPopup = async (order: any) => {
      selectedOrder.value = order;
      await fetchOrderProducts(order.id);
      await fetchOrderTotalPrice(order.id);
      showPopup.value = true;
    };

    fetchData(); // Initial fetch

    return { tableData, pagination, fetchData, showPopup, selectedOrder, orderProducts, formatDate, openOrderPopup };
  },
});
</script>
