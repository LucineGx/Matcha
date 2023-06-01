<script>
  // import { onMount } from 'svelte';
  // import { io } from 'socket.io-client';

  let messages = ['lol', 'lol2'];
  let messageInput = '';

  // const socket = io('http://127.0.0.1:5000/'); // Replace with your socket server URL

  // onMount(() => {
  //   socket.on('connect', () => {
  //     console.log('Connected to socket server');
  //   });

  //   socket.on('message', (message) => {
  //     messages = [...messages, message];
  //   });

  //   return () => {
  //     socket.disconnect();
  //   };
  // });

  function sendMessage() {
    if (messageInput.trim() !== '') {
      // socket.emit('message', messageInput);
      messageInput = '';
    }
  }
</script>

<main>
  <h1>Chat</h1>

  <div class="message-container">
    {#each messages as message}
      <div class="message">{message}</div>
    {/each}
  </div>

  <div class="input-container">
    <input type="text" bind:value={messageInput} placeholder="Type your message" />

    <button on:click={sendMessage}>Send</button>
  </div>
</main>

<style>
  .message-container {
    height: 300px;
    overflow-y: scroll;
    border: 1px solid #ccc;
    padding: 10px;
  }

  .message {
    margin-bottom: 10px;
  }

  .input-container {
    display: flex;
    margin-top: 10px;
  }

  input {
    flex: 1;
    margin-right: 10px;
  }
</style>
