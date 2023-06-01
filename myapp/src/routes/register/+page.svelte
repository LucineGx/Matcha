
<script>
    import toast, { Toaster } from 'svelte-french-toast';
    // import { register } from '../stores/auth.js';
    function register(e) {
      e.preventDefault();
      console.log('register');
      toast.success("It works!")
    }
    let email = '';
    let password = '';
</script>

<!-- Path: myapp/src/routes/register.svelte -->
<h1>Register</h1>
<form on:submit|preventDefault={register}>
    <label for="email">Email</label>
    <input type="email" id="email" bind:value={email} />
    <label for="password">Password</label>
    <input type="password" id="password" bind:value={password} />
    <button type="submit">Register</button>
</form>

<Toaster />