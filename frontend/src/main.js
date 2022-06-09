import App from "./App.svelte";

// Insert URL hash for routing
if (!window.location.hash || window.location.hash == "#") {
	history.replaceState(undefined, undefined, "#/");
}

const app = new App({
	target: document.body,
});

export default app;
