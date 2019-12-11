<template>
  <div>
    <section class="chart-container" style="height:100%;width:100%; background-color:#DAEAF2;padding-bottom: 30px;">
        <el-row :gutter="10" type="flex" class="row-bg" justify="center">
            <el-col :span="12" style="padding-right:0px;">
                <!-- <div id="chartTable" style="width:50%; height:250px;"></div> -->
                <!-- <el-table :data="users" highlight-current-row v-loading="listLoading" @selection-change="selsChange" style="width: 93%;"> -->
                <el-table :data="users" style="width: 100%;height: 330px;">
                    <el-table-column prop="name" label=" 数据项" hight="20" width="150" >
                    </el-table-column>
                    <el-table-column prop="groupA" label="A侧" hight="20">
                    </el-table-column>
                    <el-table-column prop="groupB" label="B侧" hight="20">
                    </el-table-column>
                    <el-table-column prop="unit" label="单位" hight="20" width="100">
                    </el-table-column>
                </el-table>
            </el-col>
            <el-col :span="12" style="padding-left:0px;position:relative;">
                <div id="chartStackedArea" style="width:100%; height:390px; background-color:#F0F2EE"></div>
                <div class="data-img">
                  <span class="point1" :style="{'left': ((point1[0] - 200)/600)*100 + '%', bottom: ((point1[1] + 1.2)/5.1)*100 + '%'}"></span>
                  <span class="point1-label" :style="{'left': ((point1[0] - 200 + 20)/600)*100 + '%', bottom: ((point1[1] + 1.2 + 0.1)/5.1)*100 + '%'}">
                    A: [{{point1[0]}}, {{point1[1]}}]
                  </span>
                  <span class="point2" :style="{'left': ((point2[0] - 200)/600)*100 + '%', bottom: ((point2[1] + 1.2)/5.1)*100 + '%'}"></span>
                  <span class="point1-label" :style="{'left': ((point2[0] - 200 + 20)/600)*100 + '%', bottom: ((point2[1] + 1.2 + 0.1)/5.1)*100 + '%'}">
                    B: [{{point2[0]}}, {{point2[1]}}]
                  </span>
                </div>
                <div class="echarts-label">机组负荷(MW)</div>
            </el-col>
        </el-row>

        <el-row :gutter="10" type="flex" justify="center" style="transform:translateY(-35px);padding:0px 10px;"> 
            <el-col :span="12">
                <div id="chartTxt" style="background-color:#F0F2EE;padding:5px 20px;padding-top:0px;">
                    <h1 style="font-family:verdana; color:#3399FF"> 专家建议：</h1>
                    <div class = "expertAdvice"> </div>
                    <body>
                     <p1 v-for="(str,dex) in suggestion" :key="dex"> {{str}}<br></p1>
                    </body>
                </div>
            </el-col>
            <el-col :span="12">
                <div id="chartAlarm" style="width:100%; height:100px;text-align: center;border:none;
                         padding-top: 30px;box-sizing: border-box; translateY(+20px)">

                    <span style="display: inline-block;width:50px;">
                      <i class="el-icon-warning el-icon" v-if="showIcon"></i>
                    </span>
                    
                    <!-- <el-popover
                        placement="top"
                        width="160"
                        v-model="visible">
                        <p>你是否确认已注意到预警，并关闭提示吗？</p>
                        <div style="text-align: right; margin: 0">
                            <el-button size="mini" type="text" @click="visible = false">否</el-button>
                            <el-button type="primary" size="mini" @click="closeNotice">是</el-button>
                        </div>
                        <el-button slot="reference">空预器堵塞预警</el-button>
                    </el-popover> -->

                    <el-button @click="showConfirm">空预器堵塞预警</el-button>
                    <p style="margin-top:10px;"></p>
                    <el-date-picker
                      v-model="date"
                      type="datetime"
                      value-format="yyyy-MM-dd HH:mm:ss"
                      placeholder="选择日期时间">
                    </el-date-picker>
                    <el-button @click="checkRecord">查看历史数据</el-button>
                </div>
            </el-col>
        </el-row>
    </section>
  </div>
</template>

<script>
import echarts from "echarts";
import util from "../../common/js/util";
import { getdrawPieChart, getdrawStackedAreaChart } from "../../api/api";
import { getUserListPage, removeUser, batchRemoveUser, getDataPoints} from "../../api/api";
export default {
    name: 'runtime',
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
        timer: null,
        timer2: null,
        timer3: null,
        point1: [],
        point2: [],
        suggestion: ['1,提高吹灰频次', '2,调整燃煤硫分','3,提高空预器入口风温'],
        showIcon: false,
        date: ''
      }
    },
    mounted() {
      clearInterval(this.timer)
      this.timer = setInterval(()=>{
        this.getUsers();
      }, 1000)

      clearInterval(this.timer2)
      this.timer = setInterval(()=>{
        this.getPoint();
      }, 1000)

      this.drawStackedAreaChart();

      this.sendNotice()
      // this.drawLineTest();
    },
    destroyed() {
      clearInterval(this.timer);
      clearInterval(this.timer2)
    },
    methods: {
      handleCurrentChange(val) {
        this.page = val;
        this.getUsers();
      },
      getPoint() { // 获取点坐标

      },
      sendNotice() { // 显示警告
        clearInterval(this.timer3)
        this.timer3 = setInterval(()=>{
          this.showIcon = !this.showIcon
        }, 1000)
      },
      closeNotice() { // 关闭警告
        console.log('close')
        clearInterval(this.timer3)
        this.showIcon = false
      },
      checkRecord() { // 查看历史数据
        const date = this.date // 时间
      },
      showConfirm() {
        this.$confirm('您是否确认已注意到预警，并关闭提示吗？', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          this.closeNotice()
        }).catch(() => {
          this.$message({
            type: 'info',
            message: '已取消操作'
          });          
        });
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
      //获取不同负荷下烟气侧压力oint
      getPoints() {
        getDataPoints(para).then(res => {
          this.point1 = res.point1;
          this.point2 = res.point2;
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
                          name: '机组负荷(MW)',
                          nameLocation: 'end',
                          nameTextStyle: { color: '#D4FFF9', fontSize: 10 },
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
  }
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
.data-img{
  width: 100%;
  height: 100%;
  position: absolute;
  left: 0px;
  top: 0px;
  z-index: 999;
}
.point1{
  width: 0;
  height: 0;
  border-style: solid;
  border-width: 0 9px 16px 10px;
  border-color: transparent transparent #3a3533 transparent;
  position: absolute;
  left: 0px;
  bottom: 0px;
}
.point2{
  width: 0;
  height: 0;
  border-style: solid;
  border-width: 0 9px 16px 10px;
  border-color: transparent transparent #1688da transparent;
  position: absolute;
  left: 0px;
  bottom: 0px;
}
.point1-label{
  display: inline-block;
  width: 100px;
  height: 20px;
  line-height: 20px;
  text-align: center;
  background: rgba(0, 0, 0, 0.1);
  color: #333;
  position: absolute;
  left: 0px;
  bottom: 0px;
}
.echarts-label{
  text-align: center;
  font-size: 15px;
  color: #333;
  transform: translateY(-55px);
}
.el-icon{
  font-size: 22px;
  color: #ff0000;
  margin-right: 10px;
  position: relative;
  top: 5px;
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
