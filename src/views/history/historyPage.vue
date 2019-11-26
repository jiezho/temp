<template>
    <section class="chart-container">
        <el-row>
            <el-col :span="12">
                <div id="chartLine" style="width:100%; height:400px;"></div>
            </el-col>
            <el-col :span="12">
                <div id="chartStackedArea" style="width:100%; height:400px;"></div>
            </el-col>
        </el-row>
        <br>
        <el-row>
            <el-col :span="12">
                <div id="chartPie" style="width:100%; height:400px;"></div>
            </el-col>
            <el-col :span="12">
                <div id="chartPie1" style="width:100%; height:400px;"></div>
            </el-col>
        </el-row>
    </section>
</template>

<script>
import echarts from "echarts";
import { getdrawPieChart, getdrawStackedAreaChart, getdrawLineChart } from "../../api/api";
export default {
  data() {
    return {
      chartLine: null,
      chartStackedArea: null,
      chartPie: null
    };
  },

  methods: {
    drawLineChart() {
      this.chartLine = echarts.init(document.getElementById("chartLine"));
      getdrawLineChart().then(res => {
        let { profess_value, grade_value, grade_data, code } = res.data;
        // if (code !== 200) {
        //   this.$message({
        //     message: "服务端发生错误",
        //     type: "warning"
        //   });
        // } else {
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
              text: "来源分布"
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
        // }
      });
    },
    drawStackedAreaChart() {
        this.chartStackedArea = echarts.init(document.getElementById("chartStackedArea"));
        getdrawStackedAreaChart().then(res => {
            let { x, y, code } = res.data;
            this.chartStackedArea.setOption ({
                title: {
                    text: '空预器实时预警'
                },
                tooltip : {
                    trigger: 'axis',
                    axisPointer: {
                        type: 'cross',
                        label: {
                            backgroundColor: '#6a7985'
                        }
                    }
                },
                legend: {
                    data:['正常范围','一级告警区域','二级告警区域','三级告警区域'],
                    // selected:{'正常范围':false,'一级告警区域':false},
                    icon: ["circle", "circle", "circle", "circle"]
                },
                color: ['#FFFFF0',"#C1FFC1","#FFDAB9","#FFA500","#CD5555"],
                toolbox: {
                    feature: {
                        saveAsImage: {}
                    }
                },
                grid: {
                    left: '3%',
                    right: '4%',
                    bottom: '3%',
                    top: '8%',
                    containLabel: true
                },
                xAxis : [
                    {
                        type : 'category',
                        boundaryGap : false,
                        data : ['200','800'],
                        text: '机组负荷(MW)'
                    }
                ],
                yAxis : [
                    {
                        type : 'value'
                    }
                ],
                series : [
                    {
                        name:'空区',
                        type:'line',
                        stack: '总量',
                        symbol:'none',  
                        smooth:true,    
                        areaStyle: {},
                        data:[50,200]
                    },

                    {
                        name:'正常范围',
                        type:'line',
                        stack: '总量',
                        symbol:'none',  //去掉点
                        smooth:true,    //让曲线变平滑的 
                        areaStyle: {},
                        data:[50,200]
                    },

                    {
                        name:'一级告警区域',
                        type:'line',
                        stack: '总量',
                        symbol:'none',  
                        smooth:true,    
                        areaStyle: {},
                        data:[50,300]
                    },
                    {
                        name:'二级告警区域',
                        type:'line',
                        stack: '总量',
                        symbol:'none',  
                        smooth:true,   
                        areaStyle: {normal: {}},
                        data:[50,400]
                    },
                    
                    {
                        name:'三级告警区域',
                        type:'line',
                        stack: '总量',
                        symbol:'none',  
                        smooth:true,   
                        label: {
                            normal: {
                                show: true,
                                position: 'top'
                            }
                        },
                        areaStyle: {normal: {}},
                        data:[1300,400]
                    }
                ]
            });
            // this.chartLine.setOption({
            // title: {
            //   text: "空预器堵塞系数"
            // },
            // });
            // this.chartStackedArea.setOption(option);
            // if (option && typeof option === "object") {
            //     this.chartStackedArea.setOption(option, true);
            // }
         })
    },
    drawPieChart() {
      this.chartPie = echarts.init(document.getElementById("chartPie"));
      getdrawPieChart().then(res => {
        let { value, code, total } = res.data;
        if (code !== 200) {
          this.$message({
            message: "服务端发生错误",
            type: "warning"
          });
        } else {
          this.chartPie.setOption({
            title: {
              text: "意向占比",
              subtext: "总人数:" + total,
              x: "center"
            },
            tooltip: {
              trigger: "item",
              formatter: "{a} <br/>{b} : {c} ({d}%)"
            },
            legend: {
              orient: "vertical",
              left: "left",
              data: ["视觉", "视频", "前端", "办公", "后端", "运营", "移动"] // 和value一一对应
            },
            toolbox: {
              show: true,
              feature: {
                saveAsImage: { show: true }
              }
            },
            series: [
              {
                name: "占比数",
                type: "pie",
                radius: "55%",
                center: ["50%", "60%"],
                data: [
                  { value: value[0], name: "视觉" },
                  { value: value[1], name: "视频" },
                  { value: value[2], name: "前端" },
                  { value: value[3], name: "办公" },
                  { value: value[4], name: "后端" },
                  { value: value[5], name: "运营" },
                  { value: value[6], name: "移动" }
                ],
                itemStyle: {
                  emphasis: {
                    shadowBlur: 10,
                    shadowOffsetX: 0,
                    shadowColor: "rgba(0, 0, 0, 0.5)"
                  }
                }
              }
            ]
          });
        }
      });
    },
    drawCharts() {
      this.drawLineChart();
      this.drawStackedAreaChart();
      this.drawPieChart();
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
