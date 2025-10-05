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
