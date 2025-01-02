document.addEventListener("DOMContentLoaded", () => {
    const filters = document.querySelectorAll("#orders-table input");
    const tableBody = document.querySelector("#order-list-body");
    const paginationContainer = document.querySelector("#pagination-container");

    const fetchFilteredData = () => {
        const params = new URLSearchParams();

        // Pobierz wartości filtrów
        filters.forEach(input => {
            if (input.value.trim() !== "") {
                params.append(input.id.replace("-filter", ""), input.value.trim());
            }
        });

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

    filters.forEach(input => {
        input.addEventListener("input", fetchFilteredData);
    });
});
