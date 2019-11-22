<template>
	<section>

		<!--列表-->
		<el-table :data="users" highlight-current-row v-loading="listLoading" @selection-change="selsChange" style="width: 39%;">
			<el-table-column prop="name" label=" 数据项" hight="20" width="150" >
			</el-table-column>
			<el-table-column prop="groupA" label="A侧" hight="20" width="80">
			</el-table-column>
			<el-table-column prop="groupB" label="B侧" hight="20" width="80">
			</el-table-column>
      <el-table-column prop="unit" label="单位" hight="20" width="100">
			</el-table-column>
		</el-table>

	</section>
</template>

<script>
import util from "../../common/js/util";
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
  },
  mounted() {
    this.getUsers();
  }
};
</script>

<style scoped>

</style>