<script>
	import { toast } from "@zerodevx/svelte-toast";
	import { fade } from "svelte/transition";

	import { push } from "svelte-spa-router";

	import axios from "axios";
	import LoadingAnimation from "../components/LoadingAnimation.svelte";
	import Heading from "../components/Heading.svelte";

	let selectedFiles = [];
	let gif;
	let caption = "";
	let darkBackgroundChecked = false;
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
					dark: darkBackgroundChecked,
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

<Heading />

<form on:submit|preventDefault={() => {}}>
	<div class={!gif ? "center" : ""}>
		<section>
			<p>Select GIF</p>
			<input
				type="file"
				bind:files={selectedFiles}
				accept=".gif"
				on:change={(e) => onFileSelected(e)}
			/>

			{#if gif}
				<div class="gif" in:fade|local>
					<img src={gif} alt="Selected GIF" />
				</div>
			{/if}

			<p>Enter caption</p>

			<input class="caption-input" bind:value={caption} size="50" />

			{#if gif}
				<section class="options" in:fade|local out:fade|local>
					<h3>Options</h3>

					<p>Dark background</p>
					<input type="checkbox" bind:checked={darkBackgroundChecked} />
				</section>
			{/if}
		</section>

		<section>
			<button on:click={submit} disabled={caption.length === 0 || selectedFiles.length === 0}
				>Submit
			</button>
		</section>
	</div>
</form>
{#if loading}
	<LoadingAnimation />
{/if}

<style>
	.caption-input {
		width: 35%;
	}

	@media (max-width: 640px) {
		.caption-input {
			width: 100%;
		}
	}

	.center {
		margin-top: 10%;
	}

	.center p {
		margin-top: 5%;
	}

	.center button {
		margin-top: 5%;
	}

	.gif {
		margin-top: 2%;
	}

	.gif > img {
		max-width: 80%;
	}

	form {
		margin-top: 2%;
	}

	p,
	h3 {
		margin-top: 3%;
	}

	button {
		margin-top: 3%;
	}
</style>
