import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:5000/api'
});

export default {
  getItems(params) {
    return api.get('/items', { params });
  },
  addItem(data) {
    return api.post('/items', data);
  },
  claimItem(itemId, data) {
    return api.post(`/items/claim/${itemId}`, data);
  }
};


