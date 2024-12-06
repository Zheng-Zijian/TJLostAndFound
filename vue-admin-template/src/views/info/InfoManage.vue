<template>
  <div class="app-container">
    <h2 class="title" style="text-align: center;">管理我的信息</h2>
    <el-button type="primary" @click="showCreateDialog">发布新信息</el-button>
    <el-table :data="infoList" style="width: 100%" v-loading="listLoading">
      <el-table-column prop="title" label="标题" width="180"></el-table-column>
      <el-table-column prop="category" label="分类" width="180"></el-table-column>
      <el-table-column prop="created_at" label="创建时间" width="180"></el-table-column>
      <el-table-column prop="content" label="内容"></el-table-column>
      <el-table-column label="操作" width="180">
        <template slot-scope="scope">
          <el-button size="mini" @click="showEditDialog(scope.row)">编辑</el-button>
          <el-button size="mini" type="danger" @click="deleteInfo(scope.row.id)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <!-- 发布/编辑信息的对话框 -->
    <el-dialog :title="dialogTitle" :visible.sync="dialogVisible">
      <el-form :model="form">
        <el-form-item label="标题">
          <el-input v-model="form.title"></el-input>
        </el-form-item>
        <el-form-item label="分类">
          <el-select v-model="form.category" placeholder="请选择分类">
            <el-option label="丢失物品" value="丢失物品"></el-option>
            <el-option label="捡到物品" value="捡到物品"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="内容">
          <el-input type="textarea" v-model="form.content"></el-input>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="submitForm">确定</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import { fetchUserInfoList, createInfo, updateInfo, deleteInfo } from '@/api/info';

export default {
  data() {
    return {
      infoList: [],
      listLoading: true,
      dialogVisible: false,
      dialogTitle: '',
      form: {
        id: null,
        title: '',
        category: '',
        content: ''
      }
    };
  },
  created() {
    this.getUserInfoList();
  },
  methods: {
    getUserInfoList() {
      this.listLoading = true;
      fetchUserInfoList()
        .then(response => {
          this.infoList = response.data;
          this.listLoading = false;
        })
        .catch(error => {
          console.error('获取用户信息列表失败:', error);
          this.listLoading = false;
        });
    },
    showCreateDialog() {
      this.dialogTitle = '发布新信息';
      this.form = {
        id: null,
        title: '',
        category: '',
        content: ''
      };
      this.dialogVisible = true;
    },
    showEditDialog(row) {
      this.dialogTitle = '编辑信息';
      this.form = { ...row };
      this.dialogVisible = true;
    },
    submitForm() {
      if (this.form.id) {
        updateInfo(this.form)
          .then(() => {
            this.getUserInfoList();
            this.dialogVisible = false;
          })
          .catch(error => {
            console.error('更新信息失败:', error);
          });
      } else {
        createInfo(this.form)
          .then(() => {
            this.getUserInfoList();
            this.dialogVisible = false;
          })
          .catch(error => {
            console.error('发布信息失败:', error);
          });
      }
    },
    deleteInfo(id) {
      deleteInfo(id)
        .then(() => {
          this.getUserInfoList();
        })
        .catch(error => {
          console.error('删除信息失败:', error);
        });
    }
  }
};
</script>

<style scoped>
/* 添加你的样式 */
</style>



  