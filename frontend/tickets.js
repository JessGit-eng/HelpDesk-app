import { apiFetch } from "./api.js";

const tableBody = document.getElementById("tickets-body");

function formatDate(dateValue) {
    if (!dateValue) {
        return "—";
    }

    const [year, month, day] = dateValue.split("-");
    return `${day}-${month}-${year}`;
}

function updateSummaryCards(tickets) {
    document.getElementById("open-count").textContent =
        tickets.filter((ticket) => ticket.status === "open").length;

    document.getElementById("progress-count").textContent =
        tickets.filter((ticket) => ticket.status === "in progress").length;

    document.getElementById("priority-count").textContent =
        tickets.filter((ticket) => ticket.Priority?.toLowerCase() === "high").length;

    document.getElementById("resolved-count").textContent =
        tickets.filter((ticket) => ticket.status === "resolved").length;
}

async function updateStatus(ticketId, status, select) {
    const response = await apiFetch(`/tickets/${ticketId}/status`, {
        method: "PUT",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ status })
    });

    select.value = status;
    window.location.reload();
}

async function loadTickets() {

    const response = await apiFetch("/tickets");

    const tickets = await response.json();

    console.log("Tickets from API:", tickets);

    updateSummaryCards(tickets);

    tickets.forEach((ticket) => {

        const row = `
            <tr>
                <td>
                    <a href="review-ticket.html?id=${ticket.id}">
                        ${ticket.id}
                    </a>
                </td>
                <td>${ticket.title}</td>
                <td>${formatDate(ticket.Date_Created)}</td>
                <td>${ticket.Priority || "—"}</td>
                <td>${ticket.Team || "—"}</td>
                <td>
                    <select class="status-select" data-ticket-id="${ticket.id}">
                        <option value="open" ${ticket.status === "open" ? "selected" : ""}>Open</option>
                        <option value="in progress" ${ticket.status === "in progress" ? "selected" : ""}>In Progress</option>
                        <option value="resolved" ${ticket.status === "resolved" ? "selected" : ""}>Resolved</option>
                    </select>
                </td>
                <td>${formatDate(ticket.Date_Resolved)}</td>
            </tr>
        `;

        tableBody.innerHTML += row;
    });

    document.querySelectorAll(".status-select").forEach((select) => {
        select.addEventListener("change", async (event) => {
            const statusSelect = event.currentTarget;
            const ticketId = statusSelect.dataset.ticketId;

            try {
                await updateStatus(ticketId, statusSelect.value, statusSelect);
            } catch (error) {
                console.error(error);
                window.alert("The ticket status could not be updated.");
            }
        });
    });
}

loadTickets();
