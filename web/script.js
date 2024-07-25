const apiBaseUrl = "http://127.0.0.1:8000";

// Function to fetch and display equipment list
async function fetchEquipments(queryParams = "") {
  try {
    const response = await fetch(`${apiBaseUrl}/equipments${queryParams}`);
    const equipments = await response.json();

    const equipmentList = document.getElementById("equipmentList");
    equipmentList.innerHTML = "";

    equipments.forEach((equipment) => {
      const listItem = document.createElement("li");
      listItem.textContent = `ID: ${equipment.id} - ${equipment.name} - ${equipment.type} - ${equipment.lab} - ${equipment.shelf_number} - ${equipment.danger_factor} - ${equipment.expiry_date} (Count: ${equipment.count})`;

      // Add a checkbox for bulk delete
      const checkbox = document.createElement("input");
      checkbox.type = "checkbox";
      checkbox.value = equipment.id;
      checkbox.onchange = updateBulkDelete;
      listItem.appendChild(checkbox);

      // Add buttons for edit and delete
      const editButton = document.createElement("button");
      editButton.textContent = "Edit";
      editButton.onclick = () => showEditForm(equipment);
      listItem.appendChild(editButton);

      const deleteButton = document.createElement("button");
      deleteButton.textContent = "Delete";
      deleteButton.onclick = () => deleteEquipment(equipment.id);
      listItem.appendChild(deleteButton);

      equipmentList.appendChild(listItem);
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

// Function to handle form submission for bulk adding equipment
document.getElementById("bulkAddForm").addEventListener("submit", async function (event) {
  event.preventDefault();

  const bulkData = document.getElementById("bulkData").value.trim();
  if (!bulkData) {
    alert("Please enter valid JSON data.");
    return;
  }

  try {
    const response = await fetch(`${apiBaseUrl}/bulk_add`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: bulkData,
    });

    if (response.ok) {
      await fetchEquipments();
      document.getElementById("bulkData").value = ""; // Clear the input after successful bulk add
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

  const deleteIds = document.getElementById("deleteIds").value.trim();
  if (!deleteIds) {
    alert("Please enter equipment IDs to delete.");
    return;
  }

  try {
    const response = await fetch(`${apiBaseUrl}/bulk_remove`, {
      method: "DELETE",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(deleteIds.split(",").map((id) => id.trim())),
    });

    if (response.ok) {
      await fetchEquipments();
      document.getElementById("deleteIds").value = ""; // Clear the input after successful bulk delete
    } else {
      alert("Failed to bulk delete equipment");
    }
  } catch (error) {
    console.error("Error bulk deleting equipment:", error);
  }
});

// Function to show edit form with pre-filled data and scroll to it
function showEditForm(equipment) {
  document.getElementById("editId").value = equipment.id;
  document.getElementById("editName").value = equipment.name;
  document.getElementById("editCount").value = equipment.count;
  document.getElementById("editType").value = equipment.type;
  document.getElementById("editDangerFactor").value = equipment.danger_factor;
  document.getElementById("editExpiryDate").value = equipment.expiry_date || "";
  document.getElementById("editLab").value = equipment.lab;
  document.getElementById("editShelfNumber").value = equipment.shelf_number;

  // Show the edit form and scroll to it
  const editForm = document.getElementById("editForm");
  editForm.style.display = "block";
  editForm.scrollIntoView({ behavior: "smooth" });
}

// Function to handle form submission for editing equipment
document.getElementById("editForm").addEventListener("submit", async function (event) {
  event.preventDefault();

  const formData = new FormData(this);
  const requestData = {};
  formData.forEach((value, key) => {
    requestData[key] = value;
  });

  try {
    const id = document.getElementById("editId").value;
    const response = await fetch(`${apiBaseUrl}/equipment/${id}`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(requestData),
    });

    if (response.ok) {
      await fetchEquipments();
      document.getElementById("editForm").style.display = "none"; // Hide the edit form after successful update
    } else {
      alert("Failed to update equipment");
    }
  } catch (error) {
    console.error("Error updating equipment:", error);
  }
});

// Function to handle deleting equipment
async function deleteEquipment(id) {
  try {
    const response = await fetch(`${apiBaseUrl}/equipment/${id}`, {
      method: "DELETE",
    });

    if (response.ok) {
      await fetchEquipments();
    } else {
      alert(`Failed to delete equipment with ID: ${id}`);
    }
  } catch (error) {
    console.error("Error deleting equipment:", error);
  }
}

// Function to update the bulk delete IDs based on checked checkboxes
function updateBulkDelete() {
  const checkboxes = document.querySelectorAll("#equipmentList input[type='checkbox']");
  const selectedIds = Array.from(checkboxes)
    .filter((checkbox) => checkbox.checked)
    .map((checkbox) => checkbox.value)
    .join(",");

  document.getElementById("deleteIds").value = selectedIds;
}

// Function to handle search form submission
document.getElementById("searchForm").addEventListener("submit", function (event) {
  event.preventDefault();

  const formData = new FormData(this);
  const queryParams = new URLSearchParams();
  formData.forEach((value, key) => {
    if (value.trim() !== "") {
      queryParams.append(key, value);
    }
  });

  fetchEquipments(`?${queryParams.toString()}`);
});

// Initial fetch of equipment list on page load
fetchEquipments();
