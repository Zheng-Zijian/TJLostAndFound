import request from '@/utils/request'

// 获取所有失物列表
export function getItems(params) {
  return request({
    url: '/api/items',
    method: 'get',
    params
  })
}

// 用户认领失物
export function claimItem(itemId, data) {
  return request({
    url: '/api/items/claim',
    method: 'post',
    data
  })
}

// 获取失物认领请求列表
export function getClaimRequests(itemId) {
  return request({
    url: `/api/items/claims/${itemId}`,
    method: 'get'
  })
}

// 上传者批准某个认领请求
export function approveClaim(itemId, claimId) {
  return request({
    url: `/api/items/approve_claim/${itemId}/${claimId}`,
    method: 'post'
  })
}
