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
  // Form validation and UX
  // -----------------------------
  document.querySelectorAll("form").forEach(form => {
    form.addEventListener("submit", e => {
      let valid = true;
      let errorMsg = "";
      form.querySelectorAll("input[required]").forEach(input => {
        if (!input.value.trim()) {
          valid = false;
          errorMsg = "All fields are required.";
        }
      });
      if (!valid) {
        e.preventDefault();
        showError(form, errorMsg);
        return false;
      }
      showLoading(form);
    });
  });

  function showError(form, msg) {
    let err = form.parentElement.querySelector(".error");
    if (!err) {
      err = document.createElement("div");
      err.className = "error";
      form.parentElement.insertBefore(err, form);
    }
    err.textContent = msg;
    err.style.display = "block";
    hideLoading(form);
  }
  function showLoading(form) {
    let loading = form.parentElement.querySelector(".loading");
    if (!loading) {
      loading = document.createElement("div");
      loading.className = "loading";
      form.parentElement.insertBefore(loading, form);
    }
    loading.style.display = "block";
  }
  function hideLoading(form) {
    let loading = form.parentElement.querySelector(".loading");
    if (loading) loading.style.display = "none";
  }

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
      resendBtn.disabled = true;
      resendBtn.textContent = "Resending...";
      try {
        const response = await fetch("/resend-otp", {
          method: "POST",
          headers: { "Content-Type": "application/json" }
        });
        const result = await response.json();

        if (result.success) {
          resendBtn.textContent = "OTP Sent!";
          setTimeout(() => {
            resendBtn.textContent = "Resend OTP";
            resendBtn.disabled = false;
          }, 2000);
        } else {
          resendBtn.textContent = "Resend OTP";
          resendBtn.disabled = false;
          alert("Failed: " + result.message);
        }
      } catch (err) {
        resendBtn.textContent = "Resend OTP";
        resendBtn.disabled = false;
        alert("Error contacting server: " + err.message);
      }
    });
  }
});
