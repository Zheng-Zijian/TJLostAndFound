<template>
    <div class="app-container">
      <h2 class="title" style="text-align: center;">认领请求</h2>
  
      <!-- 发送的认领请求 -->
      <el-button type="primary" @click="fetchSentRequests" style="margin-bottom: 20px;">查看我发送的认领请求</el-button>
      <el-table v-loading="sentRequestsLoading" :data="sentRequests" border fit highlight-current-row>
        <el-table-column label="请求编号" width="95">
          <template slot-scope="scope">
            #{{ scope.row.id }} 
          </template>
        </el-table-column>
        <el-table-column label="物品名称" align="center">
          <template slot-scope="scope">
            <span>{{ scope.row.lost_item_id }}</span>
          </template>
        </el-table-column>
        <el-table-column label="状态" align="center">
          <template slot-scope="scope">
            <el-tag :type="scope.row.status | statusFilter">
              {{ scope.row.status === 'pending' ? '待处理' : (scope.row.status==='approved' ? '已同意' : '已拒绝') }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" align="center">
          <template slot-scope="scope">
            <el-button type="danger" size="small" @click="deleteSentRequest(scope.row.id)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
  
      <!-- 收到的认领请求 -->
      <el-button type="primary" @click="fetchReceivedRequests" style="margin-top: 20px;">查看我收到的认领请求</el-button>
      <el-table v-loading="receivedRequestsLoading" :data="receivedRequests" border fit highlight-current-row>
        <el-table-column label="请求编号" width="95">
          <template slot-scope="scope">
            #{{ scope.row.id }}
          </template>
        </el-table-column>
        <el-table-column label="物品名称" align="center">
          <template slot-scope="scope">
            <span>{{ scope.row.lost_item_id }}</span>
          </template>
        </el-table-column>
        <el-table-column label="申请人" align="center">
          <template slot-scope="scope">
            <span>{{ scope.row.claimant_username }}</span>
          </template>
        </el-table-column>
        <el-table-column label="状态" align="center">
          <template slot-scope="scope">
            <el-tag :type="scope.row.status | statusFilter">
              {{ scope.row.status === 'pending' ? '待处理' : (scope.row.status==='approved' ? '已同意' : '已拒绝') }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" align="center">
          <template slot-scope="scope">
            <el-button type="success" size="small" :disabled="scope.row.status !== 'pending'" @click="approveRequest(scope.row.id)">同意</el-button>
            <el-button type="danger" size="small" :disabled="scope.row.status !== 'pending'" @click="rejectRequest(scope.row.id)">拒绝</el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>
  </template>
  
  <script>
  import { getSentRequests, getReceivedRequests, deleteSentRequest, updateRequestStatus } from '@/api/claim-requests'; // 引入API
  import { Message } from 'element-ui';
  
  export default {
    filters: {
    statusFilter(status) {
      if (status === 'pending') {
        return ''
        }
        else if (status === 'approved') {
        return 'success'
        }
        else{
        return 'danger'
        }
      }
    },
  data() {
    return {
      sentRequests: [],
      receivedRequests: [],
      sentRequestsLoading: false,
      receivedRequestsLoading: false,
    };
  },
  methods: {
    // 获取当前用户发送的认领请求
    fetchSentRequests() {
      this.sentRequestsLoading = true;
      getSentRequests()
        .then((response) => {
          this.sentRequests = response.data;
          this.sentRequestsLoading = false;
        })
        .catch((error) => {
          console.error('获取发送的请求失败:', error);
          this.sentRequestsLoading = false;
          Message.error(`获取发送的请求失败: ${error.response ? error.response.data.error : error.message}`);
        });
    },
    // 获取当前用户收到的认领请求
    fetchReceivedRequests() {
      this.receivedRequestsLoading = true;
      getReceivedRequests()
        .then((response) => {
          this.receivedRequests = response.data;
          this.receivedRequestsLoading = false;
        })
        .catch((error) => {
          console.error('获取收到的请求失败:', error);
          this.receivedRequestsLoading = false;
          Message.error(`获取收到的请求失败: ${error.response ? error.response.data.error : error.message}`);
        });
    },
    // 删除发送的认领请求
    deleteSentRequest(requestId) {
      deleteSentRequest(requestId)
        .then((response) => {
          Message.success('删除成功');
          this.fetchSentRequests(); // 刷新请求列表
        })
        .catch((error) => {
          console.error('删除请求失败:', error);
          Message.error('删除失败');
        });
    },
    // 同意认领请求
    approveRequest(requestId) {
      updateRequestStatus(requestId, 'approved')
        .then((response) => {
          Message.success('请求已同意');
          this.fetchReceivedRequests(); // 刷新请求列表
        })
        .catch((error) => {
          console.error('同意请求失败:', error);
          Message.error('同意失败');
        });
    },
    // 拒绝认领请求
    rejectRequest(requestId) {
      updateRequestStatus(requestId, 'rejected')
        .then((response) => {
          Message.success('请求已拒绝');
          this.fetchReceivedRequests(); // 刷新请求列表
        })
        .catch((error) => {
          console.error('拒绝请求失败:', error);
          Message.error('拒绝失败');
        });
    },
  },
  mounted() {
    this.fetchSentRequests();
    this.fetchReceivedRequests();
  },
};

  </script>
  