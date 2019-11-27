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
        <el-row :gutter="10" type="flex" class="row-bg" justify="center" style="transform: translateY(-20px);"> 
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
                <div id="chartAlarm" style="width:100%; height:100px;text-align: center;
                         padding-top: 30px;box-sizing: border-box;">
                    <el-popover
                        placement="top"
                        width="160"
                        v-model="visible">
                        <p>你是否确认已注意到预警，并关闭提示吗？</p>
                        <div style="text-align: right; margin: 0">
                            <el-button size="mini" type="text" @click="visible = false">否</el-button>
                            <el-button type="primary" size="mini" @click="visible = false">是</el-button>
                        </div>
                        <el-button slot="reference">空预器堵塞预警</el-button>
                    </el-popover>
                </div>
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
        visible: false,
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
                        data : ['0','3.175'],
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
                        areaStyle: {normal: {}},
                        data:[0.4671, 1.5873]
                    },

                    {
                        name:'正常范围',
                        type:'line',
                        stack: '总量',
                        symbol:'none',  //去掉点
                        smooth:true,    //让曲线变平滑的 
                        areaStyle: {normal: {}},
                        data:[0.0929, 0.3177]
                    },

                    {
                        name:'一级告警区域',
                        type:'line',
                        stack: '总量',
                        symbol:'none',  
                        smooth:true,    
                        areaStyle: {normal: {}},
                        data:[0.1407,0.476]
                    },
                    {
                        name:'二级告警区域',
                        type:'line',
                        stack: '总量',
                        symbol:'none',  
                        smooth:true,   
                        areaStyle: {normal: {}},
                        data:[0.2335, 0.794]
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
                        data:[2.5658, 0.325]
                    }
                ]
            });

         })
    }
  },
  mounted() {
    this.getUsers();
    this.drawStackedAreaChart();
    // this.drawLineTest();
    },
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
