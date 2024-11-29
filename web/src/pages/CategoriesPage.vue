<template>
  <div>
    <GenericTable
        title="Categories"
        :headers="['Name', 'Description', 'Count']"
        :data="tableData"
        :metadata="pagination"
        @page-change="fetchData"
    >
      <template #row="{ item }">
        <tr
            class="bg-white border-b hover:bg-gray-50 transition-all cursor-pointer"
            @click="openCategoryPopup(item)"
        >
          <td class="p-4 text-sm font-medium text-gray-900">{{ item.name }}</td>
          <td class="p-4 text-sm text-gray-700">{{ item.description }}</td>
          <td class="p-4 text-sm font-medium text-right text-gray-800">{{ item.products_count }}</td>
        </tr>
      </template>
    </GenericTable>

    <!-- Popup with Products List -->
    <div
        v-if="showPopup"
        class="fixed inset-0 bg-gray-800 bg-opacity-50 flex items-center justify-center"
        aria-label="Category Products"
    >
      <div class="bg-white p-6 rounded-md shadow-lg w-96">
        <h3 class="text-lg font-semibold mb-4">Products in Category: {{ selectedCategory?.name }}</h3>
        <ul>
          <li v-for="product in categoryProducts" :key="product.id" class="border-b py-2">
            <div class="flex justify-between">
              <span>{{ product.name }}</span>
              <span class="text-sm text-gray-500">{{ $currency(product.unit_price) }}</span>
            </div>
            <div class="text-xs text-gray-500">
              Orders: {{ product.orders_count }} | Stock: {{ product.units_in_stock }}
              <span v-if="product.discontinued" class="text-red-500">Discontinued</span>
            </div>
          </li>
        </ul>
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
    const selectedCategory = ref<any>(null);
    const categoryProducts = ref<any[]>([]);

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

    const openCategoryPopup = async (category: any) => {
      selectedCategory.value = category;
      try {
        const response = await fetch(
            `https://northwind.yooud.org/api/categories/${category.id}/products`
        );
        const { data } = await response.json();
        categoryProducts.value = data;
        showPopup.value = true;
      } catch (error) {
        console.error('Failed to fetch products:', error);
      }
    };

    fetchData(); // Initial fetch

    return { tableData, pagination, fetchData, openCategoryPopup, showPopup, selectedCategory, categoryProducts };
  },
});
</script>
