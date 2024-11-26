<template>
    <div>
      <el-card>
        <h2>{{ isEditMode ? '编辑信息' : '发布信息' }}</h2>
        <el-form :model="info" label-width="80px">
          <el-form-item label="标题">
            <el-input v-model="info.title" />
          </el-form-item>
          <el-form-item label="分类">
            <el-select v-model="info.category">
              <el-option label="公告" value="announcement" />
              <el-option label="活动" value="event" />
            </el-select>
          </el-form-item>
          <el-form-item label="内容">
            <el-input type="textarea" v-model="info.content" />
          </el-form-item>
          <el-button type="primary" @click="submitInfo">
            {{ isEditMode ? '保存修改' : '发布信息' }}
          </el-button>
        </el-form>
      </el-card>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        info: {
          title: '',
          category: '',
          content: ''
        },
        isEditMode: false // 是否为编辑模式
      };
    },
    created() {
      const id = this.$route.params.id; // 获取路由参数 id
      if (id) {
        this.isEditMode = true;
        this.fetchInfo(id); // 加载信息详情
      }
    },
    methods: {
      fetchInfo(id) {
        // 根据 id 从后端获取信息详情
        this.$http.get(`/api/info/${id}`).then(res => {
          this.info = res.data;
        });
      },
      submitInfo() {
  if (this.isEditMode) {
    // 编辑模式
    this.$http.put(`/api/info/${this.$route.params.id}`, this.info).then(() => {
      this.$message.success('信息更新成功');
      this.$router.push('/info/list');
    });
  } else {
    // 发布模式
    this.$http.post('/api/info', this.info).then(() => {
      this.$message.success('信息发布成功');
      this.$router.push('/info/list');
    }).catch(err => {
      console.error('发布失败:', err);
      this.$message.error('发布信息失败，请重试！');
    });
  }
}

    }
  };
  </script>
  