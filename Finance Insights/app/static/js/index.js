window.addEventListener("DOMContentLoaded", () => {
    const avatar = document.getElementById("profileAvatar");
    const profileNameEl = document.querySelector(".profile-name");
    const dropdown = document.getElementById("profileDropdown");

    // Fetch current user details from session
    fetch("/current-user")
        .then(res => res.json())
        .then(data => {
            if (data.status === "success") {
                const name = data.profile_name || "User";
                profileNameEl.textContent = name;
                // Compute initials
                const initials = name.split(" ").map(n => n[0].toUpperCase()).join("").substring(0, 2);
                avatar.textContent = initials;
            }
        })
        .catch(err => console.error("Failed to fetch user details:", err));

    // Toggle dropdown
    avatar.addEventListener("click", (e) => {
        e.stopPropagation();
        dropdown.style.display = dropdown.style.display === "block" ? "none" : "block";
    });

    // Logout with browser alert
    document.getElementById("logout").addEventListener("click", () => {
        fetch("/logout")
            .then(() => {
                alert("You have been logged out successfully.");
                window.location.href = "/login";
            })
            .catch(err => console.error("Logout failed:", err));
    });

    // Close dropdown on outside click
    document.addEventListener("click", (e) => {
        if (!avatar.contains(e.target) && !dropdown.contains(e.target)) {
            dropdown.style.display = "none";
        }
    });
});

// Upload functionality
function uploadFile() {
    const fileInput = document.getElementById("excelFile");
    const statusMsg = document.getElementById("statusMsg");
    const viewBtn = document.getElementById("viewDashboard");
    const chatBtn = document.getElementById("chatBot");

    if (!fileInput.files.length) {
        statusMsg.textContent = "Please select a file!";
        return;
    }

    const file = fileInput.files[0];
    const formData = new FormData();
    formData.append("file", file);

    statusMsg.textContent = "Uploading...";
    viewBtn.disabled = true;
    chatBtn.disabled = true;

    fetch("/upload", { method: "POST", body: formData })
        .then(res => res.json())
        .then(data => {
            if (data.status === "success") {
                statusMsg.textContent = "Upload and analysis complete!";
                viewBtn.disabled = false;
                chatBtn.disabled = false;
            } else {
                statusMsg.textContent = "Error: " + data.message;
            }
        })
        .catch(err => {
            statusMsg.textContent = "Upload failed. Try again.";
            console.error(err);
        });
}
