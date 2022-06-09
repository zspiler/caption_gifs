<script>
	import axios from "axios";
	import LoadingAnimation from "./components/LoadingAnimation.svelte";

	let selectedFiles;
	let gif;
	let caption;
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
		// TODO: validate file selected, text not

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
			console.log(filename);
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
		} catch (error) {
			console.log(error);
		}
	}
</script>

<main>
	<h1>Caption GIFs</h1>

	<input
		type="file"
		bind:files={selectedFiles}
		accept=".gif"
		on:change={(e) => onFileSelected(e)}
	/>

	{#if gif}
		<div class="gif">
			<img src={gif} alt="Selected GIF" />
		</div>
	{/if}

	<p>Enter caption:</p>
	<input bind:value={caption} />

	<button on:click={submit}>Submit </button>

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
