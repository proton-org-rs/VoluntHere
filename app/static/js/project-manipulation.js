function approveProject(id) {
    fetch(`/admin/project/approve/${id}`, { method: "POST" })
        .then(r => r.json())
        .then(data => showToast(data.message));
}

function suspendProject(id) {
    fetch(`/admin/project/suspend/${id}`, { method: "POST" })
        .then(r => r.json())
        .then(data => showToast(data.message));
}

function deleteProject(id) {
    fetch(`/admin/project/delete/${id}`, { method: "POST" })
        .then(r => r.json())
        .then(data => showToast(data.message));
}
