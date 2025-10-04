document.addEventListener("DOMContentLoaded", () => {

  // -----------------------------
  // Toggle password visibility
  // -----------------------------
 document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll('.toggle-password').forEach(btn => {
    btn.addEventListener('click', () => {
      const input = btn.previousElementSibling;
      if (input && input.type === 'password') {
        input.type = 'text';
        btn.textContent = 'Hide';
      } else if (input) {
        input.type = 'password';
        btn.textContent = 'Show';
      }
    });
  });
});


  // -----------------------------
  // OTP Page Logic (Countdown + Resend)
  // -----------------------------
  const otpTimerEl = document.getElementById('resetTimer');
  const resendBtn = document.getElementById('resendOtpBtn');
  let otpInterval;

  function startOtpTimer(seconds) {
    if (!otpTimerEl) return;
    if (otpInterval) clearInterval(otpInterval);

    let timeLeft = seconds;
    function update() {
      if (timeLeft <= 0) {
        clearInterval(otpInterval);
        otpTimerEl.innerText = 'Expired';
        resendBtn && (resendBtn.disabled = false); // enable resend when expired
      } else {
        let m = String(Math.floor(timeLeft / 60)).padStart(2, '0');
        let s = String(timeLeft % 60).padStart(2, '0');
        otpTimerEl.innerText = `${m}:${s}`;
        timeLeft--;
      }
    }
    update();
    otpInterval = setInterval(update, 1000);
  }

  // Start 5-min timer if OTP page
  if (otpTimerEl) startOtpTimer(300);

  // -----------------------------
  // Resend OTP button logic
  // -----------------------------
  if (resendBtn) {
    resendBtn.addEventListener('click', async () => {
      resendBtn.disabled = true;
      resendBtn.textContent = 'Resending...';

      try {
        const response = await fetch('/resend-otp', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({})
        });

        const result = await response.json();

        if (result.success) {
          otpTimerEl && startOtpTimer(300); // restart 5-min timer
          resendBtn.textContent = 'OTP Sent!';
          setTimeout(() => {
            resendBtn.textContent = 'Resend OTP';
            resendBtn.disabled = false;
          }, 2000);
        } else {
          alert('Failed: ' + result.message);
          resendBtn.textContent = 'Resend OTP';
          resendBtn.disabled = false;
        }
      } catch (err) {
        alert('Error contacting server: ' + err.message);
        resendBtn.textContent = 'Resend OTP';
        resendBtn.disabled = false;
      }
    });
  }

  // -----------------------------
  // Reset Password / Change Password Page
  // -----------------------------
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

});
