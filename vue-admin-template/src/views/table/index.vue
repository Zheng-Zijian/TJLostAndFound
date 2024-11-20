<template>
  <div class="app-container">
    <h2 class="title" style="text-align: center;">失物列表</h2>
    <el-form :inline=true>
      <el-form-item label="物品:">
        <el-input v-model="search" placeholder="搜索失物..." @keydown.enter.native="handleSearch" class="input" />
      </el-form-item>
      <el-form-item label="类别:">
        <el-select v-model="category" placeholder="请选择类别" @change="fetchItems">
          <el-option value="" label="所有类别" />
          <el-option value="雨伞" label="雨伞" />
          <el-option value="眼镜" label="眼镜" />
          <el-option value="3C电子" label="3C电子" />
        </el-select>
      </el-form-item>
      <el-form-item label="状态:">
        <el-select v-model="claimedStatus" placeholder="请选择状态" @change="fetchItems">
          <el-option value="" label="全部" />
          <el-option value="claimed" label="已认领" />
          <el-option value="unclaimed" label="未认领" />
        </el-select>
      </el-form-item>
    </el-form>
    <el-table v-loading="listLoading" :data="items" element-loading-text="Loading" border fit highlight-current-row
      :default-sort="{ prop: 'time', order: 'descending' }">
      <el-table-column align="center" label="编号" width="95">
        <template slot-scope="scope">
          #{{ scope.row.id }}
        </template>
      </el-table-column>
      <el-table-column label="物品名称" align="center">
        <template slot-scope="scope">
          {{ scope.row.item_name }}
        </template>
      </el-table-column>
      <el-table-column label="类别" align="center">
        <template slot-scope="scope" align="center">
          <span>{{ scope.row.category }}</span>
        </template>
      </el-table-column>
      <el-table-column label="拾得地点" width="110" align="center">
        <template slot-scope="scope">
          {{ scope.row.location }}
        </template>
      </el-table-column>
      <el-table-column align="center" prop="time" label="拾得时间" sortable>
        <template slot-scope="scope">
          <i class="el-icon-time" />
          <span>{{ scope.row.found_date }}</span>
        </template>
      </el-table-column>
      <el-table-column label="上传用户" align="center">
        <template slot-scope="scope">
          <el-button type="text" @click="showContactInfo(scope.row.upload_user, scope.row.contact_info)"> <span style="
            text-decoration: underline;">{{ scope.row.upload_user
              }}</span></el-button>
        </template>
      </el-table-column>
      <el-table-column class-name="status-col" label="状态" align="center">
        <template slot-scope="scope">
          <el-tag :type="scope.row.claimed | statusFilter">{{ scope.row.claimed ? '已认领' : '未认领' }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column label="类别" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.claimed_user || '--' }}</span>
        </template>
      </el-table-column>

    </el-table>
    <!-- 用户详细信息对话框 -->
    <el-dialog :visible.sync="modalVisible" title="上传用户信息">
      <p><strong>上传用户:</strong> {{ modalUser }}</p>
      <p><strong>联系方式:</strong> {{ modalContact }}</p>
      <span slot="footer" class="dialog-footer">
        <el-button type="primary" @click="closeModal">关 闭</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import { getItems } from '@/api/table'
import _ from 'lodash';
export default {
  filters: {
    statusFilter(status) {
      if (status) {
        return 'success'
      }
      return ''
    }
  },
  data() {
    return {
      results: [],
      listLoading: true,
      items: [],
      category: '',
      search: '',
      claimedStatus: '',
      tooltipVisible: false,
      tooltipContent: '',
      tooltipStyle: {},
      modalVisible: false,
      modalUser: '',
      modalContact: '',
      sortOrder: 'asc' // 排序方式，默认为升序
    };
  },
  methods: {
    fetchItems() {
      console.log('排序方式值值:', this.sortOrder);
      getItems({
        category: this.category,
        search: this.search.trim(),
        claimed: this.claimedStatus,
        sort: this.sortOrder
      }).then(response => {
        this.items = response.data;
        this.listLoading = false;
      })
        .catch(error => {
          console.error('获取失物列表失败:', error);
        });
    },
    // createFilter(queryString) {
    //   return (items) => {
    //     return _.includes(items.item_name, queryString);
    //   };
    // }
    handleSearch() {
      this.fetchItems();
      this.search = '';
    },
    showDescription(description) {
      this.tooltipVisible = true;
      this.tooltipContent = description || '无描述';
    },
    hideDescription() {
      this.tooltipVisible = false;
    },
    showContactInfo(user, contact) {
      this.modalUser = user;
      this.modalContact = contact || '无';
      this.modalVisible = true;
    },
    closeModal() {
      this.modalVisible = false;
    },
    toggleSortOrder() {
      // 切换排序方式
      this.sortOrder = this.sortOrder === 'asc' ? 'desc' : 'asc';
      this.fetchItems();
    }

  },
  mounted() {
    this.fetchItems();
  }
};
</script>
<style scoped>
/* 整体样式 */
</style>
