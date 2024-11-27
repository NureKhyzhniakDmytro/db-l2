<template>
  <div class="flex h-screen">
    <!-- Sidebar -->
    <transition name="slide">
      <div v-if="isPanelOpen" class="w-64 relative h-full bg-white shadow-md p-4">
        <h2 class="text-lg font-semibold mb-4">NORTHWIND</h2>
        <ul class="space-y-2">
          <li
              v-for="(table, index) in tables"
              :key="index"
              class="p-2 border rounded hover:bg-gray-100 cursor-pointer"
              @click="selectTable(index)">
            {{ table }}
          </li>
        </ul>
        <button
            @click="togglePanel"
            class="absolute top-4 right-4 bg-transparent text-gray-500 hover:text-gray-700">
          <svg aria-hidden="true" focusable="false" viewBox="0 0 16 16" width="16" height="16" fill="currentColor">
            <path d="m4.177 7.823 2.396-2.396A.25.25 0 0 1 7 5.604v4.792a.25.25 0 0 1-.427.177L4.177 8.177a.25.25 0 0 1 0-.354Z"/>
            <path d="M0 1.75C0 .784.784 0 1.75 0h12.5C15.216 0 16 .784 16 1.75v12.5A1.75 1.75 0 0 1 14.25 16H1.75A1.75 1.75 0 0 1 0 14.25Zm1.75-.25a.25.25 0 0 0-.25.25v12.5c0 .138.112.25.25.25H9.5v-13Zm12.5 13a.25.25 0 0 0 .25-.25V1.75a.25.25 0 0 0-.25-.25H11v13Z"/>
          </svg>
        </button>
      </div>
    </transition>

    <!-- Main content -->
    <div class="flex-1 bg-gray-50 p-6 overflow-y-auto">
      <button @click="togglePanel" v-if="!isPanelOpen" class="fixed top-4 left-4 bg-transparent text-gray-500 hover:text-gray-700">
        <svg aria-hidden="true" focusable="false" viewBox="0 0 16 16" width="16" height="16" fill="currentColor">
          <path d="M6.823 7.823a.25.25 0 0 1 0 .354l-2.396 2.396A.25.25 0 0 1 4 10.396V5.604a.25.25 0 0 1 .427-.177Z"/>
          <path d="M1.75 0h12.5C15.216 0 16 .784 16 1.75v12.5A1.75 1.75 0 0 1 14.25 16H1.75A1.75 1.75 0 0 1 0 14.25V1.75C0 .784.784 0 1.75 0ZM1.5 1.75v12.5c0 .138.112.25.25.25H9.5v-13H1.75a.25.25 0 0 0-.25.25ZM11 14.5h3.25a.25.25 0 0 0 .25-.25V1.75a.25.25 0 0 0-.25-.25H11Z"/>
        </svg>
      </button>
      <component :is="currentComponent" v-if="selectedTable !== null" />
    </div>
  </div>
</template>

<script lang="ts">
import {defineComponent, onMounted, ref} from 'vue';
import CategoriesPage from "./CategoriesPage.vue";
import OrdersPage from "./OrdersPage.vue";
import EmployeesPage from "./EmployeesPage.vue";

export default defineComponent({
  name: 'BackPanelPage',
  components: {
    CategoriesPage,
    OrdersPage,
    EmployeesPage
  },
  setup() {
    const isPanelOpen = ref(true);
    const tables = ref(['Categories', 'Orders', 'Employees']);
    const selectedTable = ref<number | null>(null);
    const currentComponent = ref<string>('');

    const togglePanel = () => {
      isPanelOpen.value = !isPanelOpen.value;
    };

    const selectTable = (index: number) => {
      selectedTable.value = index;
      switch (index) {
        case 0:
          currentComponent.value = 'CategoriesPage';
          break;
        case 1:
          currentComponent.value = 'OrdersPage';
          break;
        case 2:
          currentComponent.value = 'EmployeesPage';
          break;
        default:
          currentComponent.value = '';
      }
    };

    onMounted(() => {
      selectTable(0);
    });

    return {
      isPanelOpen,
      tables,
      selectedTable,
      currentComponent,
      togglePanel,
      selectTable,
    };
  },
});
</script>

<style scoped>
.slide-enter-active, .slide-leave-active {
  transition: transform 0.3s ease;
}
.slide-enter-from {
  transform: translateX(-100%);
}
.slide-leave-to {
  transform: translateX(-100%);
}
</style>
