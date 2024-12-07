<template>
  <div class="app-container">
    <h2 class="title" style="text-align: center;">认领请求</h2>

    <!-- 发送的认领请求 -->
    <h3 style="text-align: center;">您发送的认领请求</h3>
    <!-- <el-button type="primary" @click="fetchSentRequests" style="margin-bottom: 20px;">刷新</el-button> -->
    <el-table v-loading="sentRequestsLoading" :data="sentRequests" border fit highlight-current-row>
      <el-table-column label="请求编号" width="95" align="center">
        <template slot-scope="scope">
          #{{ scope.row.id }}
        </template>
      </el-table-column>
      <el-table-column label="失物编号" width="95" align="center">
        <template slot-scope="scope">
          #{{ scope.row.lost_item_id }}
        </template>
      </el-table-column>
      <el-table-column label="物品" align="center">
        <template slot-scope="scope">
          <el-button type="text" @click="showDescription(scope.row.description, scope.row.lost_item_id)"> <span style="
            text-decoration: underline;">{{ scope.row.item_name }}</span></el-button>
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
          <el-button type="text" @click="showContactInfo(scope.row.uploader_username, scope.row.uploader_email)"> <span
              style="
            text-decoration: underline;">{{ scope.row.uploader_username }}</span></el-button>
        </template>
      </el-table-column>

      <el-table-column label="状态" align="center">
        <template slot-scope="scope">
          <el-tag :type="scope.row.status | statusFilter">
            {{ scope.row.status === 'pending' ? '待处理' : (scope.row.status === 'approved' ? '已同意' : '已拒绝') }}
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
    <!-- <el-button type="primary" @click="fetchReceivedRequests" style="margin-top: 20px;">查看我收到的认领请求</el-button> -->
    <h3 style="text-align: center;">您收到的认领请求</h3>
    <el-table v-loading="receivedRequestsLoading" :data="receivedRequests" border fit highlight-current-row>
      <el-table-column label="请求编号" width="95" align="center">
        <template slot-scope="scope">
          #{{ scope.row.id }}
        </template>
      </el-table-column>
      <el-table-column label="失物编号" width="95" align="center">
        <template slot-scope="scope">
          #{{ scope.row.lost_item_id }}
        </template>
      </el-table-column>
      <el-table-column label="物品" align="center">
        <template slot-scope="scope">
          <el-button type="text" @click="showDescription(scope.row.description, scope.row.lost_item_id)"> <span style="
            text-decoration: underline;">{{ scope.row.item_name }}</span></el-button>
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
      <el-table-column label="申请认领者" align="center">
        <template slot-scope="scope">
          <el-button type="text" @click="showContactInfo2(scope.row.claimant_username, scope.row.claimant_email)"> <span
              style="
            text-decoration: underline;">{{ scope.row.claimant_username }}</span></el-button>
        </template>
      </el-table-column>
      <el-table-column label="状态" align="center">
        <template slot-scope="scope">
          <el-tag :type="scope.row.status | statusFilter">
            {{ scope.row.status === 'pending' ? '待处理' : (scope.row.status === 'approved' ? '已同意' : '已拒绝') }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作" align="center" width="150">
        <template slot-scope="scope">
          <el-button type="success" size="small" :disabled="scope.row.status !== 'pending'"
            @click="approveRequest(scope.row.id)">同意</el-button>
          <el-button type="danger" size="small" :disabled="scope.row.status !== 'pending'"
            @click="rejectRequest(scope.row.id)">拒绝</el-button>
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
    <el-dialog :visible.sync="modalVisible2" title="申请认领者信息">
      <p><strong>申请用户:</strong> {{ modalUser2 }}</p>
      <p><strong>联系方式:</strong> {{ modalContact2 }}</p>
      <span slot="footer" class="dialog-footer">
        <el-button type="primary" @click="closeModal2">关 闭</el-button>
      </span>
    </el-dialog>

    <!-- 物品描述信息对话框2 -->
    <el-dialog :visible.sync="tooltipVisible" title="物品描述信息">
      <p><strong>物品描述:</strong> {{ tooltipContent }}</p>
      <img :src="image_url" style="width: 100%;">
      <span slot="footer" class="dialog-footer">
        <el-button type="primary" @click="hideDescription">关 闭</el-button>
      </span>
    </el-dialog>
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
      else {
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
      image_url: process.env.VUE_APP_BASE_API + '/images/upload',
      tooltipVisible: false,
      modalVisible: false,
      modalUser: '',
      modalContact: '',
      modalVisible2: false,
      modalUser2: '',
      modalContact2: ''
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
          console.log(response.data, 1)
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
      this.$confirm(
        `是否删除编号为 #${requestId} 的申请？`,
        '确认删除',
        {
          confirmButtonText: '删除',
          cancelButtonText: '取消',
          type: 'warning',
        }
      ).then(() => {
        deleteSentRequest(requestId)
          .then((response) => {
            Message.success('删除成功');
            this.fetchReceivedRequests();
            this.fetchSentRequests(); // 刷新请求列表
          })
          .catch((error) => {
            console.error('删除请求失败:', error);
            Message.error('删除失败');
          });
      })

    },
    // 同意认领请求
    approveRequest(requestId) {
      this.$confirm(
        `是否同意编号为 #${requestId} 的申请？`,
        '确认同意',
        {
          confirmButtonText: '同意',
          cancelButtonText: '取消',
          type: 'warning',
        }).then(() => {
          updateRequestStatus(requestId, 'approved')
            .then((response) => {
              Message.success('请求已同意');
              this.fetchReceivedRequests();
              this.fetchSentRequests(); // 刷新请求列表
            })
            .catch((error) => {
              console.error('同意请求失败:', error);
              Message.error('同意失败');
            });
        })
    },
    // 拒绝认领请求
    rejectRequest(requestId) {
      this.$confirm(
        `是否拒绝编号为 #${requestId} 的申请？`,
        '确认拒绝',
        {
          confirmButtonText: '拒绝',
          cancelButtonText: '取消',
          type: 'warning',
        }).then(() => {
          updateRequestStatus(requestId, 'rejected')
            .then((response) => {
              Message.success('请求已拒绝');
              this.fetchReceivedRequests();
              this.fetchSentRequests(); // 刷新请求列表
            })
            .catch((error) => {
              console.error('拒绝请求失败:', error);
              Message.error('拒绝失败');
            });
        })
    },
    showDescription(description, id) {
      this.tooltipVisible = true;
      this.image_url = process.env.VUE_APP_BASE_API + '/images/get/' + id;
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
    showContactInfo2(user, contact) {
      this.modalUser2 = user;
      this.modalContact2 = contact || '无';
      this.modalVisible2 = true;
    },
    closeModal2() {
      this.modalVisible2 = false;
    }
  },
  mounted() {
    this.fetchSentRequests();
    this.fetchReceivedRequests();
  },
};

</script>