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
    const currentSection = document.getElementById('current-section');
    if (currentSection) {
        currentSection.innerText = 'AGENDA - ' + name;
    }
    const viewTitle = document.getElementById('view-title');
    if (viewTitle) {
        viewTitle.innerText = name;
    }
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

// Resaltar la sección activa y desplegar su submenú en base a la URL actual
document.addEventListener("DOMContentLoaded", () => {
    const currentPath = window.location.pathname;

    // Buscar todos los enlaces en el drawer
    const links = document.querySelectorAll(".drawer a.menu-item");
    links.forEach(link => {
        const linkPath = new URL(link.href, window.location.origin).pathname;
        if (currentPath === linkPath) {
            link.classList.add("sub-active");

            // Si el enlace está dentro de un submenú, lo abrimos automáticamente
            const parentSubmenu = link.closest(".submenu");
            if (parentSubmenu) {
                parentSubmenu.classList.add("active");
            }
        }
    });
});

/* ══════════ NAVEGACIÓN DE PESTAÑAS ══════════ */
function switchTab(tabName, event) {
    if (event) event.preventDefault();

    const panels = { ficha: 'panel-ficha', segunda: 'panel-segunda' };
    const tabBtns = { ficha: 'tab-btn-ficha', segunda: 'tab-btn-segunda' };

    Object.keys(panels).forEach(function (key) {
        document.getElementById(panels[key]).style.display = (key === tabName) ? 'block' : 'none';
        document.getElementById(tabBtns[key]).classList.toggle('active', key === tabName);
    });
}

/* ══════════ MODAL DE AYUDA ══════════ */
function toggleInfoModal() {
    const overlay = document.getElementById('info-modal-overlay');
    const modal = document.getElementById('info-modal');
    const visible = overlay.style.display === 'flex';
    overlay.style.display = visible ? 'none' : 'flex';
    modal.style.display = visible ? 'none' : 'block';
}

/* ══════════ PROCEDIMIENTOS ══════════ */
document.addEventListener('DOMContentLoaded', function () {
    const selectProc = document.getElementById('id_procedimiento');
    const container = document.getElementById('procedimientos-container');

    // Este bloque solo aplica en la vista de crear/editar consulta.
    // Si los elementos no existen en el DOM, se omite para evitar errores.
    if (!selectProc || !container) return;

    const emptyHint = container.querySelector('.empty-hint');
    const otrosWrapper = document.getElementById('otros-wrapper');
    const otroInput = document.getElementById('id_procedimiento_otro');
    const btnAgregarOtro = document.getElementById('btn-agregar-otro');
    const btnCancelarOtro = document.getElementById('btn-cancelar-otro');
    const selectedSet = new Set();

    function agregarPill(label, key) {
        if (selectedSet.has(key)) return;
        selectedSet.add(key);
        if (emptyHint) emptyHint.style.display = 'none';

        const pill = document.createElement('span');
        pill.style.cssText = 'display:inline-flex; align-items:center; gap:8px; background-color:var(--primary-color); color:white; padding:4px 10px; border-radius:20px; font-size:0.85rem; font-weight:600; box-shadow:0 2px 5px rgba(26,188,156,0.2);';
        pill.innerHTML = `
            <span>${label}</span>
            <span class="remove-btn" style="cursor:pointer; font-weight:bold; opacity:0.8; transition:opacity 0.2s;" onmouseover="this.style.opacity=1" onmouseout="this.style.opacity=0.8">✕</span>
            <input type="hidden" name="procedimientos_enviados" value="${label}">
        `;
        pill.querySelector('.remove-btn').addEventListener('click', function () {
            selectedSet.delete(key);
            pill.remove();
            if (selectedSet.size === 0 && emptyHint) emptyHint.style.display = 'inline';
        });
        container.appendChild(pill);
    }

    selectProc.addEventListener('change', function () {
        const value = selectProc.value;
        selectProc.value = '';
        if (!value) return;
        if (value === '__otros__') {
            otrosWrapper.style.display = 'block';
            otroInput.focus();
        } else {
            agregarPill(value, value);
            otrosWrapper.style.display = 'none';
        }
    });

    btnAgregarOtro.addEventListener('click', function () {
        const texto = otroInput.value.trim();
        if (!texto) { otroInput.focus(); return; }
        agregarPill(texto, '__otro__' + texto.toLowerCase());
        otroInput.value = '';
        otrosWrapper.style.display = 'none';
    });

    btnCancelarOtro.addEventListener('click', function () {
        otroInput.value = '';
        otrosWrapper.style.display = 'none';
        selectProc.value = '';
    });

    otroInput.addEventListener('keydown', function (e) {
        if (e.key === 'Enter') { e.preventDefault(); btnAgregarOtro.click(); }
    });
});