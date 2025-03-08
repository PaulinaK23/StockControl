document.addEventListener("DOMContentLoaded", function () {
    const orderTable = document.querySelector("#order-items-table tbody");
    const addItemButton = document.getElementById("add-item-btn");
    const editOrderForm = document.getElementById("edit-order-form");
    const totalFormsInput = document.querySelector("#id_form-TOTAL_FORMS");

    if (!editOrderForm) {
        console.error("🚨 Błąd: Nie znaleziono formularza edycji zamówienia!");
        return;
    }

    let totalForms = totalFormsInput ? parseInt(totalFormsInput.value) : 0;
    const orderId = editOrderForm.getAttribute("data-order-id");

    console.log(`📌 Order ID: ${orderId}`); // 🔍 Debugowanie ID zamówienia

    if (!orderId) {
        console.error("🚨 Błąd: Brak `orderId` w `edit_order.html`!");
        return;
    }

    // ✅ Funkcja dodająca nowy wiersz
    function addNewRow(itemId = "", quantity = 1, price = 0.00) {
        const newRow = document.createElement("tr");
        newRow.classList.add("order-item-form");

        const formIndex = totalForms;
        totalForms++;

        newRow.innerHTML = `
            <td>
                <select name="form-${formIndex}-oit_itmid" class="form-control item-select">
                    ${getItemOptions(itemId)}
                </select>
            </td>
            <td>
                <input type="number" name="form-${formIndex}-oit_quantity" class="form-control quantity-input" min="1" value="${quantity}">
            </td>
            <td>
                <input type="text" name="form-${formIndex}-oit_price" class="form-control price-input" value="${price.toFixed(2)}">
            </td>
            <td>
                <input type="checkbox" name="form-${formIndex}-DELETE" class="delete-checkbox" style="display: none;">
                <button type="button" class="btn btn-danger btn-sm remove-item-btn">
                    <i class="bi bi-trash"></i> Usuń
                </button>
            </td>
        `;

        orderTable.appendChild(newRow);
        attachRemoveEvent(newRow);
        if (totalFormsInput) {
            totalFormsInput.value = totalForms;
        }
    }

    // ✅ Funkcja dołączająca obsługę usuwania wiersza
    function attachRemoveEvent(row) {
        const deleteButton = row.querySelector(".remove-item-btn");
        const deleteCheckbox = row.querySelector(".delete-checkbox");

        deleteButton.addEventListener("click", function () {
            if (deleteCheckbox) {
                deleteCheckbox.checked = true;
            }
            row.style.display = "none"; // Ukryj wiersz zamiast go usuwać
        });
    }

    // ✅ Funkcja pobierająca opcje produktów
    function getItemOptions(selectedItemId = "") {
        let options = "<option value=''>Wybierz produkt...</option>";

        fetch("/api/items/")
            .then(response => response.json())
            .then(data => {
                data.items.forEach(item => {
                    const isSelected = item.itm_id == selectedItemId ? "selected" : "";
                    options += `<option value="${item.itm_id}" ${isSelected}>${item.itm_name}</option>`;
                });

                document.querySelectorAll(".item-select").forEach(select => {
                    if (!select.value) {
                        select.innerHTML = options;
                    }
                });
            })
            .catch(error => console.error("🚨 Błąd ładowania produktów:", error));

        return options;
    }

    // ✅ Funkcja pobierająca dane z formularza
    function getOrderData() {
        let orderItems = [];
        document.querySelectorAll(".order-item-form").forEach(row => {
            let item = row.querySelector(".item-select").value.trim();
            let quantity = row.querySelector(".quantity-input").value.trim();
            let price = row.querySelector(".price-input").value.trim();

            if (item && quantity && price) {
                orderItems.push({
                    item: item,
                    quantity: parseInt(quantity),
                    price: parseFloat(price.replace(",", ".")) // Zamiana , na . dla poprawnej liczby
                });
            }
        });

        let orderDateInput = document.querySelector("#id_ord_date")?.value || "";
        let formattedOrderDate = orderDateInput.split(" ")[0]; // Usuwa godzinę

        let orderData = {
            order_id: orderId,
            order_number: document.querySelector("#id_ord_number")?.value || "",
            order_date: formattedOrderDate,
            order_status: document.querySelector("#id_ord_statusid")?.value || "",
            warehouse: document.querySelector("#id_ord_whsid")?.value || "",
            supplier: document.querySelector("#id_ord_supid")?.value || "",
            items: orderItems
        };

        console.log("📋 Dane zamówienia:", orderData);
        return orderData;
    }

    // ✅ Obsługa wysyłania formularza
    editOrderForm.addEventListener("submit", function (event) {
        event.preventDefault();

        console.log("📤 Wysyłanie formularza edycji zamówienia...");

        const orderData = getOrderData();

        fetch(`/orders/${orderId}/edit/`, {
            method: "POST",
            body: JSON.stringify(orderData),
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value,
            },
        })
        .then(response => response.json())
        .then(data => {
            console.log("✅ Otrzymana odpowiedź JSON:", data);

            if (data.success) {
                console.log("✅ Zamówienie zostało zapisane poprawnie.");
                window.location.href = "/orders/";
            } else {
                console.error("🚨 Błąd walidacji:", JSON.stringify(data.errors, null, 2));
                alert("Błąd zapisu! Sprawdź formularz.");
            }
        })
        .catch(error => {
            console.error("🚨 Błąd podczas zapisywania:", error);
            alert("Wystąpił błąd podczas zapisu zamówienia. Sprawdź konsolę.");
        });
    });
});
