<script>
    
    let username = '';
    let password = '';

    export async function handleLogin() {
        try {
            const response = await fetch('http://127.0.0.1:5000/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: new URLSearchParams({
                    username: username,
                    password: password,
                }),
            });
            
            const result = await response.json();
            
            if (result.success) {
                console.log('Login successful');
                window.location.href = '/';
            } else {
                console.log('Login failed');
            }
        } catch (error) {
            console.error('Error during login:', error);
        }
    }
</script>

<svelte:head>
    <title>Login</title>
</svelte:head>

<section>
    <h1>Login</h1>
    <form on:submit|preventDefault={handleLogin}>
        <label for="username">Username</label>
        <input type="text" id="username" name="username" bind:value={username} />
        <label for="password">Password</label>
        <input type="password" id="password" name="password" bind:value={password} />
        <button type="submit">Login</button>
    </form>
</section>

<style>
    section {
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }
</style>