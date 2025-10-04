document.addEventListener("DOMContentLoaded", () => {
  // -----------------------------
  // Reset Password Page Logic
  // -----------------------------
  function setupResetPasswordPage() {
    // Password show/hide toggle
    document.querySelectorAll('.toggle-password').forEach(btn => {
      btn.addEventListener('click', () => {
        const input = btn.previousElementSibling;
        if (input.type === 'password') {
          input.type = 'text';
          btn.textContent = 'Hide';
        } else {
          input.type = 'password';
          btn.textContent = 'Show';
        }
      });
    });

    // OTP timer logic
    let resetTimerEl = document.getElementById('resetTimer');
    let resetTimerInterval;
    function startResetTimer(seconds) {
      if (resetTimerInterval) clearInterval(resetTimerInterval);
      let timeLeft = seconds;
      function updateTimer() {
        if (timeLeft <= 0) {
          clearInterval(resetTimerInterval);
          resetTimerEl.innerText = 'Expired';
        } else {
          let m = String(Math.floor(timeLeft / 60)).padStart(2, '0');
          let s = String(timeLeft % 60).padStart(2, '0');
          resetTimerEl.innerText = `${m}:${s}`;
          timeLeft--;
        }
      }
      updateTimer();
      resetTimerInterval = setInterval(updateTimer, 1000);
    }
    if (resetTimerEl) {
      startResetTimer(300);
    }

    // Send OTP button logic
    const sendOtpBtn = document.getElementById('sendResetOtpBtn');
    if (sendOtpBtn) {
      sendOtpBtn.addEventListener('click', async function() {
        const email = document.getElementById('email').value.trim();
        if (!email) {
          alert('Please enter your registered email first.');
          return;
        }
        this.disabled = true;
        this.textContent = 'Sending...';
        try {
          const response = await fetch('/send-reset-otp', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email })
          });
          const result = await response.json();
          if (result.success) {
            this.textContent = 'OTP Sent!';
            startResetTimer(300);
            setTimeout(() => {
              this.textContent = 'Send OTP';
              this.disabled = false;
            }, 2000);
          } else {
            this.textContent = 'Send OTP';
            this.disabled = false;
            alert('Failed: ' + result.message);
          }
        } catch (err) {
          this.textContent = 'Send OTP';
          this.disabled = false;
          alert('Error contacting server: ' + err.message);
        }
      });
    }
  }

  // -----------------------------
  // Reset Password OTP Page Logic
  // -----------------------------
  function setupResetPasswordOtpPage() {
    let resetTimerEl = document.getElementById('resetTimer');
    let resetTimerInterval;
    function startResetTimer(seconds) {
      if (resetTimerInterval) clearInterval(resetTimerInterval);
      let timeLeft = seconds;
      function updateTimer() {
        if (timeLeft <= 0) {
          clearInterval(resetTimerInterval);
          resetTimerEl.innerText = 'OTP has expired';
        } else {
          let m = String(Math.floor(timeLeft / 60)).padStart(2, '0');
          let s = String(timeLeft % 60).padStart(2, '0');
          resetTimerEl.innerText = `${m}:${s}`;
          timeLeft--;
        }
      }
      updateTimer();
      resetTimerInterval = setInterval(updateTimer, 1000);
    }
    if (resetTimerEl) {
      startResetTimer(300);
    }

    // Resend OTP button logic
    const resendBtn = document.getElementById('resendResetOtpBtn');
    const emailInput = document.getElementById('email'); // Not present, so use session on backend
    if (resendBtn) {
      resendBtn.addEventListener('click', async function() {
        resendBtn.disabled = true;
        resendBtn.textContent = 'Resending...';
        try {
          // Email is stored in session, so no need to pass from frontend
          const response = await fetch('/send-reset-otp', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email: null }) // backend uses session
          });
          const result = await response.json();
          if (result.success) {
            resendBtn.textContent = 'OTP Sent!';
            startResetTimer(300);
            setTimeout(() => {
              resendBtn.textContent = 'Resend OTP';
              resendBtn.disabled = false;
            }, 2000);
          } else {
            resendBtn.textContent = 'Resend OTP';
            resendBtn.disabled = false;
            alert('Failed: ' + result.message);
          }
        } catch (err) {
          resendBtn.textContent = 'Resend OTP';
          resendBtn.disabled = false;
          alert('Error contacting server: ' + err.message);
        }
      });
    }
  }

  // -----------------------------
  // Reset Password New Page Logic
  // -----------------------------
  function setupResetPasswordNewPage() {
    document.querySelectorAll('.toggle-password').forEach(btn => {
      btn.addEventListener('click', () => {
        const input = btn.previousElementSibling;
        if (input.type === 'password') {
          input.type = 'text';
          btn.textContent = 'Hide';
        } else {
          input.type = 'password';
          btn.textContent = 'Show';
        }
      });
    });
  }

  // Initialize logic for each reset password step
  if (document.getElementById('sendResetOtpBtn')) {
    setupResetPasswordPage();
  }
  if (document.getElementById('resendResetOtpBtn')) {
    setupResetPasswordOtpPage();
  }
  if (document.getElementById('new_password') && document.getElementById('confirm_password')) {
    setupResetPasswordNewPage();
  }
});
