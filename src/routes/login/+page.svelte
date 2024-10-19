<script>
    
    let username = '';
    let password = '';

    export async function handleLogin() {
        try {
            const response = await fetch('https://zestful-roseanne-fweah-a96f3f59.koyeb.app/login', {
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
    /* Center the form within the section */
    section {
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        min-height: 100vh;
        background-color: #f9f9f9; /* Light background to match the theme */
        padding: 20px;
    }

    /* Styling for the login form */
    form {
        display: flex;
        flex-direction: column;
        width: 100%;
        max-width: 400px; /* Max width for better readability */
        background-color: #fff; /* White background for form */
        padding: 30px;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); /* Subtle shadow for a clean look */
    }

    h1 {
        text-align: center;
        margin-bottom: 20px;
        color: #333;
        font-family: 'Arial', sans-serif;
    }

    /* Input fields */
    label {
        margin-bottom: 8px;
        font-size: 1rem;
        color: #666;
    }

    input {
        margin-bottom: 20px;
        padding: 10px;
        border: 1px solid #ccc;
        border-radius: 5px;
        font-size: 1rem;
        box-sizing: border-box;
    }

    /* Button styling */
    button {
        padding: 12px;
        background-color: #ff4d4d; /* Bright red button */
        color: white;
        border: none;
        border-radius: 5px;
        font-size: 1rem;
        cursor: pointer;
        transition: background-color 0.3s ease;
    }

    button:hover {
        background-color: #e60000; /* Darker red on hover */
    }

    /* Responsive design */
    @media (min-width: 480px) {
        form {
            padding: 40px;
        }

        button {
            font-size: 1.1rem;
        }
    }
</style>