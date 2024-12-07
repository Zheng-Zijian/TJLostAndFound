import request from '@/utils/request';

/**
 * 获取信息列表
 * @param {Object} params - 查询条件 { search, category }
 * @returns {Promise}
 */
export function fetchInfoList(params) {
  return request({
    url: '/api/info/all',
    method: 'get',
    params:params
  })
}

export function fetchUserInfoList() {
  return request({
    url: '/api/info/user',
    method: 'get'
  });
}

export function createInfo(data) {
  return request({
    url: '/api/info',
    method: 'post',
    data
  });
}

export function updateInfo(data) {
  return request({
    url: `/api/info/${data.id}`,
    method: 'put',
    data
  });
}

export function deleteInfo(id) {
  return request({
    url: `/api/info/${id}`,
    method: 'delete'
  });
}