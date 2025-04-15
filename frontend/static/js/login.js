function handleLogin(event) {
    event.preventDefault(); // Prevent form submission

    // Example credentials for validation
    const validEmail = "user@example.com";
    const validPassword = "password123";

    // Get input values
    const email = document.getElementById("login-email").value;
    const password = document.getElementById("login-password").value;

    // Check credentials
    if (email === validEmail && password === validPassword) {
        // Redirect to dashboard.html
        window.location.href = "../templates/dashboard.html";
    } else {
        alert("Invalid email or password. Please try again.");
    }
}