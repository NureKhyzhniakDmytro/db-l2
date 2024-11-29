<template>
  <div class="flex h-screen">
    <!-- Sidebar -->
    <transition name="slide">
      <div
          v-if="isPanelOpen"
          class="w-64 h-full bg-gradient-to-b from-blue-800 via-blue-700 to-blue-600 text-white shadow-lg p-6 relative"
      >
        <h2 class="text-2xl font-bold mb-6 tracking-wide">NORTHWIND</h2>
        <ul class="space-y-4">
          <li
              v-for="(table, index) in tables"
              :key="index"
              class="flex items-center p-3 rounded-lg cursor-pointer transition-all duration-200"
              :class="selectedTable === index ? 'bg-blue-500 shadow-lg' : 'hover:bg-blue-700'"
              @click="selectTable(index)"
          >
            <img
                :src="icons[index]"
                alt="icon"
                class="w-6 h-6 mr-3"
                loading="lazy"
            />
            <span class="text-sm font-medium">{{ table }}</span>
          </li>
        </ul>
        <button
            @click="togglePanel"
            class="absolute top-4 right-4 text-blue-200 hover:text-white focus:outline-none"
        >
          <svg
              xmlns="http://www.w3.org/2000/svg"
              class="h-5 w-5"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
          >
            <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M6 18L18 6M6 6l12 12"
            />
          </svg>
        </button>
      </div>
    </transition>

    <!-- Main content -->
    <div class="flex-1 bg-gray-50 p-6 overflow-y-auto">
      <button
          v-if="!isPanelOpen"
          @click="togglePanel"
          class="fixed top-4 left-4 text-gray-400 hover:text-blue-700 focus:outline-none"
      >
        <svg
            xmlns="http://www.w3.org/2000/svg"
            class="h-6 w-6"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
        >
          <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M3 12h18M3 6h18M3 18h18"
          />
        </svg>
      </button>
      <component :is="currentComponent" v-if="selectedTable !== null" />
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, onMounted, ref } from "vue";
import CategoriesPage from "./CategoriesPage.vue";
import OrdersPage from "./OrdersPage.vue";
import EmployeesPage from "./EmployeesPage.vue";

export default defineComponent({
  name: "BackPanelPage",
  components: {
    CategoriesPage,
    OrdersPage,
    EmployeesPage,
  },
  setup() {
    const isPanelOpen = ref(true);
    const tables = ref(["Categories", "Orders", "Employees"]);
    const icons = ref([
      "https://www.svgrepo.com/show/496936/category.svg", // Categories icon
      "https://www.svgrepo.com/show/458826/order.svg",    // Orders icon
      "https://www.svgrepo.com/show/447734/person-male.svg", // Employees icon
    ]);
    const selectedTable = ref<number | null>(null);
    const currentComponent = ref<string>("");

    const togglePanel = () => {
      isPanelOpen.value = !isPanelOpen.value;
    };

    const selectTable = (index: number) => {
      selectedTable.value = index;
      switch (index) {
        case 0:
          currentComponent.value = "CategoriesPage";
          break;
        case 1:
          currentComponent.value = "OrdersPage";
          break;
        case 2:
          currentComponent.value = "EmployeesPage";
          break;
        default:
          currentComponent.value = "";
      }
    };

    onMounted(() => {
      selectTable(0);
    });

    return {
      isPanelOpen,
      tables,
      icons,
      selectedTable,
      currentComponent,
      togglePanel,
      selectTable,
    };
  },
});
</script>

<style scoped>
.slide-enter-active,
.slide-leave-active {
  transition: transform 0.3s ease;
}
.slide-enter-from {
  transform: translateX(-100%);
}
.slide-leave-to {
  transform: translateX(-100%);
}
</style>
