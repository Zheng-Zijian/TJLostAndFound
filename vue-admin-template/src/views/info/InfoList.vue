<template>
    <div class="app-container">
    <h2 class="title" style="text-align: center;">信息列表</h2>
    <el-form :inline=true>
    <div class="search-bar">
      <el-form-item label="搜索:">
        <el-input v-model="search" placeholder="搜索信息..." @keydown.enter.native="handleSearch" class="input" />
      </el-form-item>
      <el-form-item label="类别:">
        <el-select v-model="category" placeholder="请选择类别" @change="getInfoList">
          <el-option value="" label="所有类别" />
          <el-option label="丢失物品" value="丢失物品"/>
          <el-option label="捡到物品" value="捡到物品"/>
        </el-select>
      </el-form-item>
    </div>
    </el-form>
    <el-table :data="infoList" style="width: 100%">
      <el-table-column prop="title" label="标题" width="180"></el-table-column>
      <el-table-column prop="category" label="分类" width="180"></el-table-column>
      <el-table-column prop="created_at" label="创建时间" width="180"></el-table-column>
      <el-table-column prop="content" label="内容"></el-table-column>
    </el-table>
  </div>
</template>

<script>
import { fetchInfoList } from '@/api/info';

export default {
  data() {
    return {
      infoList: [],
      search: '',
      category: '',
      sortOrder: 'desc',
      listLoading: true
    };
  },
  created() {
    this.getInfoList();
  },
  methods: {
    handleSearch() {
      this.getInfoList();
    },

    getInfoList() {
      this.listLoading = true;
      fetchInfoList({
        search: this.search.trim(),
        category: this.category,
        sort: this.sortOrder
      })
        .then(response => {
          this.infoList = response.data;
          this.listLoading = false;
        })
        .catch(error => {
          console.error('获取信息列表失败:', error);
          this.listLoading = false;
        });
        console.log('值:', this.infoList);
    }
  }
};
</script>

<style scoped>
.search-bar {
  display: flex;
  align-items: center;
  margin-bottom: 5px;
}

.search-input {
  margin-right: 10px;
  flex: 1;
}

.search-select {
  margin-right: 10px;
  width: 200px;
}
</style>
  