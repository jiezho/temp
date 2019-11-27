<template>
    <section class="chart-container" style="height:100%;width:100%; background-color:#DAEAF2">
        <el-row>
            <el-col :span="12">
                <div id="airClogChart" style="width:100%; height:200px;"></div>
            </el-col>
            <el-col :span="12"> 
                <div id="sizeNH3Chart" style="width:100%; height:200px;"></div>
            </el-col>
        </el-row>
        <br>
        <el-row>
            <el-col :span="12">
                <div id="airDeposiChart" style="width:100%; height:200px;"></div>
            </el-col>
            <el-col :span="12">
                <div id="chartPie1" style="width:100%; height:400px;"></div>
            </el-col>
        </el-row>
    </section>
</template>

<script>
import echarts from "echarts";
import { getdrawPieChart, getdrawStackedAreaChart, getdrawLineChart, getdrawHistoryChart } from "../../api/api";
import { getdrawAirClogChart, getdrawSizeNH3Chart, getdrawAirDeposiChart } from "../../api/api";
export default {
  data() {
    return {
      chartLine: null,
      chartStackedArea: null,
      chartPie: null,
      getdrawHistoryChart: null
    };
  },

  methods: {
    drawLineChart() {
      this.airClogChart = echarts.init(document.getElementById("airClogChart"));
      getdrawAirClogChart().then(res => {
        let { code, listAirClogA, listAirClogB } = res.data; 
          this.airClogChart.setOption({
            title: {
                text: '空预器堵塞系数'
            },
            tooltip: {
                trigger: 'axis'
            },
            xAxis: {
                data: listAirClogA.map(function (item) {
                    return item[0];
                }),
  
            },
            yAxis: {
                splitLine: {
                    show: false
                }
            },
            leged: {
              data:['空预器A', '空预器B'],
              // icon:["circle","circle"]
            },
            toolbox: {
            left: 'center',
            feature: {
                dataZoom: {
                    yAxisIndex: 'none'
                },
                restore: {},
                saveAsImage: {}
            }
          },
          dataZoom: [{
            startValue: '2014-06-01'
        }, {
            type: 'inside'
        }],
          series: [{
            name: 'A空预器',
            type: 'line',
            data: listAirClogA.map(function (item) {
                return item[1];
            }),
          },
          {
            name: 'B空预器',
            type: 'line',
            data: listAirClogB.map(function (item) {
                return item[1];
            }),
          }],
          });
        // }
      });
    },

    drawLineChart1() {
      this.sizeNH3Chart = echarts.init(document.getElementById("sizeNH3Chart"));
      getdrawSizeNH3Chart().then(res => {
        let { code, listSizeNH3Actual, listSizeNH3Demand } = res.data; 
          this.sizeNH3Chart.setOption({
            title: {
                text: '脱硝喷氨量 kg/h'
            },
            tooltip: {
                trigger: 'axis'
            },
            xAxis: {
                data: listSizeNH3Actual.map(function (item) {
                    return item[0];
                }),
  
            },
            yAxis: {
                splitLine: {
                    show: false
                }
            },
            leged: {
              data:['实际喷氨量', '喷氨需求量'],
              // icon:["circle","circle"]
            },
            toolbox: {
            left: 'center',
            feature: {
                dataZoom: {
                    yAxisIndex: 'none'
                },
                restore: {},
                saveAsImage: {}
            }
          },
          dataZoom: [{
            startValue: '2014-06-01'
        }, {
            type: 'inside'
        }],
          series: [{
            name: '实际喷氨量',
            type: 'line',
            data: listSizeNH3Actual.map(function (item) {
                return item[1];
            }),
          },
          {
            name: '喷氨需求量',
            type: 'line',
            data: listSizeNH3Demand.map(function (item) {
                return item[1];
            }),
          }],
          });
        // }
      });
    },

    drawLineChart2() {
      this.airDeposiChart = echarts.init(document.getElementById("airDeposiChart"));
      getdrawAirDeposiChart().then(res => {
        let { code, listAirDeposiA, listAirDeposiB } = res.data; 
          this.airDeposiChart.setOption({
            title: {
                text: '空预器沉积系数'
            },
            tooltip: {
                trigger: 'axis'
            },
            xAxis: {
                data: listAirDeposiA.map(function (item) {
                    return item[0];
                }),
  
            },
            yAxis: {
                splitLine: {
                    show: false
                }
            },
            leged: {
              data:['空预器A', '空预器B'],
              // icon:["circle","circle"]
            },
            toolbox: {
            left: 'center',
            feature: {
                dataZoom: {
                    yAxisIndex: 'none'
                },
                restore: {},
                saveAsImage: {}
            }
          },
          dataZoom: [{
            startValue: '2014-06-01'
        }, {
            type: 'inside'
        }],
          series: [{
            name: '空预器A',
            type: 'line',
            data: listAirDeposiA.map(function (item) {
                return item[1];
            }),
          },
          {
            name: '空预器B',
            type: 'line',
            data: listAirDeposiB.map(function (item) {
                return item[1];
            }),
          }],
          });
        // }
      });
    },

    drawCharts() {
      this.drawLineChart();
      this.drawLineChart1();
      this.drawLineChart2();
      // this.drawStackedAreaChart();
      // this.drawPieChart();
    }
  },

  mounted: function() {
    this.drawCharts();
  },
  updated: function() {
    this.drawCharts();
  }
};
</script>

<style scoped>
.chart-container {
  width: 100%;
  float: left;
}
/*.chart div {
        height: 400px;
        float: left;
    }*/

.el-col {
  padding: 30px 20px;
}
</style>
