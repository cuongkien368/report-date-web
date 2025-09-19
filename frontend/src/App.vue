<script setup>
import { ref, onMounted } from 'vue'
import { Chart, registerables } from 'chart.js'
import axios from 'axios'

Chart.register(...registerables)

const chartCanvas = ref(null)
let chartInstance = null

// Link CSV public từ Google Sheet (replace bằng link CSV của bạn)
const url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSM_MhYnKMXjTHY3SOxV5sr68z1WyLNxjs7-E13gOV7Fiiu2yjdXNp7TGTTLRDG0a58CFJnIIh-zJo4/pub?output=csv"

async function fetchAndRenderChart() {
  try {
    const res = await axios.get(url)

    // Parse CSV
    const rows = res.data
      .trim()
      .split('\n')
      .map(r => r.split(',').map(c => c.trim()))

    const labels = rows.slice(1).map(r => r[0])
    const values = rows.slice(1).map(r => Number(r[1]) || 0)

    console.log('labels:', labels)
    console.log('values:', values)

    if (chartInstance) chartInstance.destroy()

    chartInstance = new Chart(chartCanvas.value, {
      type: 'line',
      data: {
        labels,
        datasets: [{
          label: 'Số lượt mua mỗi ngày',
          data: values,
          borderColor: 'blue',
          backgroundColor: 'rgba(0,0,255,0.1)',
          tension: 0.3,
          fill: true
        }]
      },
      options: {
        responsive: true,
        scales: {
          x: { title: { display: true, text: 'Ngày' } },
          y: { title: { display: true, text: 'Lượt mua' } }
        }
      }
    })
  } catch (err) {
    console.error('Error fetching CSV:', err)
  }
}

onMounted(() => {
  fetchAndRenderChart()
})
</script>

<template>
  <div class="p-4">
    <h2 class="text-xl font-bold mb-2">Biểu đồ lượt mua từ Excel</h2>
    <canvas ref="chartCanvas"></canvas>
  </div>
</template>
