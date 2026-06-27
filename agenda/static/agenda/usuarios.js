document.addEventListener('DOMContentLoaded', function() {
    const searchForm = document.getElementById('search-form');
    if (!searchForm) return;

    const searchUrl = searchForm.getAttribute('data-url') || '/agenda/usuarios/buscar/';
    const activeTab = searchForm.getAttribute('data-tab') || 'pendientes';

    new Autocomplete({
        inputSelector: '#search-input',
        dropdownSelector: '#autocomplete-dropdown',
        listSelector: '#autocomplete-list',
        formSelector: '#search-form',
        url: searchUrl,
        getParams: () => ({
            tab: activeTab
        }),
        renderItem: (user) => {
            const stateBadge = user.is_active 
                ? `<span style="font-size:0.75rem; color:#1abc9c; background:#e8f8f5; padding:2px 6px; border-radius:10px; margin-left:8px;">Activo</span>`
                : `<span style="font-size:0.75rem; color:#e67e22; background:#fcedd8; padding:2px 6px; border-radius:10px; margin-left:8px;">Inactivo</span>`;
                
            return `
                <div style="font-weight:600; color:#2c3e50; font-size:0.9rem; display:flex; align-items:center; justify-content:space-between;">
                    <span>${user.username}</span>
                    <span style="font-size:0.75rem; color:#7f8c8d; font-weight:normal;">(${user.rol_display})</span>
                </div>
                <div style="font-size:0.8rem; color:#7f8c8d; margin-top:2px;">
                    ${user.first_name} ${user.last_name} ${stateBadge}
                </div>
            `;
        },
        onSelect: (user) => {
            const searchInput = document.getElementById('search-input');
            const dropdown = document.getElementById('autocomplete-dropdown');
            if (searchInput) searchInput.value = user.username;
            if (dropdown) dropdown.style.display = 'none';
            searchForm.submit();
        }
    });
});
