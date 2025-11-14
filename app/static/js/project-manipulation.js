function approveProject(id) {
    fetch(`/admin/project/approve/${id}`, { method: "POST" })
        .then(r => r.json())
        .then(data => {
            showToast(data.message);
            setTimeout(() => location.reload(), 400);
        });
}

function suspendProject(id) {
    fetch(`/admin/project/suspend/${id}`, { method: "POST" })
        .then(r => r.json())
        .then(data => {
            showToast(data.message);
            setTimeout(() => location.reload(), 400);
        });
}

function deleteProject(id) {
    fetch(`/admin/project/delete/${id}`, { method: "POST" })
        .then(r => r.json())
        .then(data => {
            showToast(data.message);
            setTimeout(() => location.reload(), 400);
        });
}

function suspendUser(id) {
    fetch(`/admin/user/suspend/${id}`, { method: "POST" })
        .then(r => r.json())
        .then(data => {
            showToast(data.message);
            setTimeout(() => location.reload(), 400);
        });
}

function unsuspendUser(id) {
    fetch(`/admin/user/unsuspend/${id}`, { method: "POST" })
        .then(r => r.json())
        .then(data => {
            showToast(data.message);
            setTimeout(() => location.reload(), 400);
        });
}

function deleteUser(id) {
    fetch(`/admin/user/delete/${id}`, { method: "POST" })
        .then(r => r.json())
        .then(data => {
            showToast(data.message);
            setTimeout(() => location.reload(), 400);
        });
}
