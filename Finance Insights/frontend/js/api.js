async function apiRequest(path, options = {}) {
    const response = await fetch(
        path,
        {
            ...options,
            credentials: "include",
        }
    );

    const contentType = response.headers.get(
        "content-type"
    );

    const data = contentType?.includes(
        "application/json"
    )
        ? await response.json()
        : null;

    if (!response.ok) {
        throw new Error(
            data?.detail || "Request failed"
        );
    }

    return data;
}