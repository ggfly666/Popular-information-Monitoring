<template>
    <div ref="chart" style="width: 700px; height: 350px;"></div>
</template>
  
<script>
import * as echarts from 'echarts';
import 'echarts-wordcloud'; 
import { ref, onMounted } from 'vue';
import axios from 'axios';
import { ElMessage } from 'element-plus';

export default {
  setup() {
    const chart = ref(null);
    const errorMessage = ref('');
    const wordFreqData = ref([]); 
    const isWordCloud = ref(true); 

    onMounted(async () => {
      try {
        const username = localStorage.getItem('username') || '';
        const response = await axios.get('http://127.0.0.1:8000/api/wbhotwordcloud', {
          params: { username: username }
        });
        const wordFreq = response.data.word_freq;
        const data = Object.keys(wordFreq).map(word => ({
          name: word,
          value: wordFreq[word]
        }));
        const myChart = echarts.init(chart.value);
        const wordCloudOption = {
          series: [{
            type: 'wordCloud',
            shape: 'circle',
            sizeRange: [12, 60],
            rotationRange: [-90, 90],
            rotationStep: 45,
            gridSize: 8,
            drawOutOfBound: false,
            textStyle: {
              fontFamily: 'sans-serif',
              fontWeight: 'bold',
              color: function () {
                const colors = [
                  '#5470C6', '#91CC75', '#EE6666', '#FAC858', '#73C0DE',
                  '#3BA272', '#FC8452', '#9A60B4', '#EA7CCC', '#FF9F7F'
                ];
                return colors[Math.floor(Math.random() * colors.length)];
              }
            },
            emphasis: {
              shadowBlur: 10,
              shadowColor: '#333'
            },
            data: data
          }]
        };
        wordFreqData.value = Object.entries(wordFreq)
          .sort((a, b) => b[1] - a[1]) 
          .slice(0, 10); 
        const barOption = {
          xAxis: {
            show: false 
          },
          yAxis: {
            type: 'category',
            data: wordFreqData.value.map(([word]) => word) 
          },
          series: [{
            type: 'bar',
            data: wordFreqData.value.map(([_, value]) => value),
            label: {
              show: true,
              position: 'right', 
              formatter: '{c}' 
            }
          }]
        };
        myChart.setOption(wordCloudOption);
        myChart.getZr().on('click', () => {
          if (isWordCloud.value) {
            myChart.clear(); 
            myChart.setOption(barOption); 
          } else {
            myChart.clear(); 
            myChart.setOption(wordCloudOption); 
          }
          isWordCloud.value = !isWordCloud.value; 
        });
      } catch (error) {
        ElMessage.error('无法加载，请检查网络连接！');
      }
    });
    return {
      chart
    };
  }
};
</script>