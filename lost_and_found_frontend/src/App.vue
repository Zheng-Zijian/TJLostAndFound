<template>
  <div id="app">
    <h1>失物招领管理系统</h1>
    <div class="container">
      <!-- 搜索和筛选栏 -->
      <section class="filters">
        <input
          v-model="search"
          placeholder="搜索失物..."
          @input="fetchItems"
          class="search-bar"
        />
        <select v-model="category" @change="fetchItems" class="category-filter">
          <option value="">所有类别</option>
          <option value="雨伞">雨伞</option>
          <option value="眼镜">眼镜</option>
          <option value="3C电子">3C电子</option>
          <option value="其他">其他</option>
        </select>
      </section>

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
      search: ''
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
