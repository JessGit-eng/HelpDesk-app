import { apiFetch } from "./api.js";

const form = document.querySelector(".ticket-form");

form.addEventListener("submit", async (event) => {
    event.preventDefault();

    const formData = new FormData(form);
    const submitButton = form.querySelector('button[type="submit"]');
    submitButton.disabled = true;

    try {
        const response = await apiFetch("/tickets", {
            method: "POST",
            body: formData
        });

        const data = await response.json();
        console.log("Created ticket:", data);
        window.location.href = "index.html";
    } catch (error) {
        console.error("Unable to create ticket:", error);
        window.alert(`The ticket could not be submitted. ${error.message}`);
        submitButton.disabled = false;
    }
});
