<script>

	import '../app.css';
</script>

<div class="app">
	

	<main>
		<slot />
	</main>
</div>

<style>
	/* General styling for the app container */
	.app {
		display: flex;
		flex-direction: column;
		min-height: 100vh;
		background-color: #f9f9f9; /* Light background to match the professional theme */
	}

	/* Styling for the main content area */
	main {
		flex: 1;
		display: flex;
		flex-direction: column;
		padding: 1rem;
		width: 100%;
		max-width: 64rem; /* Maximum width for better readability on larger screens */
		margin: 0 auto;
		box-sizing: border-box;
		background-color: #fff; /* White background for the main content area */
		border-radius: 10px; /* Rounded corners for a sleek, modern look */
		box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); /* Subtle shadow effect */
	}

	/* Styling for the footer */
	footer {
		display: flex;
		flex-direction: column;
		justify-content: center;
		align-items: center;
		padding: 12px;
		background-color: #333; /* Dark background for the footer to create contrast */
		color: white; /* White text for good contrast with the dark background */
		font-family: 'Arial', sans-serif; /* Clean and professional font */
	}

	footer a {
		font-weight: bold;
		color: #ff4d4d; /* Bright color for links to make them stand out */
		text-decoration: none;
	}

	footer a:hover {
		color: #e60000; /* Darker red on hover to match the logout button hover effect */
	}

	/* Responsive styling for footer on larger screens */
	@media (min-width: 480px) {
		footer {
			padding: 12px 0;
		}
	}
</style>