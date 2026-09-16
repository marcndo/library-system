function getUsernameFromToken(token) {
    try {
        const payloadBase64 = token.split(".")[1];
        const payload = JSON.parse(atob(payloadBase64));
        return payload.sub;
    } catch (error) {
        return null;
    }
}

function renderNav() {
    const nav = document.getElementById("nav");
    const token = localStorage.getItem("access_token");
    const username = token ? getUsernameFromToken(token) : null;

    let linksHtml = `
        <a href="/static/index.html">Home</a>
        <a href="/static/lend.html">Lend</a>
    `;

    if (username) {
        linksHtml += `
            <span class="nav-status">Logged in as <strong>${username}</strong></span>
            <a href="#" id="logout-link">Log Out</a>
        `;
    } else {
        linksHtml += `
            <a href="/static/login.html">Log In</a>
            <a href="/static/register.html">Sign Up</a>
        `;
    }

    nav.innerHTML = linksHtml;

    if (username) {
        document.getElementById("logout-link").addEventListener("click", function (event) {
            event.preventDefault();
            localStorage.removeItem("access_token");
            window.location.href = "/static/index.html";
        });
    }
}

renderNav();