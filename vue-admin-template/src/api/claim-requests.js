import request from '@/utils/request';

// 获取当前用户发送的认领请求
export function getSentRequests() {
  return request({
    url: '/api/claim-requests/sent',
    method: 'get',
  });
}

// 获取当前用户收到的认领请求
export function getReceivedRequests() {
  return request({
    url: '/api/claim-requests/received',
    method: 'get',
  })
  .catch((error) => {
    console.error('请求失败:', error);
    throw error; // 抛出异常以便外部处理
  });
}


export function deleteSentRequest(requestId) {
  return request({
    url: `/api/claim-requests/${requestId}`,
    method: 'delete',
  });
}



export function updateRequestStatus(requestId, data) {
  return request({
    url: `/api/claim-requests/${requestId}/update`,
    method: 'patch',
    data:{
        'status': data
    }
  });
}
