document.addEventListener("DOMContentLoaded", () => {
  // -----------------------------
  // Password show/hide toggle
  // -----------------------------
  const toggleBtns = document.querySelectorAll(".toggle-password");
  toggleBtns.forEach(btn => {
    btn.addEventListener("click", () => {
      const input = btn.previousElementSibling;
      if (input.type === "password") {
        input.type = "text";
        btn.textContent = "Hide";
      } else {
        input.type = "password";
        btn.textContent = "Show";
      }
    });
  });

  // -----------------------------
  // OTP countdown timer
  // -----------------------------
  const timerEl = document.getElementById("timer");
  if (timerEl) {
    let seconds = 300; // 5 minutes
    let interval = setInterval(() => {
      if (seconds <= 0) {
        clearInterval(interval);
        timerEl.innerText = "Expired";
      } else {
        let m = String(Math.floor(seconds / 60)).padStart(2, '0');
        let s = String(seconds % 60).padStart(2, '0');
        timerEl.innerText = `${m}:${s}`;
        seconds--;
      }
    }, 1000);
  }

  // -----------------------------
  // Resend OTP button
  // -----------------------------
  const resendBtn = document.getElementById("resendOtpBtn");
  if (resendBtn) {
    resendBtn.addEventListener("click", async () => {
      try {
        const response = await fetch("/resend-otp", {
          method: "POST",
          headers: { "Content-Type": "application/json" }
        });
        const result = await response.json();

        if (result.success) {
          alert("OTP resent successfully! Check your email.");
        } else {
          alert("Failed: " + result.message);
        }
      } catch (err) {
        alert("Error contacting server: " + err.message);
      }
    });
  }
});
