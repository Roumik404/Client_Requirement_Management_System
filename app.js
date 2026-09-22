(function () {
    const toggle = document.querySelector("[data-theme-toggle]");
    const savedTheme = localStorage.getItem("clientreq-theme");
    const menuToggle = document.querySelector("[data-sidebar-toggle]");
    const closeToggle = document.querySelector("[data-sidebar-close]");
    const sidebar = document.querySelector("[data-sidebar]");

    document.querySelectorAll("[data-password-toggle]").forEach(function (passwordToggle) {
        passwordToggle.addEventListener("click", function () {
            const target = document.getElementById(passwordToggle.dataset.passwordTarget);

            if (!target) {
                return;
            }

            const shouldShow = target.type === "password";
            target.type = shouldShow ? "text" : "password";
            passwordToggle.setAttribute("aria-label", shouldShow ? "Hide password" : "Show password");
            passwordToggle.setAttribute("title", shouldShow ? "Hide password" : "Show password");
            passwordToggle.classList.toggle("is-visible", shouldShow);
        });
    });

    if (savedTheme === "dark") {
        document.body.classList.add("dark-theme");
    }

    if (toggle) {
        toggle.addEventListener("click", function () {
            const isDark = document.body.classList.toggle("dark-theme");
            localStorage.setItem("clientreq-theme", isDark ? "dark" : "light");
            toggle.setAttribute("aria-label", isDark ? "Switch to light theme" : "Switch to dark theme");
        });
    }

    if (menuToggle && sidebar) {
        function closeSidebar() {
            document.body.classList.remove("sidebar-open");
            menuToggle.setAttribute("aria-expanded", "false");
            menuToggle.setAttribute("aria-label", "Open navigation menu");
        }

        menuToggle.addEventListener("click", function () {
            const isOpen = document.body.classList.toggle("sidebar-open");
            menuToggle.setAttribute("aria-expanded", isOpen ? "true" : "false");
            menuToggle.setAttribute("aria-label", isOpen ? "Close navigation menu" : "Open navigation menu");
        });

        document.addEventListener("click", function (event) {
            if (!document.body.classList.contains("sidebar-open")) {
                return;
            }

            if (!sidebar.contains(event.target) && !menuToggle.contains(event.target)) {
                closeSidebar();
            }
        });

        if (closeToggle) {
            closeToggle.addEventListener("click", closeSidebar);
        }

        sidebar.querySelectorAll(".nav-links a").forEach(function (link) {
            link.addEventListener("click", function () {
                closeSidebar();
            });
        });
    }

    document.querySelectorAll("[data-toast]").forEach(function (toast) {
        window.setTimeout(function () {
            toast.classList.add("toast-hidden");
        }, 4200);
    });

    document.querySelectorAll("[data-filter-form] select").forEach(function (filter) {
        filter.addEventListener("change", function () {
            filter.form.submit();
        });
    });
})();