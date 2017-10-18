import request from './request';

export default function apiRequest(path, type, data) {
  const url = `${process.env.REACT_APP_BASE_URL}/${path}`
  const options = {
    method: type,
    headers: {
      'Content-Type': 'application/json'
    },
    body: data ? JSON.stringify(data) : null,
  }
  return request(url, options)
}