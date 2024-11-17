<template>
  <div>
    <h1>Lost Items</h1>
    <ul>
      <li v-for="item in items" :key="item.id">{{ item.item_name }} - {{ item.location }}</li>
    </ul>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      items: []
    };
  },
  created() {
    axios.get('http://localhost:5000/api/items')
      .then(response => {
        this.items = response.data;
      })
      .catch(error => {
        console.error(error);
      });
  }
}
</script>

