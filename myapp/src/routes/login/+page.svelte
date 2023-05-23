<script>
    // import { login } from '../stores/auth.js';
    function login(e) {
      e.preventDefault()
      console.log('login')
    }
    let email = ''
    let password = ''
</script>

<!-- Path: myapp/src/routes/login.svelte -->
<h1>Login</h1>
<form on:submit|preventDefault={login}>
    <label for="email">Email</label>
    <input type="email" id="email" bind:value={email} />
    <label for="password">Password</label>
    <input type="password" id="password" bind:value={password} />
    <button type="submit">Login</button>
</form>