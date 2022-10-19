/**
 * @param {string} url
 * @param {'GET' | 'POST' | 'PUT' | 'DELETE'} [method]
 * @param {FormData} [data]
 */
const pushRequest = async (url, method, data) => {
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
      const body = await res.json()
      console.log('response body', body)
      const user = body
      localStorage.removeItem("userInfo")
      localStorage.setItem("userInfo", JSON.stringify(user))
      return user
    }
  } catch (e) {
    console.error('updateUserInfo:')
    console.error(e)
  }
}

export {
  pushRequest
}