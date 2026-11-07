/* ============================================================
   Finance Insights - Signup
   ============================================================ */


const signupForm =
    document.getElementById("signup-form");

const signupButton =
    document.getElementById("signup-button");

const sendOtpButton =
    document.getElementById("send-otp-button");

const verifyOtpButton =
    document.getElementById("verify-otp-button");

const loading =
    document.getElementById("loading");

const availabilityMessage =
    document.getElementById(
        "availability-message"
    );

const usernameInput =
    document.getElementById("username");

const emailInput =
    document.getElementById("email");

const passwordInput =
    document.getElementById("password");

const confirmPasswordInput =
    document.getElementById("confirm-password");

const otpInput =
    document.getElementById("otp");


/* ============================================================
   Signup State
   ============================================================ */

let usernameAvailable = false;

let emailAvailable = false;

let passwordsMatch = false;

let otpSent = false;

let otpVerified = false;

let verificationToken = null;


/* ============================================================
   Shared Message
   ============================================================ */

function showMessage(
    text,
    type = "error"
) {
    availabilityMessage.textContent =
        text;

    availabilityMessage.className =
        `availability-message ${type}`;
}


function hideMessage() {
    availabilityMessage.textContent = "";

    availabilityMessage.className =
        "availability-message";
}


/* ============================================================
   Loading
   ============================================================ */

function setLoading(
    isLoading
) {
    loading.classList.toggle(
        "visible",
        isLoading
    );

    signupButton.disabled =
        isLoading ||
        !canSubmit();

    sendOtpButton.disabled =
        isLoading ||
        otpVerified;

    verifyOtpButton.disabled =
        isLoading ||
        !otpSent ||
        otpVerified;
}


/* ============================================================
   Submit State
   ============================================================ */

function canSubmit() {
    return (
        usernameAvailable &&
        emailAvailable &&
        passwordsMatch &&
        otpVerified &&
        verificationToken
    );
}


function updateSignupButton() {
    signupButton.disabled =
        !canSubmit();
}


/* ============================================================
   Input Validation Styling
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
   Username Availability
   ============================================================ */

usernameInput.addEventListener(
    "input",
    () => {

        usernameAvailable = false;

        clearValidationState(
            usernameInput
        );

        hideMessage();

        updateSignupButton();

    }
);


usernameInput.addEventListener(
    "blur",
    async () => {

        const username =
            usernameInput.value.trim();


        if (!username) {

            usernameAvailable = false;

            clearValidationState(
                usernameInput
            );

            hideMessage();

            updateSignupButton();

            return;
        }


        try {

            const result =
                await checkUsername(
                    username
                );


            usernameAvailable =
                result.available;


            setValidationState(
                usernameInput,
                result.available
            );


            showMessage(
                result.message,
                result.available
                    ? "success"
                    : "error"
            );


            updateSignupButton();

        } catch (error) {

            usernameAvailable = false;

            setValidationState(
                usernameInput,
                false
            );


            showMessage(
                error.message
            );


            updateSignupButton();

        }

    }
);


/* ============================================================
   Email Availability
   ============================================================ */

emailInput.addEventListener(
    "input",
    () => {

        emailAvailable = false;

        otpSent = false;

        otpVerified = false;

        verificationToken = null;

        clearValidationState(
            emailInput
        );

        hideMessage();

        otpInput.value = "";

        otpInput.disabled = false;

        verifyOtpButton.disabled = true;

        verifyOtpButton.classList.remove(
            "verified"
        );

        verifyOtpButton.textContent =
            "Verify OTP";

        sendOtpButton.disabled = false;

        updateSignupButton();

    }
);


