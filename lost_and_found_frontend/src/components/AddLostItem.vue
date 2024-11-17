<template>
    <div>
      <h2>发布失物</h2>
      <form @submit.prevent="submitItem">
        <input v-model="item_name" placeholder="物品名称" required>
        <input v-model="location" placeholder="拾得地点" required>
        <textarea v-model="description" placeholder="描述"></textarea>
        <button type="submit">发布</button>
      </form>
    </div>
  </template>
  
  <script>
  import api from '../services/api';
  
  export default {
    data() {
      return {
        item_name: '',
        location: '',
        description: '',
        contact_info: ''
      };
    },
    methods: {
      submitItem() {
        api.addItem({
          item_name: this.item_name,
          location: this.location,
          description: this.description,
          contact_info: this.contact_info
        }).then(() => {
          alert('失物信息已发布');
          this.item_name = '';
          this.location = '';
          this.description = '';
          this.contact_info = '';
        });
      }
    }
  };
  </script>
  