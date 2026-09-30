const configuredApiBaseUrl = import.meta.env?.VITE_API_BASE_URL;
const isDevelopment = import.meta.env?.DEV ?? false;
const API_BASE_URL = isDevelopment
    ? ""
    : configuredApiBaseUrl === "same-origin"
        ? ""
        : (configuredApiBaseUrl ?? "http://127.0.0.1:8000");

export function apiUrl(path) {
    return `${API_BASE_URL}${path}`;
}

export async function apiFetch(path, options) {
    const response = await fetch(apiUrl(path), options);

    if (!response.ok) {
        let detail = response.statusText;
        try {
            const body = await response.json();
            if (typeof body.detail === "string") {
                detail = body.detail;
            }
        } catch {
            // Keep the HTTP status message when the server response is not JSON.
        }

        throw new Error(`Request failed (${response.status}): ${detail}`);
    }

    return response;
}
