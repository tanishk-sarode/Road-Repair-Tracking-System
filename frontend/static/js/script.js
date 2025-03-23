document.addEventListener("DOMContentLoaded", async function () {
    try {
        const response = await fetch("http://localhost:8080/api/dashboard");  // Backend API
        const data = await response.json();

        document.getElementById("ongoingRepairs").textContent = data.ongoingRepairs;
        document.getElementById("pendingRepairs").textContent = data.pendingRepairs;
        document.getElementById("resources").textContent = data.resources;
        document.getElementById("users").textContent = data.users;
        document.getElementById("residents").textContent = data.residents;
        document.getElementById("supervisors").textContent = data.supervisors;
        document.getElementById("admins").textContent = data.admins;
        document.getElementById("complaints").textContent = data.complaints;
    } catch (error) {
        console.error("Error fetching dashboard data:", error);
    }
});
