<script>
  /** @param {string} url */
  const navigate = (url) => {
    window.location.href = url
  }

  /** @param {Event} e */
  const login = (e) => {
    e.preventDefault()
    navigate('/login')
  }

  /** @param {Event} e */
  const register = (e) => {
    e.preventDefault();
    navigate('/register')
  }

</script>
<lol>
<!-- make a svelte page with login and register button -->
  <h1>Home</h1>
  <button on:click={() => navigate('/login')}>Login</button>
  <button on:click={() => navigate('/register')}>Register</button>

</lol>


<svelte:head>
    <title>SvelteKit</title>
</svelte:head>

<style>
    lol {
      margin-top: 10vh;
      /* margin-right: auto;
      background-color: grey;
      padding: 15px;
      width: 120px; */
      text-align: center;
    }
    :global(body) {
        font-family: comic sans ms;
        /* width: 30vmax;
        height: 30vmax;
        border: 1px black solid; */
        display: flex;
        justify-content: center;
        align-items: center;
    }
    h1 {
        color: red;
    }

    button {
        background-color: blue;
        color: white;
        padding: 10px;
        border-radius: 5px;
        border: none;
        cursor: pointer;
    }

</style>