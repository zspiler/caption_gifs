<script>
	import { onMount } from "svelte";
	import { fade } from "svelte/transition";
	import { push } from "svelte-spa-router";

	import axios from "axios";
	import LoadingAnimation from "../components/LoadingAnimation.svelte";
	import Heading from "../components/Heading.svelte";

	export let params = {};

	let gifFile;
	let loading = true;

	onMount(async () => {
		try {
			const res = await axios.get(`API_URL/captioned/${params.filename}`);
			gifFile = res.data;
			loading = false;
		} catch (error) {
			loading = false;
		}
	});
</script>

<Heading />

{#if !loading}
	<h2>Result</h2>
	{#if gifFile}
		<div class="gif" in:fade|local>
			<img src={`API_URL/captioned/${params.filename}`} loop="infinite" alt="Captioned GIF" />
		</div>
		<br />

		<button on:click={() => window.open(`API_URL/captioned/${params.filename}`, "Download")}>
			Download
		</button>
		<br />
		<button on:click={() => push("/")}>Upload another GIF</button>
	{:else}
		<div class="center">
			<h3>Cannot find GIF '{params.filename}'.</h3>
			<h4>GIFs are available for 24 hours after creation.</h4>

			<button on:click={() => push("/")}>Upload another GIF</button>
		</div>
	{/if}
{/if}

{#if loading}
	<LoadingAnimation />
{/if}

<style>
	.center {
		margin-top: 5%;
		margin-bottom: 5%;
		left: 0;
		line-height: 50px;
		margin-top: -100px;
		position: absolute;
		text-align: center;
		top: 50%;
		width: 100%;
	}
	.gif {
		margin-top: 2%;
	}

	.gif > img {
		max-width: 80%;
	}

	h3 {
		color: rgb(77, 77, 77);
		font-weight: 100;
		font-size: 2em;
	}

	h4 {
		color: rgb(77, 77, 77);
		font-weight: 100;
		font-size: 1.5em;
	}

	button {
		margin-top: 1%;
	}
</style>
