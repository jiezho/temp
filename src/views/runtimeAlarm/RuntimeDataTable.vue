<template>
	<section>
        <el-table :data="tableDataalllist" border style="width: 100%" @sort-change="totalusercount">
            <el-table-column :label="head" :prop="head" v-for="(head, index) in header" :key="head" :sortable="定义自定义排序项">
                <template slot-scope="scope">
                {{tableDataalllist[scope.$index][index]}} // 当前行数据  接收两个参数scope.$index; scope.row
                <template>
            <el-table-column>
        <el-table>
    </section>
</template>

<script>
    export default{
        data(){
            return{
            // 数据结构
                tableDataalllist:[{
                    1,'张三','23'
                },{
                    2,'李四','15'
                },{
                    3,'王五','18'
                }],
                header:['id','name','age']
            }  
        },
        methods:{
        // 接受一个obj参数
            totalusercount(obj){
                console.log(obj.prop)  // 排序规则
                console.log(obj.order)  // 排序方式
            }
        }
    }
</script>

<style scoped>

</style>
