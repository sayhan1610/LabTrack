const apiBaseUrl = "http://127.0.0.1:8000";

// Function to fetch and display equipment list
async function fetchEquipments(queryParams = "") {
  try {
    const response = await fetch(`${apiBaseUrl}/equipments${queryParams}`);
    const equipments = await response.json();

    const equipmentList = document.getElementById("equipmentList");
    equipmentList.innerHTML = "";

    equipments.forEach((equipment) => {
      const row = document.createElement("tr");

      row.innerHTML = `
        <td>${equipment.id}</td>
        <td>${equipment.name}</td>
        <td>${equipment.type}</td>
        <td>${equipment.lab}</td>
        <td>${equipment.shelf_number}</td>
        <td>${equipment.danger_factor}</td>
        <td>${equipment.expiry_date}</td>
        <td>${equipment.count}</td>
        <td>
          <input type="checkbox" value="${equipment.id}" onchange="updateBulkDelete()" />
          <button onclick="showEditForm(${JSON.stringify(equipment)})">Edit</button>
          <button onclick="deleteEquipment(${equipment.id})">Delete</button>
        </td>
      `;

      equipmentList.appendChild(row);
    });
  } catch (error) {
    console.error("Error fetching equipments:", error);
  }
}

// Function to handle form submission for adding new equipment
document.getElementById("addForm").addEventListener("submit", async function (event) {
  event.preventDefault();

  const formData = new FormData(this);
  const requestData = {};
  formData.forEach((value, key) => {
    requestData[key] = value;
  });

  try {
    const response = await fetch(`${apiBaseUrl}/equipment`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(requestData),
    });

    if (response.ok) {
      await fetchEquipments();
      this.reset();
    } else {
      alert("Failed to add equipment");
    }
  } catch (error) {
    console.error("Error adding equipment:", error);
  }
});

// Function to handle form submission for searching equipment
document.getElementById("searchForm").addEventListener("submit", async function (event) {
  event.preventDefault();

  const queryParams = new URLSearchParams(new FormData(this)).toString();
  await fetchEquipments(`?${queryParams}`);
});

// Function to handle form submission for bulk adding equipment
document.getElementById("bulkAddForm").addEventListener("submit", async function (event) {
  event.preventDefault();

  const bulkData = document.getElementById("bulkData").value;

  try {
    const response = await fetch(`${apiBaseUrl}/equipments`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: bulkData,
    });

    if (response.ok) {
      await fetchEquipments();
      this.reset();
    } else {
      alert("Failed to bulk add equipment");
    }
  } catch (error) {
    console.error("Error bulk adding equipment:", error);
  }
});

// Function to handle form submission for bulk deleting equipment
document.getElementById("bulkDeleteForm").addEventListener("submit", async function (event) {
  event.preventDefault();

  const deleteIds = document.getElementById("deleteIds").value.split(",").map(id => id.trim());

  try {
    const response = await fetch(`${apiBaseUrl}/equipments`, {
      method: "DELETE",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ ids: deleteIds }),
    });

    if (response.ok) {
      await fetchEquipments();
      this.reset();
    } else {
      alert("Failed to bulk delete equipment");
    }
  } catch (error) {
    console.error("Error bulk deleting equipment:", error);
  }
});

// Function to handle form submission for editing equipment
document.getElementById("editForm").addEventListener("submit", async function (event) {
  event.preventDefault();

  const formData = new FormData(this);
  const requestData = {};
  formData.forEach((value, key) => {
    requestData[key] = value;
  });

  try {
    const response = await fetch(`${apiBaseUrl}/equipment/${requestData.id}`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(requestData),
    });

    if (response.ok) {
      await fetchEquipments();
      this.reset();
    } else {
      alert("Failed to update equipment");
    }
  } catch (error) {
    console.error("Error updating equipment:", error);
  }
});

// Function to delete equipment
async function deleteEquipment(id) {
  try {
    const response = await fetch(`${apiBaseUrl}/equipment/${id}`, {
      method: "DELETE",
    });

    if (response.ok) {
      await fetchEquipments();
    } else {
      alert("Failed to delete equipment");
    }
  } catch (error) {
    console.error("Error deleting equipment:", error);
  }
}

// Function to show edit form with pre-filled data
function showEditForm(equipment) {
  const editForm = document.getElementById("editForm");

  editForm.querySelector("#editId").value = equipment.id;
  editForm.querySelector("#editName").value = equipment.name;
  editForm.querySelector("#editCount").value = equipment.count;
  editForm.querySelector("#editType").value = equipment.type;
  editForm.querySelector("#editDangerFactor").value = equipment.danger_factor;
  editForm.querySelector("#editExpiryDate").value = equipment.expiry_date;
  editForm.querySelector("#editLab").value = equipment.lab;
  editForm.querySelector("#editShelfNumber").value = equipment.shelf_number;

  editForm.scrollIntoView({ behavior: "smooth" });
}

// Function to update bulk delete input field
function updateBulkDelete() {
  const checkboxes = document.querySelectorAll('#equipmentList input[type="checkbox"]:checked');
  const ids = Array.from(checkboxes).map(cb => cb.value);
  document.getElementById("deleteIds").value = ids.join(",");
}

// Initial fetch of equipment list
fetchEquipments();
