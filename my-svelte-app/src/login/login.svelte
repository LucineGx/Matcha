
<script>
  import toast, { Toaster } from 'svelte-french-toast'
  import {globalCache} from '../resource/cache.js'
  import { navigate } from "svelte-routing"
  let formData = new FormData();
  let user

  function handleInputChange(event) {
    const { name, value } = event.target;
    formData.set(name, value);
  }

  async function handleSubmit() {
    try {
      const response = await globalCache.request('/auth/login', {
        method: 'POST',
        body: formData,
      })
      if (response.status === 200) {
        const data = await response.json()
        user = data
        globalCache.cacheResourceByType("userInfo", data)
        toast.success('Login successful')
        // redirect to userPage
        navigate("/profile", { replace: true })
        // window.location.href = '/user/me'
      } else {
        const error = await response.text()
        toast.error(error)
      }
    } catch (error) {
      toast.error(error.message)
    }
  }
</script>

<form on:submit|preventDefault={handleSubmit}>
  <input type="text" name="username" on:input={handleInputChange} placeholder="Username" />
  <input type="password" name="password" on:input={handleInputChange} placeholder="Password" />
  <button type="submit">Submit</button>
</form>

<Toaster />
