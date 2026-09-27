const form = document.querySelector(".ticket-form");

form.addEventListener("submit", async (event) => {

    event.preventDefault();

    const formData = new FormData(form);

    const response = await fetch(
        "http://127.0.0.1:8000/tickets",
        {
            method: "POST",
            body: formData
        }
    );

    const data = await response.json();

    console.log("Created ticket:", data);
});