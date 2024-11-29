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
            <span v-html="icons[index]" class="w-6 h-6 mr-3"></span>
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
      `<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><g id="SVGRepo_bgCarrier" stroke-width="0"></g><g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g><g id="SVGRepo_iconCarrier"> <path d="M5 10H7C9 10 10 9 10 7V5C10 3 9 2 7 2H5C3 2 2 3 2 5V7C2 9 3 10 5 10Z" stroke="#ffffff" stroke-width="1.5" stroke-miterlimit="10" stroke-linecap="round" stroke-linejoin="round"></path> <path d="M17 10H19C21 10 22 9 22 7V5C22 3 21 2 19 2H17C15 2 14 3 14 5V7C14 9 15 10 17 10Z" stroke="#ffffff" stroke-width="1.5" stroke-miterlimit="10" stroke-linecap="round" stroke-linejoin="round"></path> <path d="M17 22H19C21 22 22 21 22 19V17C22 15 21 14 19 14H17C15 14 14 15 14 17V19C14 21 15 22 17 22Z" stroke="#ffffff" stroke-width="1.5" stroke-miterlimit="10" stroke-linecap="round" stroke-linejoin="round"></path> <path d="M5 22H7C9 22 10 21 10 19V17C10 15 9 14 7 14H5C3 14 2 15 2 17V19C2 21 3 22 5 22Z" stroke="#ffffff" stroke-width="1.5" stroke-miterlimit="10" stroke-linecap="round" stroke-linejoin="round"></path> </g></svg>`,
      `<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><g id="SVGRepo_bgCarrier" stroke-width="0"></g><g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g><g id="SVGRepo_iconCarrier"> <rect x="5" y="4" width="14" height="17" rx="2" stroke="#ffffff" stroke-width="2"></rect> <path d="M9 9H15" stroke="#ffffff" stroke-width="2" stroke-linecap="round"></path> <path d="M9 13H15" stroke="#ffffff" stroke-width="2" stroke-linecap="round"></path> <path d="M9 17H13" stroke="#ffffff" stroke-width="2" stroke-linecap="round"></path> </g></svg>`,
      `<svg viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg" stroke-width="5.12" stroke="#ffffff" fill="none"><g id="SVGRepo_bgCarrier" stroke-width="0"></g><g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g><g id="SVGRepo_iconCarrier"><circle cx="32" cy="18.14" r="11.14"></circle><path d="M54.55,56.85A22.55,22.55,0,0,0,32,34.3h0A22.55,22.55,0,0,0,9.45,56.85Z"></path></g></svg>`,
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
