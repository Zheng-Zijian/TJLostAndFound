<template>
  <div class="lost-items">
    <h2 class="title">失物列表</h2>
    <div class="filters">
      <!-- 搜索框 -->
      <input
        v-model="search"
        placeholder="搜索失物..."
        @keydown.enter="handleSearch"
        class="input"
      >

      <!-- 类别筛选下拉框 -->
      <select v-model="category" @change="fetchItems" class="select">
        <option value="">所有类别</option>
        <option value="雨伞">雨伞</option>
        <option value="眼镜">眼镜</option>
        <option value="3C电子">3C电子</option>
      </select>

      <!-- 认领状态筛选下拉框 -->
      <select v-model="claimedStatus" @change="fetchItems" class="select">
        <option value="">全部</option>
        <option value="claimed">已认领</option>
        <option value="unclaimed">未认领</option>
      </select>
    </div>
    <div class="table-container">
      <table class="table">
        <thead>
          <tr>
            <th style="width: 5%;">编号</th>
            <th style="width: 20%;">物品名称</th>
            <th style="width: 15%;">类别</th>
            <th style="width: 25%;">拾得地点</th>
            <th style="width: 15%;">上传用户</th>
            <th style="width: 10%;">认领状态</th>
            <th style="width: 10%;">认领用户</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in items" :key="item.id">
            <td>{{ item.id }}</td>
            <td>{{ item.item_name }}</td>
            <td>{{ item.category }}</td>
            <td>{{ item.location }}</td>
            <td>{{ item.upload_user }}</td>
            <td>
              <span :class="{ claimed: item.claimed, unclaimed: !item.claimed }">
                {{ item.claimed ? '✔' : '✘' }}
              </span>
            </td>
            <td>{{ item.claimed_user || '无' }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import api from '../services/api';

export default {
  data() {
    return {
      items: [],
      category: '',
      search: '',
      claimedStatus: '' // 新增字段用于筛选认领状态
    };
  },
  methods: {
    fetchItems() {
      // 将认领状态作为查询参数传递到后端
      api.getItems({
        category: this.category,
        search: this.search.trim(),
        claimed: this.claimedStatus // 新增筛选条件
      })
        .then(response => {
          this.items = response.data;
        })
        .catch(error => {
          console.error('获取失物列表失败:', error);
        });
    },
    handleSearch() {
      this.fetchItems(); // 搜索
      this.search = ''; // 清空搜索框
    }
  },
  mounted() {
    this.fetchItems(); // 页面加载时获取数据
  }
};
</script>


<style scoped>
/* 整体布局 */
.lost-items {
  max-width: 1000px;
  margin: 20px auto;
  font-family: Arial, sans-serif;
  color: #333;
}

/* 标题 */
.title {
  text-align: center;
  font-size: 24px;
  margin-bottom: 20px;
  color: #444;
}

/* 过滤选项 */
.filters {
  display: flex;
  justify-content: space-between;
  margin-bottom: 15px;
}

.input {
  flex: 1;
  margin-right: 10px;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 14px;
}

.select {
  flex: 0.4;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 14px;
}

/* 表格样式 */
.table-container {
  max-height: 400px;
  overflow-y: auto;
  border: 1px solid #ddd;
}

.table {
  width: 100%;
  border-collapse: collapse;
}

.table th,
.table td {
  border: 1px solid #ddd;
  text-align: left;
  padding: 10px;
}

.table th {
  background-color: #f4f4f4;
  font-weight: bold;
  color: #555;
}

.table tbody tr:nth-child(odd) {
  background-color: #f9f9f9;
}

.table tbody tr:nth-child(even) {
  background-color: #ffffff;
}

.table tbody tr:hover {
  background-color: #f1f1f1;
}

/* 认领状态样式 */
.claimed {
  color: green;
  font-size: 16px;
  font-weight: bold;
}

.unclaimed {
  color: red;
  font-size: 16px;
  font-weight: bold;
}
</style>
