/* ============================================================
   Login
   ============================================================ */

async function login(
    usernameOrEmail,
    password
) {
    return apiRequest(
        "/auth/login",
        {
            method: "POST",

            headers: {
                "Content-Type": "application/json",
            },

            body: JSON.stringify({
                username_or_email: usernameOrEmail,
                password: password,
            }),
        }
    );
}


/* ============================================================
   Logout
   ============================================================ */

async function logout() {
    return apiRequest(
        "/auth/logout",
        {
            method: "POST",
        }
    );
}


/* ============================================================
   Current User
   ============================================================ */

async function getCurrentUser() {
    return apiRequest(
        "/auth/me"
    );
}


/* ============================================================
   Username Availability
   ============================================================ */

async function checkUsername(username) {
    return apiRequest(
        `/auth/check-username?username=${encodeURIComponent(username)}`
    );
}


/* ============================================================
   Email Availability
   ============================================================ */

async function checkEmail(email) {
    return apiRequest(
        `/auth/check-email?email=${encodeURIComponent(email)}`
    );
}


/* ============================================================
   Email Verification OTP
   ============================================================ */

async function sendEmailVerificationOtp(email) {
    return apiRequest(
        "/auth/send-email-verification-otp",
        {
            method: "POST",

            headers: {
                "Content-Type": "application/json",
            },

            body: JSON.stringify({
                email: email,
            }),
        }
    );
}


async function verifyEmailVerificationOtp(
    email,
    otp
) {
    return apiRequest(
        "/auth/verify-email-verification-otp",
        {
            method: "POST",

            headers: {
                "Content-Type": "application/json",
            },

            body: JSON.stringify({
                email: email,
                otp: otp,
            }),
        }
    );
}


/* ============================================================
   Signup
   ============================================================ */

async function signup(
    username,
    email,
    password,
    profileName,
    verificationToken
) {
    return apiRequest(
        "/auth/signup",
        {
            method: "POST",

            headers: {
                "Content-Type": "application/json",
            },

            body: JSON.stringify({
                username: username,
                email: email,
                password: password,
                profile_name: profileName,
                verification_token: verificationToken,
            }),
        }
    );
}


/* ============================================================
   Password Reset OTP
   ============================================================ */

async function sendPasswordResetOtp(email) {
    return apiRequest(
        "/auth/send-password-reset-otp",
        {
            method: "POST",

            headers: {
                "Content-Type": "application/json",
            },

            body: JSON.stringify({
                email: email,
            }),
        }
    );
}


async function verifyPasswordResetOtp(
    email,
    otp
) {
    return apiRequest(
        "/auth/verify-password-reset-otp",
        {
            method: "POST",

            headers: {
                "Content-Type": "application/json",
            },

            body: JSON.stringify({
                email: email,
                otp: otp,
            }),
        }
    );
}


/* ============================================================
   Reset Password
   ============================================================ */

async function resetPassword(
    email,
    newPassword,
    resetToken
) {
    return apiRequest(
        "/auth/reset-password",
        {
            method: "POST",

            headers: {
                "Content-Type": "application/json",
            },

            body: JSON.stringify({
                email: email,
                new_password: newPassword,
                reset_token: resetToken,
            }),
        }
    );
}