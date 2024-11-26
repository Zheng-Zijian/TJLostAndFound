import request from '@/utils/request'

/**
 * 获取信息列表
 * @param {Object} params - 查询条件 { search, category }
 * @returns {Promise}
 */
export function fetchInfoList(params) {
  return request({
    url: '/api/info',
    method: 'get',
    params
  })
}

/**
 * 获取信息详情
 * @param {number} id - 信息 ID
 * @returns {Promise}
 */
export function fetchInfoDetail(id) {
  return request({
    url: `/api/info/${id}`,
    method: 'get'
  })
}

/**
 * 发布新信息
 * @param {Object} data - 信息数据 { title, content, category }
 * @returns {Promise}
 */
export function createInfo(data) {
  return request({
    url: '/api/info',
    method: 'post',
    data
  })
}

/**
 * 编辑信息
 * @param {number} id - 信息 ID
 * @param {Object} data - 修改后的信息数据 { title, content, category }
 * @returns {Promise}
 */
export function updateInfo(id, data) {
  return request({
    url: `/api/info/${id}`,
    method: 'put',
    data
  })
}

/**
 * 删除信息
 * @param {number} id - 信息 ID
 * @returns {Promise}
 */
export function deleteInfo(id) {
  return request({
    url: `/api/info/${id}`,
    method: 'delete'
  })
}
