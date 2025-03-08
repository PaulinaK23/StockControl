document.addEventListener("DOMContentLoaded", function () {
    const orderTable = document.querySelector("#order-items-table tbody");
    const addItemButton = document.getElementById("add-item-btn");
    const saveOrderButton = document.getElementById("save-order-btn"); // Musi być `id="save-order-btn"`
    let totalForms = 0; // Licznik formularzy

    function addNewRow() {
        let newRow = document.createElement("tr");
        newRow.classList.add("order-item-form");

        newRow.innerHTML = `
            <td>
                <select class="form-control item-select">
                    ${getItemOptions()}
                </select>
            </td>
            <td><input type="number" class="form-control quantity-input" min="1" value="1"></td>
            <td><input type="text" class="form-control price-input" value="0.00"></td>
            <td>
                <button type="button" class="btn btn-danger btn-sm remove-item-btn">
                    <i class="bi bi-trash"></i> Usuń
                </button>
            </td>
        `;

        orderTable.appendChild(newRow);
        attachRemoveEvent(newRow);
    }

    function attachRemoveEvent(row) {
        let deleteButton = row.querySelector(".remove-item-btn");

        deleteButton.addEventListener("click", function () {
            row.remove();
            totalForms--;
        });
    }

    function getItemOptions() {
        let options = "<option value=''>Wybierz pozycję...</option>";

        fetch("/api/items/")  // 🔥 Pobieramy Items zamiast Products
            .then(response => response.json())
            .then(data => {
                data.items.forEach(item => {
                    options += `<option value="${item.itm_id}">${item.itm_name}</option>`;
                });
                document.querySelectorAll(".item-select").forEach(select => {
                    select.innerHTML = options;
                });
            })
            .catch(error => console.error("Błąd ładowania pozycji:", error));

        return options;
    }


    function getOrderData() {
        let orderItems = [];
        document.querySelectorAll(".order-item-form").forEach(row => {
            let item = row.querySelector(".item-select").value;
            let quantity = row.querySelector(".quantity-input").value;
            let price = row.querySelector(".price-input").value;

            if (item && quantity && price) {
                orderItems.push({
                    item: item,
                    quantity: quantity,
                    price: price
                });
            }
        });

        return {
            order_number: document.querySelector("#id_ord_number").value,
            order_date: document.querySelector("#id_ord_date").value,
            order_status: document.querySelector("#id_ord_statusid").value,
            warehouse: document.querySelector("#id_ord_whsid").value,
            supplier: document.querySelector("#id_ord_supid").value,
            items: orderItems
        };
    }

    saveOrderButton.addEventListener("click", function (event) {
        event.preventDefault(); // Blokujemy domyślną akcję formularza
        let orderData = getOrderData();

        fetch("/orders/add/", {  // 🔥 Poprawiony URL
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value
            },
            body: JSON.stringify(orderData)
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                window.location.href = "/orders/"; // Przekierowanie po zapisaniu
            }
        })
        .catch(error => {
            console.error("Błąd:", error);
        });
    });

    addItemButton.addEventListener("click", function () {
        addNewRow();
    });
});