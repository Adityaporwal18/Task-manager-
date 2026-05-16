const root = document.documentElement;
const savedTheme = localStorage.getItem("theme") || "light";
root.setAttribute("data-theme", savedTheme);

// Dark / Light Mode
const themeToggle = document.getElementById("themeToggle");

if (themeToggle) {
    const label = themeToggle.querySelector("span");
    const icon = themeToggle.querySelector("i");

    const syncThemeButton = () => {
        const isDark = root.getAttribute("data-theme") === "dark";

        if (label) {
            label.textContent = isDark ? "Light Mode" : "Dark Mode";
        }

        if (icon) {
            icon.className = isDark ? "bi bi-sun" : "bi bi-moon-stars";
        }
    };

    syncThemeButton();

    themeToggle.addEventListener("click", () => {
        const next = root.getAttribute("data-theme") === "dark" ? "light" : "dark";
        root.setAttribute("data-theme", next);
        localStorage.setItem("theme", next);
        syncThemeButton();
    });
}

// Sidebar Collapse Button
document.addEventListener("DOMContentLoaded", function () {
    const sidebarToggle = document.getElementById("sidebarToggle");
    const sidebarToggleIcon = document.getElementById("sidebarToggleIcon");

    if (sidebarToggle) {
        sidebarToggle.addEventListener("click", function () {
            document.body.classList.toggle("sidebar-collapsed");

            if (sidebarToggleIcon) {
                if (document.body.classList.contains("sidebar-collapsed")) {
                    sidebarToggleIcon.className = "bi bi-chevron-right";
                } else {
                    sidebarToggleIcon.className = "bi bi-chevron-left";
                }
            }
        });
    }
});

// Auto close flash alerts
setTimeout(() => {
    document.querySelectorAll(".alert").forEach((alert) => {
        const instance = bootstrap.Alert.getOrCreateInstance(alert);
        instance.close();
    });
}, 4500);

// Quick table search
const quickSearch = document.getElementById("quickTableSearch");

if (quickSearch) {
    quickSearch.addEventListener("keyup", () => {
        const value = quickSearch.value.toLowerCase();

        document.querySelectorAll("[data-task-row]").forEach((row) => {
            row.style.display = row.textContent.toLowerCase().includes(value) ? "" : "none";
        });
    });
}