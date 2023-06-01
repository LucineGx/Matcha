<script>
	import { Router, Route, Link } from "svelte-routing"
	import Login  from './login/login.svelte'
	import Home from "./Home.svelte"
	import Profile from "./user/Profile.svelte";
	export let url = ""
</script>

<main>
		<Router url="{url}">
			<nav>
				<Link to="/">Home</Link>
				<Link to="login">Login</Link>
				<Link to="/profile">Profile</Link>
			</nav>
			<div>
				<Route path="/"><Home/></Route>
				<Route path="login" component={Login}/>
				<Route path="profile" component={Profile}/>
			</div>
		</Router>
</main>



<style>
	main {
		text-align: center;
		padding: 1em;
		max-width: 240px;
		margin: 0 auto;
	}

	@media (min-width: 640px) {
		main {
			max-width: none;
		}
	}
</style>