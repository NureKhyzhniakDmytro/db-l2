import { createApp } from 'vue'
import './style.css'
import App from './App.vue'

const app = createApp(App);

app.config.globalProperties.$currency = (value: number) => {
    return new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(value);
};

app.mount('#app')
