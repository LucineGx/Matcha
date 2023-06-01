
export class Cache {
  loaded
  loading = false
  backendUrl = 'http://127.0.0.1:5000'

  constructor() {
    this.loaded = {}
    this.loadFromLocalStorage()
    // const old = localStorage.getItem('userInfo')
    // if (old) {
    //   this.loaded['userInfo'] = JSON.parse(old)
    // }
  }

  loadFromLocalStorage() {
    for (const key in localStorage) {
      if (localStorage.hasOwnProperty(key)) {
        const element = localStorage[key]
        try {
          this.loaded[key] = JSON.parse(element)
        } catch (error) {
          this.loaded[key] = element
        }
      }
    }
  }

  get count() {
    return this.data.length
  }

  get data() {
    return this.loaded
  }

  /**
   * @param {string} path
   * @param {RequestInit | undefined} options
   * @returns
   */
  async request(path, options) {
    this.loading = true
    try {
      const url = `${this.backendUrl}${path}`
      const response = await fetch(url, options)
      return response
    } catch (error) {
      console.error(error)
      return error
    } finally {
      this.loading = false
    }
  }

  cacheResourceByType(type, data) {
    if (!this.loaded[type]) {
      this.loaded[type] = {}
    }
    this.loaded[type] = data
    localStorage.setItem(type, JSON.stringify(data))
  }
}
const globalCache = new Cache()

export {globalCache}
