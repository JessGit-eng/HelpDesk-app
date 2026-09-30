import { apiFetch, apiUrl } from "./api.js";

const params = new URLSearchParams(window.location.search);

const ticketId = params.get("id");

console.log("Selected ticket ID:", ticketId);


async function loadTicket() {

    const response = await apiFetch(`/tickets/${ticketId}`);

    const ticket = await response.json();

    console.log("Ticket from API:", ticket);

    document.getElementById("ticket-heading").textContent =
        `Review Ticket #${ticket.id}`;

    document.getElementById("ticket-title").textContent =
        ticket.title;

    document.getElementById("ticket-description").textContent =
        ticket.description;

    if (ticket.attachment_filename) {
        const attachmentLink = document.getElementById("ticket-attachment");
        attachmentLink.href =
            apiUrl(`/tickets/${ticket.id}/attachment`);
        document.getElementById("ticket-attachment-container").hidden = false;
    }
}


async function loadAIRecommendation() {

    console.log("Starting AI triage...");

    const response = await apiFetch(`/tickets/${ticketId}/triage`, {
        method: "POST"
    });

    const data = await response.json();

    console.log("AI recommendation:", data);

    document.getElementById("ai-priority").textContent =
        data.priority;

    document.getElementById("ai-confidence").textContent =
        data.confidence;

    document.getElementById("ai-reason").textContent =
        data.reason;
}

loadTicket();
loadAIRecommendation();


document.querySelector(".approve-button")
    .addEventListener("click", async () => {

    const priority =
        document.getElementById("ai-priority").textContent;

    const response = await apiFetch(`/tickets/${ticketId}/priority`, {
        method: "PUT",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            priority: priority
        })
    });

    const result = await response.json();

    console.log(result);

    window.location.href = "index.html";
});
