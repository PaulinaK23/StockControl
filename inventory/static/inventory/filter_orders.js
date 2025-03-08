document.addEventListener("DOMContentLoaded", () => {
    const filters = document.querySelectorAll("#orders-table input, #orders-table select"); // Pobierz pola filtrów
    const tableBody = document.querySelector("#order-list-body"); // Tylko <tbody>
    const paginationContainer = document.querySelector("#pagination-container"); // Kontener paginacji
    const exportButton = document.getElementById("export-button"); // Przycisk eksportu

    const updateExportButton = () => {
        const params = new URLSearchParams();

        // Pobierz wartości filtrów i dodaj je do URL-a eksportu
        filters.forEach(input => {
            if (input.value.trim() !== "") {
                params.append(input.id.replace("-filter", ""), input.value.trim());
            }
        });

        // **Zaktualizowany URL dla eksportu**
        exportButton.href = `/orders/export/?${params.toString()}`;
    };

    const fetchFilteredData = () => {
        const params = new URLSearchParams();

        // Pobierz wartości filtrów
        filters.forEach(input => {
            if (input.value.trim() !== "") {
                params.append(input.id.replace("-filter", ""), input.value.trim());
            }
        });

        // Wyślij zapytanie AJAX z aktualnymi filtrami
        fetch(`?${params.toString()}`, {
            headers: { "X-Requested-With": "XMLHttpRequest" }
        })
            .then(response => response.json())
            .then(data => {
                tableBody.innerHTML = data.html;
                paginationContainer.innerHTML = data.pagination;

                // Zaktualizuj przycisk eksportu po każdej zmianie filtrów
                updateExportButton();
            })
            .catch(error => console.error("Error:", error));
    };

    // Nasłuchuj zmian w polach filtrów
    filters.forEach(input => {
        input.addEventListener("input", () => {
            fetchFilteredData();
            updateExportButton();
        });
    });

    // Zainicjalizuj poprawny URL eksportu na starcie
    updateExportButton();
});
