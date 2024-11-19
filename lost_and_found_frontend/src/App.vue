<template>
  <div id="app">
    <h1>失物招领管理系统</h1>
    <div class="container">


      <!-- 显示失物列表 -->
      <LostItemList :items="items" />
    </div>
  </div>
</template>

<script>
import LostItemList from './components/LostItemList.vue';
import api from './services/api';

export default {
  components: {
    LostItemList
  },
  data() {
    return {
      items: [],
      category: '',
      search: '',
    };
  },
  methods: {
    // 获取失物列表
    fetchItems() {
      api.getItems({ category: this.category, search: this.search })
        .then(response => {
          this.items = response.data;
        })
        .catch(error => {
          console.error('获取失物列表失败:', error);
        });
    }
  },
  mounted() {
    // 组件加载时获取失物列表
    this.fetchItems();
  }
};
</script>

<style>
#app {
  text-align: center;
  margin-top: 20px;
}

.container {
  width: 80%;
  margin: auto;
}

.search-bar {
  padding: 8px;
  width: 60%;
  margin-right: 10px;
}

.category-filter {
  padding: 8px;
  margin-left: 10px;
}
</style>

<style>
/* 整体页面样式 */
body {
  margin: 0;
  padding: 0;
  font-family: Arial, sans-serif;
  background: linear-gradient(-45deg, #ff9a9e, #fad0c4, #fbc2eb, #a18cd1); /* 初始背景 */
  background-size: 400% 400%; /* 背景尺寸大于视口，便于动画平滑过渡 */
  animation: gradientAnimation 15s ease infinite; /* 动态背景动画 */
  min-height: 100vh; /* 保证背景覆盖整个视口 */
  display: flex;
  justify-content: center;
  align-items: center;
}

/* 动态渐变动画 */
@keyframes gradientAnimation {
  0% {
    background-position: 0% 50%; /* 起始位置 */
  }
  50% {
    background-position: 100% 50%; /* 中间位置 */
  }
  100% {
    background-position: 0% 50%; /* 结束回到起始位置 */
  }
}

/* 应用主容器 */
#app {
  text-align: center;
  background: #fff; /* 白色背景，增加对比度 */
  padding: 20px;
  border-radius: 10px; /* 圆角效果 */
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); /* 阴影效果 */
  width: 80%;
  max-width: 1200px;
  margin: auto;
}

/* 标题样式 */
h1 {
  color: #333;
  font-size: 2rem;
  margin-bottom: 20px;
}

/* 容器样式 */
.container {
  width: 100%;
}

/* 搜索栏 */
.search-bar {
  padding: 8px;
  width: 60%;
  margin-right: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

/* 筛选栏 */
.category-filter {
  padding: 8px;
  margin-left: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
}
</style>
