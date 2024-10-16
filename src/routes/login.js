import { writable } from 'svelte/store';
let username = '';
let password = '';
export const loginStore = writable(false);
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
            loginStore.set(true);
            window.location.replace("/protected")
        } else {
            console.log('Login failed');
            
        }
    } catch (error) {
        console.error('Error during login:', error);
    }
}
export function logout() {
    loginStore.set(false);
}