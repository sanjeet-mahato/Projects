document.getElementById("uploadBtn").addEventListener("click", async () => {
  const fileInput = document.getElementById("fileInput");
  const status = document.getElementById("status");
  const dashboardBtn = document.getElementById("dashboardBtn");
  const chatBtn = document.getElementById("chatBtn");

  if (!fileInput.files.length) {
    status.textContent = "Please select a file first.";
    return;
  }

  const file = fileInput.files[0];
  const formData = new FormData();
  formData.append("file", file);

  status.textContent = "Uploading...";

  try {
    const response = await fetch("/upload", {
      method: "POST",
      body: formData
    });

    status.textContent = "Loading...";

    const result = await response.json();

    if (result.status === "success") {
      status.textContent = `Upload complete! ${result.total_months} months processed.`;
      dashboardBtn.disabled = false;
      chatBtn.disabled = false;
      dashboardBtn.style.backgroundColor = "#4caf50";
      chatBtn.style.backgroundColor = "#4caf50";

      // Store JSON in sessionStorage if needed for frontend preview
      sessionStorage.setItem("transformedJson", JSON.stringify(result));

    } else {
      status.textContent = "Error: " + result.message;
    }

  } catch (err) {
    console.error(err);
    status.textContent = "Error uploading file.";
  }
});
