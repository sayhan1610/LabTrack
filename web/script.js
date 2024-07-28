const apiBaseUrl = "http://127.0.0.1:8000";

// Function to fetch and display equipment list
async function fetchEquipments(queryParams = "") {
  try {
    const response = await fetch(`${apiBaseUrl}/equipments${queryParams}`);
    const equipments = await response.json();

    const equipmentList = document.getElementById("equipmentList");
    equipmentList.innerHTML = "";

    const expiringItems = [];
    const today = new Date();
    const twoWeeksFromNow = new Date();
    twoWeeksFromNow.setDate(today.getDate() + 14);

    equipments.forEach((equipment) => {
      const row = document.createElement("tr");

// Create individual cell elements
const idCell = document.createElement("td");
idCell.textContent = equipment.id;

const nameCell = document.createElement("td");
nameCell.textContent = equipment.name;

const typeCell = document.createElement("td");
typeCell.textContent = equipment.type;

const labCell = document.createElement("td");
labCell.textContent = equipment.lab;

const shelfCell = document.createElement("td");
shelfCell.textContent = equipment.shelf_number;

const dangerCell = document.createElement("td");
dangerCell.textContent = equipment.danger_factor;

const expiryCell = document.createElement("td");
expiryCell.textContent = equipment.expiry_date;

const countCell = document.createElement("td");
countCell.textContent = equipment.count;

// Create the checkbox and buttons
const actionsCell = document.createElement("td");

const checkbox = document.createElement("input");
checkbox.type = "checkbox";
checkbox.value = equipment.id;
checkbox.onchange = updateBulkDelete;
actionsCell.appendChild(checkbox);

const editButton = document.createElement("button");
editButton.textContent = "Edit";
editButton.onclick = () => showEditForm(equipment);
actionsCell.appendChild(editButton);

const deleteButton = document.createElement("button");
deleteButton.textContent = "Delete";
deleteButton.onclick = () => deleteEquipment(equipment.id);
actionsCell.appendChild(deleteButton);

// Append all cells to the row
row.appendChild(idCell);
row.appendChild(nameCell);
row.appendChild(typeCell);
row.appendChild(labCell);
row.appendChild(shelfCell);
row.appendChild(dangerCell);
row.appendChild(expiryCell);
row.appendChild(countCell);
row.appendChild(actionsCell);

equipmentList.appendChild(row);


      const expiryDate = new Date(equipment.expiry_date);
      if (expiryDate >= today && expiryDate <= twoWeeksFromNow) {
        expiringItems.push(equipment);
      }
    });

    if (expiringItems.length > 0) {
      showExpiryModal(expiringItems);
    }
  } catch (error) {
    console.error("Error fetching equipments:", error);
  }
}

// Function to show modal with expiring items
function showExpiryModal(expiringItems) {
  const modal = document.getElementById("expiryModal");
  const expiryList = document.getElementById("expiryList");
  expiryList.innerHTML = "";

  expiringItems.forEach((item) => {
    const listItem = document.createElement("li");
    listItem.innerText = `ID: ${item.id}, Name: ${item.name}, Expiry Date: ${item.expiry_date}`;
    expiryList.appendChild(listItem);
  });

  modal.style.display = "block";

  const closeBtn = document.getElementsByClassName("close")[0];
  closeBtn.onclick = function () {
    modal.style.display = "none";
  };

  window.onclick = function (event) {
    if (event.target == modal) {
      modal.style.display = "none";
    }
  };
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
