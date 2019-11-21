import Login from './views/Login.vue'
import NotFound from './views/404.vue'
import Home from './views/Home.vue'
import Table from './views/nav1/Table.vue'
// import Table from './views/runtimeAlarm/RuntimeDataTable.vue'
import echarts from './views/charts/echarts.vue'
// import echarts from './views/history/historyEcharts.vue'

let routes = [
    {
        path: '/login',
        component: Login,
        name: '',
        hidden: true
    },
    {
        path: '/404',
        component: NotFound,
        name: '',
        hidden: true
    },
    //{ path: '/main', component: Main },
    {
        path: '/',
        component: Home,
        name: '',
        leaf: true,//只有一个节点
        iconCls: 'fa fa-area-chart',//图标样式class
        children: [
            { path: '/table', component: Table, name: '实时告警' },
        ]
    },
    {
        path: '/',
        component: Home,
        name: '',
        leaf: true,
        iconCls: 'fa fa-calendar',
        children: [
            { path: '/echarts', component: echarts, name: '历史查询' }
        ]
    },
    {
        path: '*',
        hidden: true,
        redirect: { path: '/404' }
    }
];

export default routes;