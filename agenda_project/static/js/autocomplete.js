/**
 * Autocomplete - Clase reusable para implementar comportamiento de autocompletado
 * en campos de búsqueda mediante AJAX/Fetch.
 */
class Autocomplete {
    constructor(options) {
        this.input = document.querySelector(options.inputSelector);
        this.dropdown = document.querySelector(options.dropdownSelector);
        this.list = document.querySelector(options.listSelector);
        this.form = options.formSelector ? document.querySelector(options.formSelector) : null;
        this.url = options.url;
        this.getParams = options.getParams || (() => ({}));
        this.renderItem = options.renderItem;
        this.onSelect = options.onSelect || ((item) => {
            if (this.input) this.input.value = item.value || item.username || '';
            if (this.dropdown) this.dropdown.style.display = 'none';
            if (this.form) this.form.submit();
        });
        this.debounceDelay = options.debounceDelay || 250;
        this.minChars = options.minChars || 1;
        this.debounceTimer = null;

        if (this.input && this.dropdown && this.list) {
            this.init();
        }
    }

    init() {
        // Estilos de foco del formulario contenedor
        if (this.form) {
            this.form.addEventListener('focusin', () => this.form.classList.add('focused'));
            this.form.addEventListener('focusout', () => {
                setTimeout(() => {
                    if (!this.form.contains(document.activeElement) && !this.dropdown.contains(document.activeElement)) {
                        this.dropdown.style.display = 'none';
                        this.form.classList.remove('focused');
                    }
                }, 150);
            });
        }

        // Evento de escritura
        this.input.addEventListener('input', () => {
            clearTimeout(this.debounceTimer);
            const query = this.input.value.trim();

            if (query.length < this.minChars) {
                this.dropdown.style.display = 'none';
                return;
            }

            this.debounceTimer = setTimeout(() => {
                // Combinar la query 'q' con parámetros adicionales definidos por la vista
                const queryParams = new URLSearchParams({
                    q: query,
                    ...this.getParams()
                });

                fetch(`${this.url}?${queryParams.toString()}`)
                    .then(response => {
                        if (!response.ok) throw new Error('Error en la búsqueda');
                        return response.json();
                    })
                    .then(data => {
                        this.list.innerHTML = '';
                        
                        // Soporta respuesta genérica 'results' o específica 'usuarios'
                        const items = data.results || data.usuarios || [];
                        
                        if (items.length > 0) {
                            items.forEach(item => {
                                const li = document.createElement('li');
                                li.style.padding = '10px 14px';
                                li.style.cursor = 'pointer';
                                li.style.borderBottom = '1px solid #f0f2f5';
                                li.style.transition = 'background 0.2s';
                                
                                // Renderizado dinámico provisto por la configuración del componente
                                li.innerHTML = this.renderItem(item);
                                
                                li.addEventListener('mouseover', () => li.style.backgroundColor = '#fafbfc');
                                li.addEventListener('mouseout', () => li.style.backgroundColor = 'transparent');
                                
                                li.addEventListener('click', () => {
                                    this.onSelect(item);
                                });
                                
                                this.list.appendChild(li);
                            });
                            this.dropdown.style.display = 'block';
                        } else {
                            const li = document.createElement('li');
                            li.style.padding = '12px 14px';
                            li.style.color = '#95a5a6';
                            li.style.fontSize = '0.85rem';
                            li.style.textAlign = 'center';
                            li.innerText = 'No se encontraron coincidencias';
                            this.list.appendChild(li);
                            this.dropdown.style.display = 'block';
                        }
                    })
                    .catch(err => {
                        console.error('Error autocomplete:', err);
                    });
            }, this.debounceDelay);
        });
    }
}
