import Home from "./pages/Home.svelte";
import Result from "./pages/Result.svelte";
import NotFound from "./pages/NotFound.svelte";

export const routes = {
	"/": Home,
	"/result/:filename": Result,
	"*": NotFound,
};
