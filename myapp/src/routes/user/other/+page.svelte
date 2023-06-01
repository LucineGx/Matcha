<script>
  import toast, { Toaster } from 'svelte-french-toast';

  let userProfile = {
    name: 'John Doe',
    age: 25,
    gender: 'Male',
    bio: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit.',
    interests: ['#vegan', '#fitness', '#travel'],
    pictures: [
      'https://example.com/profile-picture1.jpg',
      'https://example.com/profile-picture2.jpg'
    ],
    connected: true,
    liked: true,
    online: true,
    lastConnection: '2023-05-24 10:30:00',
    fakeAccountReported: false,
    blocked: false,
    fame: 100
  };

  function likeUser() {
    if (userProfile.pictures.length > 0) {
      userProfile.liked = !userProfile.liked;
    } else {
      toast.error('You need to upload at least one picture to like this user.')
    }
  }

  function unlikeUser() {
    userProfile.liked = false;
  }

  function disconnectUser() {
    userProfile.connected = false;
  }

  function reportFakeAccount() {
    userProfile.fakeAccountReported = true;
  }

  function blockUser() {
    userProfile.blocked = true;
  }
</script>

<main>
  <h1>{userProfile.name}'s Profile</h1>

  <div class="profile-info">
    <p>Age: {userProfile.age}</p>
    <p>Gender: {userProfile.gender}</p>
    <p>Bio: {userProfile.bio}</p>
    <p>Interests: {userProfile.interests.join(', ')}</p>
    <p>Fame: {userProfile.fame}</p>
    <p>Online: {userProfile.online ? 'Yes' : 'No'}</p>
    {#if !userProfile.online}
      <p>Last Connection: {userProfile.lastConnection}</p>
    {/if}
  </div>

  <div class="profile-actions">
    {#if userProfile.connected}
      <button on:click={disconnectUser}>Disconnect</button>
    {:else if userProfile.liked}
      <button on:click={unlikeUser}>Unlike</button>
    {:else}
      <button on:click={likeUser}>Like</button>
    {/if}

    <button on:click={reportFakeAccount}>Report Fake Account</button>
    <button on:click={blockUser}>Block User</button>
  </div>
</main>

<style>
  .profile-info {
    margin-bottom: 20px;
  }

  .profile-actions button {
    margin-right: 10px;
  }
</style>