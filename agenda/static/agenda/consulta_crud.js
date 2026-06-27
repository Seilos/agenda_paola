document.addEventListener('DOMContentLoaded', function() {
    // 1. Autocompletado para Paciente
    const pacienteInput = document.getElementById('paciente-search');
    if (pacienteInput) {
        const url = pacienteInput.getAttribute('data-url') || '/agenda/pacientes/buscar/';
        new Autocomplete({
            inputSelector: '#paciente-search',
            dropdownSelector: '#paciente-dropdown',
            listSelector: '#paciente-list',
            url: url,
            renderItem: (paciente) => {
                return `
                    <div style="font-weight: 600; color: var(--secondary-color); font-size: 0.9rem;">
                        ${paciente.nombre}
                    </div>
                `;
            },
            onSelect: (paciente) => {
                const hiddenInput = document.getElementById('id_nombre_id');
                if (hiddenInput) hiddenInput.value = paciente.id;
                pacienteInput.value = paciente.nombre;
                const dropdown = document.getElementById('paciente-dropdown');
                if (dropdown) dropdown.style.display = 'none';
            }
        });
    }

    // 2. Autocompletado para Profesor
    const profesorInput = document.getElementById('profesor-search');
    if (profesorInput) {
        const url = profesorInput.getAttribute('data-url') || '/agenda/usuarios/buscar/';
        new Autocomplete({
            inputSelector: '#profesor-search',
            dropdownSelector: '#profesor-dropdown',
            listSelector: '#profesor-list',
            url: url,
            getParams: () => ({
                tab: 'todos', // O el rol del profesor si se requiere filtrar en la vista
                rol: 'PROFESOR'
            }),
            renderItem: (profesor) => {
                return `
                    <div style="font-weight: 600; color: var(--secondary-color); font-size: 0.9rem;">
                        ${profesor.first_name} ${profesor.last_name}
                    </div>
                    <div style="font-size: 0.8rem; color: var(--text-muted); margin-top: 2px;">
                        @${profesor.username}
                    </div>
                `;
            },
            onSelect: (profesor) => {
                const hiddenInput = document.getElementById('id_profesor_id');
                if (hiddenInput) hiddenInput.value = profesor.id;
                profesorInput.value = `${profesor.first_name} ${profesor.last_name}`;
                const dropdown = document.getElementById('profesor-dropdown');
                if (dropdown) dropdown.style.display = 'none';
            }
        });
    }

    // 3. Toggle de Fecha de Próxima Consulta basado en el Checkbox de Seguimiento
    const checkbox = document.getElementById('id_requiere_seguimiento');
    const dateContainer = document.getElementById('fecha-consulta-container');
    if (checkbox && dateContainer) {
        checkbox.addEventListener('change', function() {
            if (checkbox.checked) {
                dateContainer.classList.add('visible');
            } else {
                dateContainer.classList.remove('visible');
            }
        });

        // Estado inicial
        if (checkbox.checked) {
            dateContainer.classList.add('visible');
        }
    }
});

