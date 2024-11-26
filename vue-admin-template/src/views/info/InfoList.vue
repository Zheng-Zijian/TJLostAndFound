<template>
    <div class="info-list-page">
      <el-row>
        <el-col :span="8">
          <el-card>
            <el-input v-model="searchText" placeholder="搜索信息" />
            <el-table :data="infoList" @row-click="selectInfo">
              <el-table-column prop="title" label="标题" />
              <el-table-column prop="category" label="分类" />
            </el-table>
          </el-card>
        </el-col>
        <el-col :span="16">
          <el-card v-if="selectedInfo">
            <h3>{{ selectedInfo.title }}</h3>
            <p>分类: {{ selectedInfo.category }}</p>
            <p>{{ selectedInfo.content }}</p>
          </el-card>
          <el-empty v-else description="请选择一条信息" />
        </el-col>
      </el-row>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        searchText: '',
        infoList: [], // 信息列表数据
        selectedInfo: null // 当前选中的信息
      };
    },
    mounted() {
      this.fetchInfoList();
    },
    methods: {
      fetchInfoList() {
        // 获取信息列表数据
        this.$http.get('/api/info').then(res => {
          this.infoList = res.data;
          if (res.data.length > 0) {
            this.selectedInfo = res.data[0]; // 默认选择第一条
          }
        });
      },
      selectInfo(row) {
        this.selectedInfo = row; // 设置选中的信息
      }
    }
  };
  </script>
  