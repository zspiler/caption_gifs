<script>
	import Router from "svelte-spa-router";
	import { routes } from "./routes.js";
	import { SvelteToast } from "@zerodevx/svelte-toast";
</script>

<main>
	<Router {routes} />
	<SvelteToast options={{ classes: ["log"] }} />
</main>

<style>
	:global(.log.info) {
		--toastBackground: grey;
	}
	:global(.log.warn) {
		--toastBackground: rgb(219, 76, 76);
	}
</style>
