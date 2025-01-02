document.addEventListener("DOMContentLoaded", function () {
    const addItemButton = document.getElementById("add-item-btn");
    const tableBody = document.querySelector("#order-items-table tbody");
    const totalFormsInput = document.querySelector("#id_order_items-TOTAL_FORMS");

    // Funkcja do obsługi usuwania wiersza
    function handleRemoveButtonClick(event) {
        const removeButton = event.target.closest(".remove-item-btn");
        if (removeButton) {
            const row = removeButton.closest("tr");
            const deleteInput = row.querySelector('input[type="hidden"][name$="-DELETE"]');

            if (deleteInput) {
                // Oznacz wiersz do usunięcia w backendzie
                deleteInput.checked = true;
            }
            // Ukryj wiersz
            row.style.display = "none";
        }
    }

    // Obsługa dynamicznego dodawania wierszy
    addItemButton.addEventListener("click", function () {
        // Liczba istniejących formularzy
        const currentFormsCount = parseInt(totalFormsInput.value, 10);

        // Klonowanie pustego formularza
        const emptyForm = document.querySelector(".order-item-form").cloneNode(true);

        // Zmiana atrybutów name i id na nowe
        const newFormHTML = emptyForm.innerHTML.replace(/-0-/g, `-${currentFormsCount}-`);
        emptyForm.innerHTML = newFormHTML;

        // Wyczyszczenie wartości pól
        const inputs = emptyForm.querySelectorAll("input, select");
        inputs.forEach(input => {
            input.value = "";
            // Usuń zaznaczenie checkboxa DELETE w nowym formularzu
            if (input.type === "checkbox") {
                input.checked = false;
            }
        });

        // Dodanie nowego wiersza do tabeli
        tableBody.appendChild(emptyForm);

        // Zwiększenie liczby formularzy
        totalFormsInput.value = currentFormsCount + 1;
    });

    // Obsługa dynamicznego usuwania wierszy
    tableBody.addEventListener("click", handleRemoveButtonClick);
});
