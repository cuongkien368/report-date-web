<script setup lang="ts">
import { ref } from "vue";
import { Chart as ChartJS, Title, Tooltip, Legend, LineElement, CategoryScale, LinearScale, PointElement } from "chart.js";
import { Line } from "vue-chartjs";

// đăng ký chart.js
ChartJS.register(Title, Tooltip, Legend, LineElement, CategoryScale, LinearScale, PointElement);

const selectedDate = ref<string>("");
const data = ref<number[]>([12, 19, 3, 5, 2, 3]);

const chartData = ref({
  labels: ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
  datasets: [
    {
      label: "Demo Data",
      backgroundColor: "#42b883",
      borderColor: "#42b883",
      data: data.value,
    },
  ],
});

const chartOptions = ref({
  responsive: true,
  maintainAspectRatio: false,
});
</script>

<template>
  <div style="padding:20px; max-width:600px; margin:auto">
    <h2>Demo nhập ngày + hiển thị data + biểu đồ</h2>

    <label>Chọn ngày: </label>
    <input type="date" v-model="selectedDate" />

    <p>Bạn chọn ngày: <b>{{ selectedDate }}</b></p>

    <div style="height:300px;">
      <Line :data="chartData" :options="chartOptions" />
    </div>
  </div>
</template>

<style>
body {
  font-family: sans-serif;
}
</style>
