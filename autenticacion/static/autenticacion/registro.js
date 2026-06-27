document.addEventListener("DOMContentLoaded", function() {
    // Configuración en común para Tom Select
    const config = {
        create: false,         // Evita que el usuario cree nuevas opciones
        sortField: {
            field: "text",
            direction: "asc"
        },
        placeholder: "-- Selecciona --"
    };

    // Inicializar ambos selects
    new TomSelect("#reg-profesor", config);
    new TomSelect("#reg-ambulatorio", config);
});
