<script>
	import { toast } from "@zerodevx/svelte-toast";
	import { fade } from "svelte/transition";

	import { push } from "svelte-spa-router";

	import axios from "axios";
	import LoadingAnimation from "../components/LoadingAnimation.svelte";

	let selectedFiles = [];
	let gif;
	let caption = "";

	let loading;

	function onFileSelected(e) {
		let image = e.target.files[0];
		let reader = new FileReader();
		reader.readAsDataURL(image);
		reader.onload = (e) => {
			gif = e.target.result;
		};
	}

	async function submit() {
		if (selectedFiles.length === 0) {
			return toast.push("Please select a GIF", { classes: ["info"] });
		}
		const fileSize = selectedFiles[0].size / 1000000;
		if (fileSize > 20) {
			return toast.push(
				"Selected GIF exceeds 20 MB size limit. Please select a different GIF",
				{ classes: ["info"] }
			);
		}

		if (caption.length === 0) {
			return toast.push("Please enter some text for the caption", { classes: ["info"] });
		}

		loading = true;
		var formData = new FormData();
		formData.append("file", selectedFiles[0]);

		try {
			let res = await axios.post("API_URL/upload", formData, {
				headers: {
					"Content-Type": "multipart/form-data",
				},
			});
			const filename = res.data.filename;
			res = await axios.post(
				"API_URL/caption",
				{
					filename,
					text: caption,
				},
				{ filename, text: caption },
				{
					headers: {
						"Content-Type": "application/json",
					},
				}
			);
			loading = false;
			push(`/result/${res.data.filename}`);
		} catch (error) {
			loading = false;
			toast.push("Server error", { classes: ["warn"] });
		}
	}
</script>

<main>
	<h1>Caption GIFs</h1>

	<form on:submit|preventDefault={() => {}}>
		<input
			type="file"
			bind:files={selectedFiles}
			accept=".gif"
			on:change={(e) => onFileSelected(e)}
		/>

		{#if gif}
			<div class="gif" in:fade>
				<img src={gif} alt="Selected GIF" />
			</div>
		{/if}

		<p>Enter caption:</p>
		<input bind:value={caption} />

		<br />
		<button on:click={submit} disabled={caption.length === 0 || selectedFiles.length === 0}
			>Submit
		</button>
	</form>
	{#if loading}
		<LoadingAnimation />
	{/if}
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