emailInput.addEventListener(
    "blur",
    async () => {

        const email =
            emailInput.value.trim();


        if (!email) {

            emailAvailable = false;

            clearValidationState(
                emailInput
            );

            hideMessage();

            updateSignupButton();

            return;
        }


        try {

            const result =
                await checkEmail(
                    email
                );


            emailAvailable =
                result.available;


            setValidationState(
                emailInput,
                result.available
            );


            showMessage(
                result.message,
                result.available
                    ? "success"
                    : "error"
            );


            updateSignupButton();

        } catch (error) {

            emailAvailable = false;

            setValidationState(
                emailInput,
                false
            );


            showMessage(
                error.message
            );


            updateSignupButton();

        }

    }
);


/* ============================================================
   Password Confirmation
   ============================================================ */

function validatePasswords() {

    const password =
        passwordInput.value;

    const confirmPassword =
        confirmPasswordInput.value;


    if (
        !password ||
        !confirmPassword
    ) {

        passwordsMatch = false;

        clearValidationState(
            passwordInput
        );

        clearValidationState(
            confirmPasswordInput
        );

        updateSignupButton();

        return;
    }


    passwordsMatch =
        password === confirmPassword;


    setValidationState(
        passwordInput,
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


    updateSignupButton();
}


passwordInput.addEventListener(
    "input",
    validatePasswords
);


confirmPasswordInput.addEventListener(
    "input",
    validatePasswords
);


/* ============================================================
   Send OTP
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


        if (!emailAvailable) {

            showMessage(
                "✕ Please enter an available email address first."
            );

            emailInput.focus();

            return;
        }


        sendOtpButton.disabled = true;


        try {

            const result =
                await sendEmailVerificationOtp(
                    email
                );


            otpSent = true;

            otpVerified = false;

            verificationToken = null;

            otpInput.disabled = false;

            verifyOtpButton.disabled = false;

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

            otpSent = false;

            otpVerified = false;

            verificationToken = null;

            verifyOtpButton.disabled = true;


            showMessage(
                error.message
            );

        } finally {

            if (!otpVerified) {

                sendOtpButton.disabled =
                    false;

            }

            updateSignupButton();

        }

    }
);


/* ============================================================
   Verify OTP
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


        verifyOtpButton.disabled = true;


        try {

            const result =
                await verifyEmailVerificationOtp(
                    email,
                    otp
                );


            /* ------------------------------------------------
               Invalid OTP
               ------------------------------------------------ */

            if (!result.verified) {

                otpVerified = false;

                verificationToken = null;


                showMessage(
                    result.message,
                    "error"
                );


                if (
                    result.remaining_attempts > 0
                ) {

                    /*
                     * Attempts remain.
                     * Allow another verification attempt.
                     */

                    verifyOtpButton.disabled =
                        false;

                } else {

                    /*
                     * Attempts exhausted.
                     * User must request a new OTP.
                     */

                    otpSent = false;

                    verifyOtpButton.disabled =
                        true;

                    sendOtpButton.disabled =
                        false;

                    otpInput.value = "";

                }


                updateSignupButton();

                return;
            }


            /* ------------------------------------------------
               Successful OTP Verification
               ------------------------------------------------ */

            otpVerified = true;

            verificationToken =
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

            sendOtpButton.disabled =
                true;

            otpInput.disabled =
                true;

            verifyOtpButton.disabled =
                true;


            updateSignupButton();

        } catch (error) {

            otpVerified = false;

            verificationToken = null;


            showMessage(
                error.message
            );


            verifyOtpButton.disabled =
                false;

            updateSignupButton();

        }

    }
);


/* ============================================================
   Signup
   ============================================================ */

signupForm.addEventListener(
    "submit",
    async event => {

        event.preventDefault();


        if (!canSubmit()) {

            showMessage(
                "✕ Please complete all required validations before creating your account."
            );

            return;
        }


        setLoading(true);


        const profileName =
            document
                .getElementById("profile-name")
                .value
                .trim();

        const username =
            usernameInput.value.trim();

        const email =
            emailInput.value.trim();

        const password =
            passwordInput.value;


        try {

            await signup(
                username,
                email,
                password,
                profileName,
                verificationToken
            );


            showMessage(
                "Account created successfully. Redirecting to login...",
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

        } finally {

            setLoading(false);

        }

    }
);