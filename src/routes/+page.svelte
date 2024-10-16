<script>
    import { onMount } from 'svelte';
    import { writable } from 'svelte/store';
    import { goto } from '@sveltejs/kit/navigation';
    import { loginStore } from './login.svelte'; // Import the store

    let isLoggedIn = false;

    // Subscribe to the loginStore to check login status
    loginStore.subscribe(value => {
        isLoggedIn = value;
    });

    onMount(() => {
        if (!isLoggedIn) {
            goto('/login'); // Redirect to login page if not logged in
        }
    });
</script>

{#if isLoggedIn}
    <h1>Welcome to the protected page!</h1>
    <!-- Your protected content goes here -->
{:else}
    <p>Redirecting to login...</p>
{/if}

<style>
	section {
		display: flex;
		flex-direction: column;
		justify-content: center;
		align-items: center;
		flex: 0.6;
	}

	h1 {
		width: 100%;
	}

	.welcome {
		display: block;
		position: relative;
		width: 100%;
		height: 0;
		padding: 0 0 calc(100% * 495 / 2048) 0;
	}

	.welcome img {
		position: absolute;
		width: 100%;
		height: 100%;
		top: 0;
		display: block;
	}
</style>
