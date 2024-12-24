// app.js
const userForm = document.getElementById('userForm');

userForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    const name = document.getElementById('name').value;
    const email = document.getElementById('email').value;

    const response = await fetch('/users/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            name: name,
            email: email,
            password: 'defaultPassword',  // Add a default password or ask user for one
        }),
    });

    if (response.ok) {
        alert('User created successfully');
    } else {
        alert('Error creating user');
    }
});
