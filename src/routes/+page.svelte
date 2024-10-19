<script>
    import { onMount } from "svelte";
	let loggedIn;
	let data;
	export let grades = []; 
  	let error = null;
	onMount(async() => {
		try {
            const response = await fetch('https://zestful-roseanne-fweah-a96f3f59.koyeb.app/get_login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: new URLSearchParams({
                    loggedIn: loggedIn
                }),
            });
			
            const result = await response.json();
            
            if (result.loggedIn) {
                console.log('Login check successful');
            } else {
                console.log('Login failed');
				window.location.href = '/login';
            }
        } catch (error) {
            console.error('Error during login check:', error);
        }
		
		try {
			const response = await fetch('https://zestful-roseanne-fweah-a96f3f59.koyeb.app/api/grades'); // Replace with your actual API URL
			if (!response.ok) {
				throw new Error('Network response was not ok');
			}
			grades = await response.json(); 
			console.log(grades)
			
	  	} 
	  	catch (err) {
			error = err.message; 
	  	}	

	});
	async function logout(){
		let success;
		try {
            const response = await fetch('https://zestful-roseanne-fweah-a96f3f59.koyeb.app/logout', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: new URLSearchParams({
                    success: success
                }),
            });
            
            const result = await response.json();
            
            if (result.success) {
                console.log('Logout successful');
				window.location.href = '/login'
            } else {
                console.log('Logout failed');
            }
        } catch (error) {
            console.error('Error during logout:', error);
        }
	}
</script>


<h1>Grades</h1>
<div class='container'>
	
	{#if grades.length != 0}
		{#each grades as grade}
		
		<div class="grades-wrapper">
			<div class='grades-container'>
				<h3>{grade[0]}</h3>
				<p>Weight 1,0: <b>{grade[1]}</b></p>
				<p>Weight 0,8: <b>{grade[2]}</b></p>
				<p>Weight 0,6: <b>{grade[3]}</b></p>
				<p>Weight 0,4: <b>{grade[4]}</b></p>
				<p>Weight 0,2: <b>{grade[5]}</b></p>
				<p>Weighted average: <b>{grade[6]}</b></p>
			</div>
		</div>
		{/each}
	{:else}
	<p>Loading...</p>
	{/if}
	<button on:click={logout}>Logout</button>
</div>

<style>
/* Color palette */
:root {
    --dark-bg: #222831;
    --medium-dark: #31363F;
    --accent: #76ABAE;
    --light-text: #EEEEEE;
}

body {
    margin: 0;
    font-family: 'Arial', sans-serif;
    background-color: var(--dark-bg);
    color: var(--light-text);
}

.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 2rem;
}

h1 {
    text-align: center;
    color: var(--accent);
    font-size: 2.5rem;
    margin-bottom: 2rem;
}

/* Change the grades-wrapper to use grid layout */
.grades-wrapper {
    display: grid;
    grid-template-columns: repeat(4, 1fr); /* 4 equal columns */
    gap: 1rem; /* Space between containers */
    justify-content: space-between; /* Distribute space evenly between items */
}

.grades-container {
    background-color: var(--medium-dark);
    padding: 1.5rem;
    border-radius: 8px;
    box-sizing: border-box;
}

h3 {
    color: var(--accent);
    font-size: 1.5rem;
    margin-bottom: 0.5rem;
}

p {
    font-size: 1rem;
    margin: 0.3rem 0;
}

b {
    color: var(--accent);
}

button {
    display: block;
    width: 100%;
    padding: 1rem;
    margin-top: 1.5rem;
    border: none;
    border-radius: 8px;
    background-color: var(--accent);
    color: var(--dark-bg);
    font-size: 1.2rem;
    cursor: pointer;
    transition: background-color 0.3s ease;
}

button:hover {
    background-color: var(--light-text);
    color: var(--dark-bg);
}

p {
    text-align: center;
    color: var(--light-text);
    font-size: 1.2rem;
}
</style>