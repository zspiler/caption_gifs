import UploadGif from "./pages/UploadGif.svelte";
import CaptionedGif from "./pages/CaptionedGif.svelte";
import NotFound from "./pages/NotFound.svelte";

export const routes = {
	"/": UploadGif,
	"/result/:filename": CaptionedGif,
	"*": NotFound,
};
