document.addEventListener("DOMContentLoaded", () => {
    const filters = document.querySelectorAll("#stocks-table input"); // Pobierz pola filtrów
    const tableBody = document.querySelector("#stock-list-body"); // Tylko <tbody>
    const paginationContainer = document.querySelector('#pagination-container'); // Kontener paginacji

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
            })
            .catch(error => console.error("Error:", error));
    };

    // Nasłuchuj zmian w polach filtrów
    filters.forEach(input => {
        input.addEventListener("input", fetchFilteredData);
    });
});
