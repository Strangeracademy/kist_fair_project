document.addEventListener("DOMContentLoaded", () => {
    const uploadForm = document.getElementById("upload-form");
    const resultsDiv = document.getElementById("analysis-results");

    uploadForm.addEventListener("submit", async (e) => {
        e.preventDefault();
        const fileInput = document.getElementById("file-input");

        if (!fileInput.files[0]) {
            alert("Please select a file!");
            return;
        }

        const formData = new FormData();
        formData.append("file", fileInput.files[0]);

        try {
            const response = await fetch("/upload", {
                method: "POST",
                body: formData,
            });
            const data = await response.json();

            if (data.error) {
                resultsDiv.innerHTML = `<p class="error">${data.error}</p>`;
            } else {
                resultsDiv.innerHTML = `
                    <h3>Analysis Results:</h3>
                    <pre>${data.analysis}</pre>
                `;
            }
        } catch (error) {
            console.error("Error uploading file:", error);
            resultsDiv.innerHTML = `<p class="error">Error uploading file. Please try again.</p>`;
        }
    });
});
