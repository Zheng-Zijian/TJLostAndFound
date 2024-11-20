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
    url: `/items/claim/${itemId}`,
    method: 'post',
    data
  })
  }
