document.addEventListener("DOMContentLoaded", () => {
    const filters = document.querySelectorAll("#suppliers-table input");
    const tableBody = document.querySelector("#supplier-list-body");
    const paginationContainer = document.querySelector(".pagination");
    const showingSelect = document.querySelector("#showing-select"); // Obsługa pola "Pokazuje"

    const fetchFilteredData = (url = window.location.href) => {
        const params = new URLSearchParams();

        // Pobierz wartości filtrów
        filters.forEach(input => {
            if (input.value.trim() !== "") {
                params.append(input.id.replace("-filter", ""), input.value.trim());
            }
        });

        // Wyślij zapytanie AJAX
        fetch(`${url.split('?')[0]}?${params.toString()}`, {
            headers: { "X-Requested-With": "XMLHttpRequest" }
        })
            .then(response => response.json())
            .then(data => {
                tableBody.innerHTML = data.html;
                paginationContainer.innerHTML = data.pagination;
            })
            .catch(error => console.error("Error:", error));
    };


    // Obsługa filtrów
    filters.forEach(input => {
        input.addEventListener("input", () => fetchFilteredData());
    });

});


document.addEventListener('DOMContentLoaded', function () {
    const exportButton = document.getElementById('export-button');
    const filterInputs = document.querySelectorAll('#suppliers-table input');

    const updateExportUrl = () => {
        const params = new URLSearchParams();
        filterInputs.forEach(input => {
            if (input.value.trim() !== '') {
                params.append(input.id.replace('-filter', ''), input.value.trim());
            }
        });
        exportButton.href = `/suppliers/export/?${params.toString()}`; // Dynamiczny URL
    };

    filterInputs.forEach(input => {
        input.addEventListener('input', updateExportUrl);
    });

    // Aktualizuj URL eksportu przy pierwszym załadowaniu
    updateExportUrl();
});
