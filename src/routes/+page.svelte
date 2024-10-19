<script>
    import { onMount, onDestroy } from "svelte";
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
            if (grades.success == 'false'){
                alert("User not logged in")
            }
			console.log(grades)
			
	  	} 
	  	catch (err) {
			error = err.message; 
	  	}	
        const handleBeforeUnload = (event) => {
                logout();
        };
        window.addEventListener('beforeunload', handleBeforeUnload);
        onDestroy(() => {
            window.removeEventListener('beforeunload', handleBeforeUnload);
        });
	});
	async function logout(){
		let success;
	
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
            window.location.replace('/login') ;
        } else {
            console.log('Logout failed');
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
</div>

<style>
    h1 {
        text-align: center;
        color: #333;
        font-family: 'Arial', sans-serif;
        margin-bottom: 20px;
    }

    .container {
        display: flex;
        flex-direction: column;
        align-items: center;
        padding: 20px;
        background-color: #f9f9f9;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }

    .grades-wrapper {
        width: 100%;
        max-width: 600px;
        background-color: #fff;
        padding: 15px;
        margin-bottom: 20px;
        border-radius: 8px;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
        transition: transform 0.2s ease-in-out;
    }

    .grades-wrapper:hover {
        transform: translateY(-5px);
    }

    .grades-container {
        text-align: left;
        font-family: 'Arial', sans-serif;
    }

    h3 {
        color: #444;
        font-size: 1.2em;
        margin-bottom: 10px;
    }

    p {
        margin: 5px 0;
        font-size: 1em;
        color: #666;
    }

    b {
        color: #333;
    }

    .logout-btn {
        padding: 10px 20px;
        background-color: #ff4d4d;
        color: white;
        border: none;
        border-radius: 5px;
        font-size: 1em;
        cursor: pointer;
        transition: background-color 0.3s ease;
    }

    .logout-btn:hover {
        background-color: #e60000;
    }
</style>