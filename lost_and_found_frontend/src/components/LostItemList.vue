<template>
  <div class="lost-items">
    <h2 class="title">失物列表</h2>
    <div class="filters">
      <input
        v-model="search"
        placeholder="搜索失物..."
        @keydown.enter="handleSearch"
        class="input"
      >
      <select v-model="category" @change="fetchItems" class="select">
        <option value="">所有类别</option>
        <option value="雨伞">雨伞</option>
        <option value="眼镜">眼镜</option>
        <option value="3C电子">3C电子</option>
      </select>
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
            <th>编号</th>
            <th>物品名称</th>
            <th>类别</th>
            <th>拾得地点</th>
            <th @click="toggleSortOrder" class="sortable">
              拾得时间
              <span v-if="sortOrder === 'asc'">⬆</span>
              <span v-else>⬇</span>
            </th>
            <th>上传用户</th>
            <th>认领状态</th>
            <th>认领用户</th>
          </tr>
        </thead>
        <tbody>
          <tr 
            v-for="item in items" 
            :key="item.id" 
            @mouseover="showDescription(item.description)" 
            @mouseout="hideDescription"
          >
            <td>{{ item.id }}</td>
            <td>{{ item.item_name }}</td>
            <td>{{ item.category }}</td>
            <td>{{ item.location }}</td>
            <td>{{ item.found_date }}</td>
            <td @click="showContactInfo(item.upload_user, item.contact_info)" class="clickable">
              {{ item.upload_user }}
            </td>
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

    <!-- Tooltip 显示描述 -->
    <div v-if="tooltipVisible" class="tooltip" :style="tooltipStyle">
      {{ tooltipContent }}
    </div>

    <!-- Modal 弹窗显示联系信息 -->
    <div v-if="modalVisible" class="modal">
      <div class="modal-content">
        <span class="close" @click="closeModal">&times;</span>
        <p><strong>上传用户:</strong> {{ modalUser }}</p>
        <p><strong>联系方式:</strong> {{ modalContact }}</p>
      </div>
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
      api.getItems({
        category: this.category,
        search: this.search.trim(),
        claimed: this.claimedStatus,
        sort: this.sortOrder
      })
        .then(response => {
          this.items = response.data;
        })
        .catch(error => {
          console.error('获取失物列表失败:', error);
        });
    },
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
.lost-items {
  max-width: 1000px;
  margin: 20px auto;
  font-family: Arial, sans-serif;
  color: #333;
}
.title {
  text-align: center;
  font-size: 24px;
  margin-bottom: 20px;
  color: #444;
}

/* 滤选样式 */
.filters {
  display: flex;
  justify-content: space-between;
  margin-bottom: 15px;
}
.input, .select {
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 14px;
}

/* 表格样式 */
.table-container {
  max-height: 400px;
  overflow-y: auto;
}
.table {
  width: 100%;
  border-collapse: collapse;
}
.table th, .table td {
  border: 1px solid #ddd;
  padding: 10px;
}
.table th {
  background-color: #f4f4f4;
  font-weight: bold;
  color: #555;
}
.clickable {
  color: blue;
  cursor: pointer;
  text-decoration: underline;
}
.table tbody tr:hover {
  background-color: #f1f1f1;
}

/* Tooltip 样式 */

.tooltip {
  position: absolute;
  background: rgba(50, 50, 50, 0.9); /* 半透明背景 */
  color: #ffffff; /* 白色文字 */
  padding: 10px 20px; /* 更大的内边距 */
  border-radius: 8px; /* 更柔和的圆角 */
  font-size: 16px; /* 增加字体大小 */
  line-height: 1.5; /* 增加行高，便于阅读 */
  box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.25); /* 添加阴影效果 */
  pointer-events: none; /* 禁止鼠标事件 */
  z-index: 1000;
  transform: translate(-50%, -120%); /* 调整位置 */
  animation: fadeIn 0.3s ease-in-out; /* 淡入动画 */
}

/* Tooltip 箭头 */
.tooltip::after {
  content: '';
  position: absolute;
  bottom: -10px;
  left: 50%;
  transform: translateX(-50%);
  border-width: 10px;
  border-style: solid;
  border-color: rgba(50, 50, 50, 0.9) transparent transparent transparent; /* 箭头颜色 */
}
/* Modal 样式 */
.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.8); /* 更暗的背景 */
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1001;
}

.modal-content {
  background: linear-gradient(135deg, #ffffff, #f0f0f0); /* 渐变背景 */
  padding: 30px;
  border-radius: 20px; /* 圆角更大 */
  width: 400px; /* 更宽 */
  text-align: center;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5); /* 更明显的阴影 */
  animation: pop-up 0.3s ease-out; /* 弹出动画 */
  position: relative;
}

.modal-content .close {
  position: absolute;
  top: 15px;
  right: 20px;
  font-size: 24px; /* 字体更大 */
  cursor: pointer;
  color: #555; /* 浅灰色 */
  transition: color 0.3s ease;
}
.modal-content .close:hover {
  color: #000; /* 鼠标悬停时变黑 */
}

.modal-content p {
  margin: 20px 0; /* 更大的间距 */
  font-size: 18px; /* 字体更大 */
  color: #333;
}

.modal-content p strong {
  font-size: 20px; /* 加粗文本更突出 */
  color: #444;
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
/* 弹出动画 */
@keyframes pop-up {
  from {
    transform: scale(0.5);
    opacity: 0;
  }
  to {
    transform: scale(1);
    opacity: 1;
  }
}


/* 可排序表头样式 */
.sortable {
  cursor: pointer;
  color: #007bff;
  font-weight: bold;
}
.sortable:hover {
  text-decoration: underline;
}

</style>


