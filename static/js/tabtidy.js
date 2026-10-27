
document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("link-form");
    const title = document.getElementById("id_title");
    const url = document.getElementById("id_url");
    const titleMessage = document.getElementById("title-message");
    const urlMessage = document.getElementById("url-message");

    if (!form || !title || !url) return;

    function validateTitle() {
        const isEmpty = title.value.trim() === "";

        title.classList.toggle("is-invalid", isEmpty);
        title.classList.toggle("is-valid", !isEmpty);

        titleMessage.textContent = isEmpty
            ? "Please enter a title for your link."
            : "Looks good!";

        titleMessage.classList.toggle("text-danger", isEmpty);
        titleMessage.classList.toggle("text-success", !isEmpty);

        return !isEmpty;
    }

    function validateUrl() {
        const value = url.value.trim();
        let isInvalid = true;

        try {
            const parsed = new URL(value);
            isInvalid = !(
                ["http:", "https:"].includes(parsed.protocol) &&
                parsed.hostname.includes(".") &&
                !/\s/.test(value)
            );
        } catch {
            isInvalid = true;
        }

        url.classList.toggle("is-invalid", isInvalid);
        url.classList.toggle("is-valid", !isInvalid);

        urlMessage.textContent = isInvalid
            ? "Please enter a valid URL, such as https://example.com."
            : "Looks good!";

        urlMessage.classList.toggle("text-danger", isInvalid);
        urlMessage.classList.toggle("text-success", !isInvalid);

        return !isInvalid;
    }

    title.addEventListener("blur", validateTitle);
    url.addEventListener("blur", validateUrl);

    title.addEventListener("input", function () {
        if (title.classList.contains("is-invalid") ||
            title.classList.contains("is-valid")) {
            validateTitle();
        }
    });

    url.addEventListener("input", function () {
        if (url.classList.contains("is-invalid") ||
            url.classList.contains("is-valid")) {
            validateUrl();
        }
    });

    form.addEventListener("submit", function (event) {
        const titleValid = validateTitle();
        const urlValid = validateUrl();

        if (!titleValid || !urlValid) {
            event.preventDefault();

            if (!titleValid) {
                title.focus();
            } else {
                url.focus();
            }
        }
    });
});
