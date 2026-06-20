/**
 * Controlador de Interfaz Modularizada para el Dashboard
 * Implementa la lógica de navegación interna y los estados de despliegue.
 * * @author Lic. Francisco Palmar
 * @version 2.0.0
 * @since 2026-06-19
 */

function toggleDrawer() {
    document.getElementById("myDrawer").classList.toggle("active");
    // Sincroniza la cortina de fondo estilo YouTube
    document.getElementById("drawerOverlay").classList.toggle("active");
}

function toggleSubmenu(id) {
    document.querySelectorAll('.submenu').forEach(s => {
        if (s.id !== id) s.classList.remove('active');
    });
    document.getElementById(id).classList.toggle('active');
}

function selectSection(name, element) {
    document.getElementById('current-section').innerText = 'AGENDA - ' + name;
    document.getElementById('view-title').innerText = name;
    document.querySelectorAll('.menu-item').forEach(item => item.classList.remove('sub-active'));
    if (element) element.classList.add('sub-active');
    toggleDrawer();
}

function toggleUserMenu(event) {
    event.stopPropagation(); // Previene el cierre inmediato por el listener global
    document.getElementById("user-menu").classList.toggle("show");
}

// Evento global para cerrar el menú desplegable del usuario
window.addEventListener('click', function (event) {
    const menu = document.getElementById("user-menu");
    if (menu && menu.classList.contains("show")) {
        menu.classList.remove("show");
    }
});