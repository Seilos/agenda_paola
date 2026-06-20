/**
 * Global Form Submission Handler
 * Previene el doble envío (Double Submit) en formularios válidos,
 * modificando el texto del botón temporalmente a "Procesando..." sin alterar su diseño.
 * 
 * Para implementarlo, solo es necesario agregar el script en el HTML.
 *     <script src="{% static 'js/form_helper.js' %}"></script>
 * 
 * @author Lic. Francisco Palmar
 * @version 1.0.0
 * @since 2026-06-19
 */

// Esperamos a que el DOM esté completamente cargado antes de ejecutar el script
document.addEventListener('DOMContentLoaded', () => {
    // 1. Manejador de envío para todos los formularios
    document.querySelectorAll('form').forEach(form => {
        // Agregamos un event listener para el evento submit
        form.addEventListener('submit', function (event) {
            // Validación técnica: Si el formulario no pasa las validaciones nativas de HTML5, no hacemos nada.
            if (!this.checkValidity()) {
                return;
            }
            // Seleccionamos el botón de submit
            const submitBtn = this.querySelector('button[type="submit"]');
            // Si el botón existe
            if (submitBtn) {
                // Deshabilitamos el botón para evitar doble clic
                submitBtn.disabled = true;

                // Guardamos el texto original (manteniendo el valor interno de texto sin HTML)
                submitBtn.dataset.originalText = submitBtn.innerText || submitBtn.textContent;

                // Cambiamos el texto de forma limpia a "Procesando..."
                submitBtn.innerText = 'Procesando...';
            }
        });
    });

    // 2. Reactivar el botón si el usuario regresa atrás en el historial del navegador (BFCache)
    window.addEventListener('pageshow', (event) => {
        // Si el evento fue persistido, significa que el usuario regresó atrás
        if (event.persisted) {
            document.querySelectorAll('button[type="submit"]').forEach(btn => {
                // Si el botón está deshabilitado, lo reactivamos
                if (btn.disabled) {
                    btn.disabled = false;
                    // Si el botón tiene texto original, lo restauramos
                    if (btn.dataset.originalText) {
                        btn.innerText = btn.dataset.originalText;
                    }
                }
            });
        }
    });
});
