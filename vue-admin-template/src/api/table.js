import request from '@/utils/request'



export function getItems(params) {
  return request({
    url: '/api/items',
    method: 'get',
    params
  })
}


export function claimItem(itemId, data) {
  return request({
    url: 'api/items/claim',
    method: 'post',
    data,itemId
  })
}



export function addItem(data){
  return request({
    url: '/api/items',
    method: 'post',
    data
  })
}



export function deleteItem(itemId){
  return request({
    url: `/api/items/${itemId}`,
    method: 'delete',
    params: {itemId}
  })
}