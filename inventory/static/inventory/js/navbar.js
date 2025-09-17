// inventory/static/inventory/js/navbar.js
document.addEventListener("DOMContentLoaded", function () {
    // Fallback seguro para abrir modal via botão (usa id changeRoleModal)
    (function() {
        const modalEl = document.getElementById("changeRoleModal");
        const btn = document.getElementById("change-role-btn");

        if (btn && modalEl) {
            btn.addEventListener("click", function (e) {
                try {
                    const bs = bootstrap.Modal.getInstance(modalEl) || new bootstrap.Modal(modalEl);
                    bs.show();
                } catch (err) {
                    // fallback simples sem quebrar
                    modalEl.style.display = "block";
                }
            });
        }
    })();

    // Inicializa toasts do Bootstrap (se existirem)
    (function() {
        try {
            var toastElList = Array.prototype.slice.call(document.querySelectorAll('.toast'));
            toastElList.forEach(function (toastEl) {
                try {
                    var toast = new bootstrap.Toast(toastEl, { delay: 5000 });
                    toast.show();
                } catch (errInner) {
                    console.error("Erro inicializando um toast:", errInner);
                }
            });
        } catch (err) {
            console.error("Erro ao inicializar toasts:", err);
        }
    })();
});
