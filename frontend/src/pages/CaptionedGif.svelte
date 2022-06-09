<script>
	import axios from "axios";
	import LoadingAnimation from "../components/LoadingAnimation.svelte";

	export let params = {};
</script>

<main>
	<h1>Your Captioned GIF</h1>

	<div class="gif">
		<img src={`API_URL/captioned/${params.filename}`} alt="Captioned GIF" />
	</div>

	<button>Download</button>
	<a href="#/">Caption another GIF</a>
</main>

<style>
	main {
		text-align: center;
		padding: 1em;
		max-width: 240px;

		margin-left: auto;

		margin: 0 auto 5% auto;
	}

	h1 {
		color: white;

		font-size: 5em;
		font-weight: 100;
	}

	@media (min-width: 640px) {
		main {
			max-width: none;
		}
	}
</style>
