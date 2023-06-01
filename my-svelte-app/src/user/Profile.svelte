<script>

  import { globalCache } from '../resource/cache.js'
  const user = globalCache?.loaded?.userInfo
  const emptyUser = {
    age: null,
    created_on: null,
    first_name: '',
    gender: '',
    id: null,
    last_name: '',
    lat: null,
    lon: null,
    public_popularity: null,
    search_female: null,
    search_male : null,
    search_other: null,
    short_bio: '',
    username: ''
  }
  if (!user) {
    // navigate("/login", { replace: true })
  }

  // all of this is part of the info login returns
  let {
    age,
    created_on,
    first_name,
    gender,
    id,
    last_name,
    lat,
    lon,
    public_popularity,
    search_female,
    search_male,
    search_other,
    short_bio,
    username
  } = user || emptyUser

  let needChange = false

  if (!created_on || !age || !gender) {
    needChange = true
  }

  let custom_localisation
  let email
  /** @type {string | ArrayBuffer | null | any } */
  let pictures
  /** @type {string | ArrayBuffer | null} */
  let profilePicture

  let currentPicture

  /**
	 * @param {{ target: { files: any[]; }; }} event
	 */
  function addPicture(event) {
    const file = event.target.files[0]
    const reader = new FileReader()

    reader.onload = () => {
      const pictureUrl = reader.result
      pictures = [...pictures, pictureUrl]
      if (pictures?.length === 1) {
        profilePicture = pictureUrl
      }
    };

    if (file) {
      reader.readAsDataURL(file)
    }
  }

  function removePicture(index) {
    pictures.splice(index, 1)
    if (profilePicture === pictures[index]) {
      profilePicture = pictures[0]
    }
  }

  function saveProfile() {
    // Here you can perform the logic to save the user profile
    // You can access the form data: gender, sexualPreferences, biography, interests, profilePicture
  }

  function sexualPreferences() {
    let kindOfHuman = ''
    if (search_female === 1) {
      kindOfHuman = '♂️'
    }
    if (search_male === 1) {
      kindOfHuman += '♀️'
    }
    if (search_other === 1) {
      kindOfHuman += '🌈'
    }
    return (`
      <div>
        search for: ${kindOfHuman}
      </div>
    `)
  }

  let  avatar, fileinput;

	const onFileSelected =(e)=>{
  let image = e.target.files[0];
            let reader = new FileReader();
            reader.readAsDataURL(image);
            reader.onload = e => {
                 avatar = e.target.result
            };
}
</script>

<main>
  <h1>User Profile</h1>

  <button on:click={() => console.log(globalCache.data)}>lol</button>
  <button on:click={() => needChange = !needChange}>update profile</button>


  {#if currentPicture}
    <img src={currentPicture} alt="imagedemoi" />
  {/if}
  {#if needChange}
    <form on:submit|preventDefault={saveProfile}>


      {#if avatar}
        <img class="avatar" src="{avatar}" alt="d" />
        {:else}
        <img class="avatar" src="https://cdn4.iconfinder.com/data/icons/small-n-flat/24/user-alt-512.png" alt="" />
      {/if}
				<img class="upload" src="https://static.thenounproject.com/png/625182-200.png" alt="" on:click={()=>{fileinput.click();}} />
        <div class="chan" on:click={()=>{fileinput.click();}}>Choose Image</div>
        <input style="display:none" type="file" accept=".jpg, .jpeg, .png" on:change={(e)=>onFileSelected(e)} bind:this={fileinput} >

      <label for="firstName">first_name:</label>
      <input type="text" id="firstName" bind:value={first_name} />

      <label for="lastName">last_name:</label>
      <input type="text" id="lastName" bind:value={last_name} />

      <label for="age">Age:</label>
      <input type="number" id="age" bind:value={age} />

      <label for="userName">user name:</label>
      <input type="text" id="userName" bind:value={username} />

      <label for="biography">Biography:</label>
      <textarea id="biography" bind:value={short_bio} />

      <label for="gender">Gender:</label>
      <select id="gender" bind:value={gender}>
        <option value="male">Male</option>
        <option value="female">Female</option>
        <option value="other">Other</option>
      </select>

      <label for="localisation">localisation:</label>
      <input type="text" id="localisation" bind:value={custom_localisation} />


      <div style="display: flex;">
        <label for="search">search:</label>

        <div style="display: flex; padding:1vmin">
          <label for="likeMale">male:</label>
          <select id="ilikedicks" bind:value={search_male}>
            <option value="likemale">yes</option>
            <option value="donotlikemale">no</option>
          </select>
        </div>

        <div style="display: flex; padding:1vmin">
          <label for="likefemale">female:</label>
          <select id="ilikepuss" bind:value={search_female}>
            <option value="likefemale">yes</option>
            <option value="donotlikefemale">no</option>
          </select>
        </div>

        <div style="display: flex; padding:1vmin">
          <label for="likeother">other:</label>
          <select id="ilikeother" bind:value={search_other}>
            <option value="likeother">yes</option>
            <option value="donotlikeother">no</option>
          </select>
        </div>

      </div>

      <!-- <label for="biography">Biography:</label> -->
      <!-- <textarea id="biography" bind:value={short_bio} rows="4"></textarea> -->

      <!-- <label for="interests">Interests (tags):</label>
      <input type="text" id="interests" bind:value={tags} /> -->

      <!-- <label for="pictures">Pictures:</label> -->
      <!-- <input type="file" id="pictures" accept="image/*" onchange={addPicture} /> -->

      <!-- <div> -->
        <!-- {#each pictures as picture, index} -->
          <!-- <div> -->
            <!-- <img src={picture} alt="Profile Picture" /> -->
            <!-- {#if picture === profilePicture} -->
              <!-- <span>Profile Picture</span> -->
            <!-- {/if} -->
            <!-- <button on:click={() => removePicture(index)}>Remove</button> -->
          <!-- </div> -->
        <!-- {/each} -->
      <!-- </div> -->

      <button type="submit">Save Profile</button>
    </form>
  {/if}

  {#if needChange === false}
  <div>
    <!-- let's print every info from user -->
    <p>age: {age}</p>
    <p>created_on: {created_on}</p>
    <p>first_name: {first_name}</p>
    <p>gender: {gender}</p>
    <p>id: {id}</p>
    <p>last_name: {last_name}</p>
    <p>lat: {lat}</p>
    <p>lon: {lon}</p>
    <p>public_popularity: {public_popularity}</p>
    <p>search_female: {search_female}</p>
    <p>search_male: {search_male}</p>
    <p>search_other: {search_other}</p>
    <p>short_bio: {short_bio}</p>
    <p>username: {username}</p>
  </div>
  {/if}


</main>

<style>
	#app{
	display:flex;
		align-items:center;
		justify-content:center;
		flex-flow:column;
}

	.upload{
		display:flex;
	height:50px;
		width:50px;
		cursor:pointer;
	}
	.avatar{
		display:flex;
		height:200px;
		width:200px;
	}
</style>