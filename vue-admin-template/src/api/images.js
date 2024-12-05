import request from '@/utils/request'
export function uploadImages(formDataInstance) {
  return request({
    url: '/images/upload',
    method: 'post',
    // 不要手动设置 'Content-Type'，Axios 会为 FormData 自动设置
    data: formDataInstance  // 使用 data 属性发送 FormData 对象
  })
}