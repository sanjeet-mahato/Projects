/* ============================================================
   Finance Insights - Forgot Password
   ============================================================ */


const resetPasswordForm =
    document.getElementById(
        "reset-password-form"
    );

const resetPasswordButton =
    document.getElementById(
        "reset-password-button"
    );

const sendOtpButton =
    document.getElementById(
        "send-otp-button"
    );

const verifyOtpButton =
    document.getElementById(
        "verify-otp-button"
    );

const loading =
    document.getElementById(
        "loading"
    );

const message =
    document.getElementById(
        "message"
    );

const emailInput =
    document.getElementById(
        "email"
    );

const otpInput =
    document.getElementById(
        "otp"
    );

const newPasswordInput =
    document.getElementById(
        "new-password"
    );

const confirmPasswordInput =
    document.getElementById(
        "confirm-password"
    );


/* ============================================================
   Reset Password State
   ============================================================ */

let emailAvailable = false;

let otpSent = false;

let otpVerified = false;

let resetToken = null;

let passwordsMatch = false;


/* ============================================================
   Shared Message
   ============================================================ */

function showMessage(
    text,
    type = "error"
) {
    message.textContent =
        text;

    message.className =
        `availability-message ${type}`;
}


function hideMessage() {
    message.textContent = "";

    message.className =
        "availability-message";
}


/* ============================================================
   Validation State
   ============================================================ */

function setValidationState(
    input,
    isValid
) {
    input.classList.remove(
        "validation-success",
        "validation-error"
    );

    input.classList.add(
        isValid
            ? "validation-success"
            : "validation-error"
    );
}


function clearValidationState(
    input
) {
    input.classList.remove(
        "validation-success",
        "validation-error"
    );
}


/* ============================================================
   Password Visibility
   ============================================================ */

document
    .querySelectorAll(".toggle-password")
    .forEach(button => {

        button.addEventListener(
            "click",
            () => {

                const input =
                    document.getElementById(
                        button.dataset.target
                    );


                if (
                    input.type === "password"
                ) {

                    input.type = "text";

                    button.textContent =
                        "Hide";

                } else {

                    input.type = "password";

                    button.textContent =
                        "Show";

                }

            }
        );

    });


/* ============================================================
   Password State
   ============================================================ */

function updatePasswordState() {

    const password =
        newPasswordInput.value;

    const confirmPassword =
        confirmPasswordInput.value;


    if (
        !password ||
        !confirmPassword
    ) {

        passwordsMatch = false;

        clearValidationState(
            newPasswordInput
        );

        clearValidationState(
            confirmPasswordInput
        );

        updateResetButton();

        return;
    }


    passwordsMatch =
        password === confirmPassword;


    setValidationState(
        newPasswordInput,
        passwordsMatch
    );

    setValidationState(
        confirmPasswordInput,
        passwordsMatch
    );


    showMessage(
        passwordsMatch
            ? "✓ Passwords match."
            : "✕ Passwords do not match.",
        passwordsMatch
            ? "success"
            : "error"
    );


    updateResetButton();
}


newPasswordInput.addEventListener(
    "input",
    updatePasswordState
);


confirmPasswordInput.addEventListener(
    "input",
    updatePasswordState
);


/* ============================================================
   Reset Button State
   ============================================================ */

function updateResetButton() {

    resetPasswordButton.disabled =
        !(
            otpVerified &&
            resetToken &&
            passwordsMatch
        );
}


/* ============================================================
   Email Change
   ============================================================ */

emailInput.addEventListener(
    "input",
    () => {

        emailAvailable = false;

        otpSent = false;

        otpVerified = false;

        resetToken = null;

        passwordsMatch = false;


        clearValidationState(
            emailInput
        );


        otpInput.value = "";

        otpInput.disabled = false;


        verifyOtpButton.disabled =
            true;

        verifyOtpButton.classList.remove(
            "verified"
        );

        verifyOtpButton.textContent =
            "Verify OTP";


        sendOtpButton.disabled =
            false;


        newPasswordInput.value = "";

        confirmPasswordInput.value = "";

        newPasswordInput.disabled =
            true;

        confirmPasswordInput.disabled =
            true;


        clearValidationState(
            newPasswordInput
        );

        clearValidationState(
            confirmPasswordInput
        );


        updateResetButton();

        hideMessage();

    }
);


