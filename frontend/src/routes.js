import UploadGif from "./pages/UploadGif.svelte";
import NotFound from "./pages/NotFound.svelte";

export const routes = {
	"/": UploadGif,
	"*": NotFound,
};
