<script>
	import { push } from "svelte-spa-router";
</script>

<h1 on:click={() => push("/")}>Caption GIFs</h1>

<style>
	h1 {
		color: white;
		font-size: 5em;
		font-weight: 100;
		cursor: pointer;
	}
</style>
