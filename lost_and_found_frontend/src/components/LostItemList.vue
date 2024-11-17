<template>
    <div>
      <h2>失物列表</h2>
      <input v-model="search" placeholder="搜索失物..." @input="fetchItems">
      <select v-model="category" @change="fetchItems">
        <option value="">所有类别</option>
        <option value="雨伞">雨伞</option>
        <option value="眼镜">眼镜</option>
        <option value="3C电子">3C电子</option>
      </select>
      <table>
        <thead>
          <tr>
            <th>编号</th>
            <th>物品名称</th>
            <th>类别</th>
            <th>拾得地点</th>
            <th>认领状态</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in items" :key="item.id">
            <td>{{ item.id }}</td>
            <td>{{ item.item_name }}</td>
            <td>{{ item.category }}</td>
            <td>{{ item.location }}</td>
            <td>{{ item.claimed ? '已认领' : '未认领' }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </template>
  
  <script>
  import api from '../services/api';
  
  export default {
    data() {
      return {
        items: [],
        category: '',
        search: ''
      };
    },
    methods: {
      fetchItems() {
        api.getItems({ category: this.category, search: this.search })
          .then(response => {
            this.items = response.data;
          });
      }
    },
    mounted() {
      this.fetchItems();
    }
  };
  </script>
  