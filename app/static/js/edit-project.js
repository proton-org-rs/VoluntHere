async function editProject(projectId) {
    try {
        const response = await fetch(`/projects/edit/${projectId}`, {
            method: "POST"
        });

        const data = await response.json();
        showToast(data.message);

    } catch (err) {
        showToast("Error while editing project.");
    }
}