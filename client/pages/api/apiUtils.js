/**
 * @param {string} url
 * @param {'GET' | 'POST' | 'PUT' | 'DELETE'} [method]
 * @param {FormData} [data]
 * @param {{isText: boolean}} [options]
 */
const pushRequest = async (url, method, data, options = {isText: false}) => {
  try {
    /** @type {RequestInit} */
    const requestOptions = {
      method: method ??= 'GET',
      credentials: 'include',
      mode: 'cors',
    }
    if (method != 'GET' && data)
      requestOptions.body = data
    const res = await fetch('http://127.0.0.1:5000/' + url, requestOptions)
    if (res.ok) {
      const body = (options.isText === true) ? await res.text() : await res.json()
      console.log(method, url, body)
      return body
    }
  } catch (e) {
    console.error('updateUserInfo:')
    console.error(e)
  }
}

export {
  pushRequest
}