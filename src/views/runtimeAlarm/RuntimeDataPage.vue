<template>
    <section class="chart-container" style="height:100%;width:100%; background-color:#DAEAF2">
        <el-row :gutter="10" type="flex" class="row-bg" justify="center">
            <el-col :span="12">
                <!-- <div id="chartTable" style="width:50%; height:250px;"></div> -->
                <el-table :data="users" highlight-current-row v-loading="listLoading" @selection-change="selsChange" style="width: 85%; background-color:#EAE9DC">
                    <el-table-column prop="name" label=" 数据项" hight="20" width="150" >
                    </el-table-column>
                    <el-table-column prop="groupA" label="A侧" hight="20" width="80">
                    </el-table-column>
                    <el-table-column prop="groupB" label="B侧" hight="20" width="80">
                    </el-table-column>
                    <el-table-column prop="unit" label="单位" hight="20" width="100">
                    </el-table-column>
                </el-table>
            </el-col>
            <el-col :span="12">
                <div id="chartLine" style="width:50%; height:250px;"></div>
            </el-col>
        </el-row>
        <br>
        <el-row :gutter="10" type="flex" class="row-bg" justify="center">
            <el-col :span="12">
                <div id="chartTxt" style="width:85%; height:250px; outline-style:ridge; background-color:#F0F2EE">
                    <h1 style="font-family:verdana; color:#3399FF"> 专家建议：</h1>
                    <div class = "expertAdvice">

                    </div>
                    <p border-style:inset; "expertAdvice"</p>
                </div>
            </el-col>
            <el-col :span="12">
                <div id="chartAlarm" style="width:50%; height:250px;"></div>
            </el-col>
        </el-row>
    </section>
</template>

<script>
import echarts from "echarts";
import util from "../../common/js/util";
import { getdrawPieChart, getdrawLineChart } from "../../api/api";
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
      chartLine: null,
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
    drawLineChart() {
         this.chartLine = echarts.init(document.getElementById("chartLine"));
         getdrawLineChart().then(res => {
            // let { profess_value, grade_value, grade_data, code } = res.data;
            option = {
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
            };
            
            // this.chartLine.setOption(option);
            if (option && typeof option === "object") {
                this.chartLine.setOption(option, true);
            }
         })
    }
  },
  mounted() {
    this.getUsers();
    this.drawLineChart();
  },
  updated: function() {
    this.getUsers();
    this.drawLineChart();
  }
};
</script>

<style scoped>
.chart-container {
  width: 100%;
  float: left;
}
</style>