/* ============================================================
   Send Password Reset OTP
   ============================================================ */

sendOtpButton.addEventListener(
    "click",
    async () => {

        const email =
            emailInput.value.trim();


        if (!email) {

            showMessage(
                "✕ Please enter your email address."
            );

            emailInput.focus();

            return;
        }


        sendOtpButton.disabled = true;


        try {

            const result =
                await sendPasswordResetOtp(
                    email
                );


            emailAvailable = true;

            otpSent = true;

            otpVerified = false;

            resetToken = null;


            otpInput.disabled =
                false;

            verifyOtpButton.disabled =
                false;


            verifyOtpButton.classList.remove(
                "verified"
            );

            verifyOtpButton.textContent =
                "Verify OTP";


            showMessage(
                result.message ||
                "✓ OTP sent successfully.",
                "success"
            );


        } catch (error) {

            emailAvailable = false;

            otpSent = false;

            otpVerified = false;

            resetToken = null;


            verifyOtpButton.disabled =
                true;


            showMessage(
                error.message
            );

        } finally {

            if (!otpVerified) {

                sendOtpButton.disabled =
                    false;

            }

            updateResetButton();

        }

    }
);


/* ============================================================
   Verify Password Reset OTP
   ============================================================ */

verifyOtpButton.addEventListener(
    "click",
    async () => {

        const email =
            emailInput.value.trim();

        const otp =
            otpInput.value.trim();


        if (!otp) {

            showMessage(
                "✕ Please enter the OTP."
            );

            otpInput.focus();

            return;
        }


        verifyOtpButton.disabled =
            true;


        try {

            const result =
                await verifyPasswordResetOtp(
                    email,
                    otp
                );


            /* ------------------------------------------------
               Invalid OTP
               ------------------------------------------------ */

            if (!result.verified) {

                otpVerified = false;

                resetToken = null;


                showMessage(
                    result.message,
                    "error"
                );


                if (
                    result.remaining_attempts > 0
                ) {

                    verifyOtpButton.disabled =
                        false;

                } else {

                    otpSent = false;

                    verifyOtpButton.disabled =
                        true;

                    sendOtpButton.disabled =
                        false;

                    otpInput.value = "";

                }


                updateResetButton();

                return;
            }


            /* ------------------------------------------------
               Successful OTP Verification
               ------------------------------------------------ */

            otpVerified = true;

            resetToken =
                result.token;


            showMessage(
                "✓ Email verified successfully.",
                "success"
            );


            verifyOtpButton.textContent =
                "✓ Verified";

            verifyOtpButton.classList.add(
                "verified"
            );

            verifyOtpButton.disabled =
                true;


            sendOtpButton.disabled =
                true;


            otpInput.disabled =
                true;


            newPasswordInput.disabled =
                false;

            confirmPasswordInput.disabled =
                false;


            newPasswordInput.focus();


            updateResetButton();

        } catch (error) {

            otpVerified = false;

            resetToken = null;


            showMessage(
                error.message
            );


            verifyOtpButton.disabled =
                false;


            updateResetButton();

        }

    }
);


/* ============================================================
   Reset Password
   ============================================================ */

resetPasswordForm.addEventListener(
    "submit",
    async event => {

        event.preventDefault();


        if (
            !otpVerified ||
            !resetToken
        ) {

            showMessage(
                "✕ Please verify your email first."
            );

            return;
        }


        if (!passwordsMatch) {

            showMessage(
                "✕ Passwords do not match."
            );

            return;
        }


        resetPasswordButton.disabled =
            true;

        loading.classList.add(
            "visible"
        );


        const email =
            emailInput.value.trim();

        const newPassword =
            newPasswordInput.value;


        try {

            await resetPassword(
                email,
                newPassword,
                resetToken
            );


            showMessage(
                "✓ Password reset successfully. Redirecting to login...",
                "success"
            );


            setTimeout(
                () => {

                    window.location.href =
                        "/login";

                },
                1200
            );

        } catch (error) {

            showMessage(
                error.message
            );

            resetPasswordButton.disabled =
                false;

        } finally {

            loading.classList.remove(
                "visible"
            );

        }

    }
);