<template>
    <section class="chart-container" style="height:100%;width:100%; background-color:#DAEAF2">
        <el-row :gutter="10" type="flex" class="row-bg" justify="center">
            <el-col :span="12">
                <!-- <div id="chartTable" style="width:50%; height:250px;"></div> -->
                <!-- <el-table :data="users" highlight-current-row v-loading="listLoading" @selection-change="selsChange" style="width: 93%;"> -->
                <el-table :data="users" style="width: 93%; hight= 40%">
                    <el-table-column prop="name" label=" 数据项" hight="20" width="150" >
                    </el-table-column>
                    <el-table-column prop="groupA" label="A侧" hight="20" width="100">
                    </el-table-column>
                    <el-table-column prop="groupB" label="B侧" hight="20" width="100">
                    </el-table-column>
                    <el-table-column prop="unit" label="单位" hight="20" width="100">
                    </el-table-column>
                </el-table>
            </el-col>
            <el-col :span="12">
                <div id="chartStackedArea" style="width:100%; height:360px; background-color:#F0F2EE"> </div>
            </el-col>
        </el-row>
        <br>
        <el-row :gutter="10" type="flex" class="row-bg" justify="center">
            <el-col :span="12">
                <div id="chartTxt" style="width:85%; height:150px; outline-style:ridge; background-color:#F0F2EE">
                    <h1 style="font-family:verdana; color:#3399FF"> 专家建议：</h1>
                    <div class = "expertAdvice"> </div>
                    <body>
                    <p1> 1,提高吹灰频次<br></p1>
                    <p2> 2,调整燃煤硫分<br></p2>
                    <p3> 3,提高空预器入口风温<br></p3>
                    <p4> 4,提高排烟温度<br></p4>
                    </body>
                </div>
            </el-col>
            <el-col :span="12">
                <!-- <h2>vue中插入Echarts示例</h2> -->
                <div id="chartAlarm" style="width:100%; height:100px;"></div>
            </el-col>
        </el-row>
    </section>
</template>

<script>
import echarts from "echarts";
import util from "../../common/js/util";
import { getdrawPieChart, getdrawStackedAreaChart } from "../../api/api";
import { getUserListPage, removeUser, batchRemoveUser } from "../../api/api";
export default {
    data() {
        return {
        filters: {
            name: ""
        },
        users: [],
        page_size: 40,
        total: 0,
        page: 1,
        chartStackedArea: null,
        };
    },
    methods: {
    handleCurrentChange(val) {
      this.page = val;
      this.getUsers();
    },
    //获取用户列表
    getUsers() {
      let para = {
        page: this.page,
        name: this.filters.name
      };
      this.listLoading = true;
      //NProgress.start();
      getUserListPage(para).then(res => {
        this.total = res.data.total;
        this.page_size = res.data.page_size;
        this.users = res.data.infos;
        this.listLoading = false;
      });
    },
    //画实时曲线图
    drawStackedAreaChart() {
         this.chartStackedArea = echarts.init(document.getElementById("chartStackedArea"));
         getdrawStackedAreaChart().then(res => {
            let { x, y, code } = res.data;
            this.chartStackedArea.setOption ({
                // title: {
                //     text: '空预器实时预警'
                // },
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
                    bottom: '13%',
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
    }
  },
  mounted() {
    // Console.log("runtimedata mounted"); // 打印不出来啊
    this.getUsers();
    this.drawStackedAreaChart();
    this.drawLineTest();
    
    let this_ = this;
      let myChart = echarts.init(document.getElementById('chartAlarm'));
      let options = {
        color: ['#f44'],
        tooltip : {
          trigger: 'axis',
          axisPointer : {
            type : 'shadow'
          }
        },
        xAxis : [
          {
            type : 'category',
            data : ['1月','2月','3月','4月','5月','6月','7月','8月','9月','10月','11月','12月',],
            axisTick: {
              alignWithLabel: true
            }
          }
        ],
        yAxis : [
          {
            type : 'value'
          }
        ],
        series : [
          {
            name:'每月花费',
            type:'bar',
            barWidth: '60%',
            data:[995,666,444,858,654,236,645,546,846,225,547,356]
          }
        ]
      };
      myChart.setOption(options);
 
      //建议加上以下这一行代码，不加的效果图如下（当浏览器窗口缩小的时候）。超过了div的界限（红色边框）
      window.addEventListener('resize',function() {myChart.resize()});
    },
    // methods: {},
    // watch: {},
    // created() {
    // }
//   updated: function() {
//     this.getUsers();
//     this.drawStackedAreaChart();
//   }
};
</script>

<style scoped>
.chart-container {
  width: 100%;
  float: left;
}
#chartStackedArea{
    width: 50%;
    height: 500px;
    /* border: 1px solid red; */
    margin: 0 auto;
}

h2{
text-align: center;
padding: 30px;
font-size: 18px;
}
#chartAlarm{
width: 50%;
height: 500px;
border: 1px solid red;
margin: 0 auto;
}
</style>

<style>
.el-table td, .el-table th {
    height:35px ;
    min-width: 0;
    text-overflow: ellipsis;
    vertical-align: middle;
}
</style>
