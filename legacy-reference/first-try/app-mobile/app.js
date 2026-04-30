const STORAGE_KEY = "time_entries_v1";

const form = document.getElementById("entryForm");
const dateInput = document.getElementById("date");
const projectInput = document.getElementById("project");
const hoursInput = document.getElementById("hours");
const noteInput = document.getElementById("note");
const tableBody = document.getElementById("entriesTableBody");
const totalHoursLabel = document.getElementById("totalHours");
const clearAllButton = document.getElementById("clearAll");
const exportCsvButton = document.getElementById("exportCsv");

const today = new Date().toISOString().split("T")[0];
dateInput.value = today;

function loadEntries() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    return raw ? JSON.parse(raw) : [];
  } catch {
    return [];
  }
}

let entries = loadEntries();

function saveEntries() {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(entries));
}

function formatHours(value) {
  return Number(value).toFixed(2);
}

function calculateTotalHours() {
  const total = entries.reduce((sum, item) => sum + Number(item.hours), 0);
  totalHoursLabel.textContent = formatHours(total);
}

function renderTable() {
  tableBody.innerHTML = "";

  const sorted = [...entries].sort((a, b) => a.date.localeCompare(b.date));

  sorted.forEach((entry) => {
    const row = document.createElement("tr");

    row.innerHTML = `
      <td>${entry.date}</td>
      <td>${entry.project}</td>
      <td>${formatHours(entry.hours)}</td>
      <td>${entry.note || "-"}</td>
      <td><button class="small-btn danger" data-id="${entry.id}">X</button></td>
    `;

    tableBody.appendChild(row);
  });

  calculateTotalHours();
}

form.addEventListener("submit", (event) => {
  event.preventDefault();

  const entry = {
    id: crypto.randomUUID(),
    date: dateInput.value,
    project: projectInput.value.trim(),
    hours: Number(hoursInput.value),
    note: noteInput.value.trim()
  };

  if (!entry.date || !entry.project || !entry.hours) {
    return;
  }

  entries.push(entry);
  saveEntries();
  renderTable();

  projectInput.value = "";
  hoursInput.value = "";
  noteInput.value = "";
  projectInput.focus();
});

tableBody.addEventListener("click", (event) => {
  const target = event.target;

  if (!(target instanceof HTMLButtonElement)) {
    return;
  }

  const id = target.dataset.id;
  if (!id) {
    return;
  }

  entries = entries.filter((entry) => entry.id !== id);
  saveEntries();
  renderTable();
});

clearAllButton.addEventListener("click", () => {
  const confirmDelete = window.confirm("Wirklich alle Einträge löschen?");
  if (!confirmDelete) {
    return;
  }

  entries = [];
  saveEntries();
  renderTable();
});

function escapeCsvValue(value) {
  const stringValue = String(value ?? "");
  return `"${stringValue.replaceAll('"', '""')}"`;
}

exportCsvButton.addEventListener("click", () => {
  if (entries.length === 0) {
    return;
  }

  const header = ["Datum", "Projekt", "Stunden", "Notiz"];
  const lines = [header.join(",")];

  const sorted = [...entries].sort((a, b) => a.date.localeCompare(b.date));
  sorted.forEach((entry) => {
    const row = [
      escapeCsvValue(entry.date),
      escapeCsvValue(entry.project),
      escapeCsvValue(formatHours(entry.hours)),
      escapeCsvValue(entry.note)
    ];
    lines.push(row.join(","));
  });

  const csvContent = lines.join("\n");
  const blob = new Blob([csvContent], { type: "text/csv;charset=utf-8;" });
  const url = URL.createObjectURL(blob);

  const link = document.createElement("a");
  link.href = url;
  link.download = "stunden.csv";
  link.click();

  URL.revokeObjectURL(url);
});

renderTable();
