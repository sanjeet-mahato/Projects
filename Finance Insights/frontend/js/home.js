/* ============================================================
   Finance Insights - Home
   ============================================================ */


const userButton =
    document.getElementById("user-button");

const userDropdown =
    document.getElementById("user-dropdown");

const logoutButton =
    document.getElementById("logout-button");

const userName =
    document.getElementById("user-name");

const userAvatar =
    document.getElementById("user-avatar");

const userDropdownName =
    document.getElementById("user-dropdown-name");


const documentsCard =
    document.getElementById("documents-card");

const merchantsCard =
    document.getElementById("merchants-card");

const insightsCard =
    document.getElementById("insights-card");


const aiChatbot =
    document.getElementById("ai-chatbot");

const aiChatbotButton =
    document.getElementById("ai-chatbot-button");

const aiChatbotPanel =
    document.getElementById("ai-chatbot-panel");

const aiChatbotClose =
    document.getElementById("ai-chatbot-close");

const openChatbotButton =
    document.getElementById("open-chatbot-button");


/* ============================================================
   USER MENU
   ============================================================ */

function toggleUserMenu() {

    userDropdown.hidden =
        !userDropdown.hidden;

}


function closeUserMenu() {

    userDropdown.hidden = true;

}


userButton.addEventListener(
    "click",
    event => {

        event.stopPropagation();

        toggleUserMenu();

    }
);


document.addEventListener(
    "click",
    event => {

        if (
            !event.target.closest(".user-menu")
        ) {

            closeUserMenu();

        }

    }
);


/* ============================================================
   USER INFORMATION
   ============================================================ */

async function loadUser() {

    try {

        const user = await getCurrentUser();

        if (!user) {
            window.location.href = "/login";
            return;
        }


        const displayName =
            user.profile_name ||
            user.username;


        userName.textContent =
            displayName;


        userDropdownName.textContent =
            displayName;


        userAvatar.textContent =
            displayName
                .charAt(0)
                .toUpperCase();

    } catch (error) {

        window.location.href = "/login";

    }

}


/* ============================================================
   LOGOUT
   ============================================================ */

logoutButton.addEventListener(
    "click",
    async () => {

        try {

            await logout();

        } finally {

            window.location.href = "/login";

        }

    }
);


/* ============================================================
   PAGE NAVIGATION
   ============================================================ */

documentsCard.addEventListener(
    "click",
    () => {

        window.location.href = "/document";

    }
);


merchantsCard.addEventListener(
    "click",
    () => {

        window.location.href = "/merchants";

    }
);


insightsCard.addEventListener(
    "click",
    () => {

        window.location.href = "/insights";

    }
);


/* ============================================================
   AI CHATBOT
   ============================================================ */

function openChatbot() {

    aiChatbotPanel.hidden = false;

    aiChatbotButton.setAttribute(
        "aria-expanded",
        "true"
    );

}


function closeChatbot() {

    aiChatbotPanel.hidden = true;

    aiChatbotButton.setAttribute(
        "aria-expanded",
        "false"
    );

}


aiChatbotButton.addEventListener(
    "click",
    event => {

        event.stopPropagation();

        if (aiChatbotPanel.hidden) {

            openChatbot();

        } else {

            closeChatbot();

        }

    }
);


aiChatbotClose.addEventListener(
    "click",
    () => {

        closeChatbot();

    }
);


document.addEventListener(
    "click",
    event => {

        if (
            !event.target.closest("#ai-chatbot")
        ) {

            closeChatbot();

        }

    }
);


/* ============================================================
   OPEN CHATBOT
   ============================================================ */

openChatbotButton.addEventListener(
    "click",
    () => {

        window.location.href = "/chatbot";

    }
);


/* ============================================================
   INITIALIZE
   ============================================================ */

loadUser();