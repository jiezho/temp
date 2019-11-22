<template>
    <section class="chart-container">
        <el-row>
            <el-col :span="12">
                <div id="chartLine" style="width:100%; height:250px;"></div>
            </el-col>
        </el-row>
    </section>
</template>

<script>
import echarts from "echarts";
import { getdrawPieChart, getdrawLineChart } from "../../api/api";
export default {
  data() {
    return {
      chartLine: null,
      chartPie: null
    };
  },

  methods: {
    drawLineChart() {
      this.chartLine = echarts.init(document.getElementById("chartLine"));
      getdrawLineChart().then(res => {
        let { profess_value, grade_value, grade_data, code } = res.data;
        if (code !== 200) {
          this.$message({
            message: "服务端发生错误",
            type: "warning"
          });
        } else {
          var series = [];
          for (var grade in grade_data) {
            var new_series = {
              name: grade,
              type: "bar",
              stack: "总量",
              data: grade_data[grade],
              markPoint: {
                data: [
                  { type: "max", name: "最大值" },
                  { type: "min", name: "最小值" }
                ]
              },
              markLine: {
                data: [{ type: "average", name: "平均值" }]
              }
            };
            series.push(new_series);
          }
          this.chartLine.setOption({
            title: {
              text: "空预器堵塞系数"
            },
            tooltip: {
              trigger: "axis"
            },
            legend: {
              data: grade_value
            },
            toolbox: {
              show: true,
              feature: {
                magicType: { show: true, type: ["line", "bar"] },
                saveAsImage: { show: true }
              }
            },
            calculable: true,
            xAxis: [
              {
                type: "category",
                data: profess_value
              }
            ],
            yAxis: [
              {
                type: "value"
              }
            ],
            series: series
          });
        }
      });
    },

    drawCharts() {
      this.drawLineChart();
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
