document.addEventListener('DOMContentLoaded', () => {
    const inputs = document.querySelectorAll('#items-table input, #items-table select');
    const tableBody = document.querySelector('#item-list-body');
    const paginationContainer = document.querySelector('#pagination-container'); // Kontener paginacji
    const exportButton = document.getElementById('export-button'); // Przycisk eksportu

    const updateExportUrl = () => {
        const params = new URLSearchParams();
        inputs.forEach(input => {
            if (input.value.trim() !== '') {
                params.append(input.id.replace('-filter', ''), input.value.trim());
            }
        });
        exportButton.href = `/items/export/?${params.toString()}`; // Dynamiczny URL eksportu
    };

    const fetchFilteredData = (url = window.location.href) => {
        const params = new URLSearchParams();
        inputs.forEach(input => {
            if (input.value.trim() !== '') {
                params.append(input.id.replace('-filter', ''), input.value.trim());
            }
        });

        fetch(`${url.split('?')[0]}?${params.toString()}`, {
            headers: { 'X-Requested-With': 'XMLHttpRequest' }
        })
            .then(response => response.json())
            .then(data => {
                tableBody.innerHTML = data.html; // Zaktualizuj tabelę
                paginationContainer.innerHTML = data.pagination; // Zaktualizuj paginację
                setupPaginationLinks(); // Ponownie zainicjalizuj paginację
                updateExportUrl(); // Zaktualizuj link eksportu
            })
            .catch(error => console.error("Error:", error));
    };

    const setupPaginationLinks = () => {
        const paginationLinks = document.querySelectorAll('#pagination-container a.page-link');
        paginationLinks.forEach(link => {
            link.addEventListener('click', (event) => {
                event.preventDefault();
                fetchFilteredData(link.href);
            });
        });
    };

    // Nasłuchuj zmian w polach filtrów
    inputs.forEach(input => {
        input.addEventListener('input', () => fetchFilteredData());
    });

    // Inicjalizuj dynamiczne linki paginacji i eksportu przy pierwszym załadowaniu
    setupPaginationLinks();
    updateExportUrl();
});
