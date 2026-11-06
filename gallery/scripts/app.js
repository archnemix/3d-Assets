import {
  loadCatalog,
  filterAssets,
  sortAssets,
  groupByCategory,
  categoryCounts,
} from "./data.js";
import { renderCards } from "./cards.js";
import { showDetail } from "./detail.js";

const byId = (id) => document.getElementById(id);
const grid = byId("asset-grid");
const dialog = byId("asset-dialog");
const detail = byId("detail-content");
const categorySelect = byId("category");
const chips = byId("category-chips");
let catalog = null;
const PAGE_SIZE = 36;
let visibleCount = PAGE_SIZE;

function stat(value, label) {
  const item = document.createElement("span");
  const number = document.createElement("strong");
  number.textContent = value;
  item.append(number, document.createTextNode(label));
  return item;
}

function renderStats() {
  byId("stats").replaceChildren(
    stat(catalog.totals.assets, "approved assets"),
    stat(catalog.totals.categories, "categories"),
    stat("12", "views per asset"),
  );
}

function addChip(value, label) {
  const chip = document.createElement("button");
  chip.type = "button";
  chip.className = "chip";
  chip.dataset.category = value;
  chip.textContent = label;
  chip.addEventListener("click", () => {
    categorySelect.value = value;
    update(true);
  });
  chips.append(chip);
}

function renderCategoryControls() {
  const selected = categorySelect.value;
  categorySelect.replaceChildren(new Option("All categories", ""));
  chips.replaceChildren();
  addChip("", `All assets (${catalog.assets.length})`);
  for (const [category, count] of categoryCounts(catalog.assets)) {
    const label = category.replaceAll("/", " / ");
    categorySelect.append(new Option(`${label} (${count})`, category));
    addChip(category, `${label} (${count})`);
  }
  categorySelect.value = [...categorySelect.options].some(
    (option) => option.value === selected,
  )
    ? selected
    : "";
}

function currentFilters() {
  return {
    query: byId("search").value,
    category: categorySelect.value,
    style: byId("style").value,
    rigged: byId("rigged").checked,
    animated: byId("animated").checked,
  };
}

function inspect(asset) {
  showDetail(dialog, detail, asset);
}

function syncChips() {
  for (const chip of chips.children) {
    chip.classList.toggle(
      "active",
      chip.dataset.category === categorySelect.value,
    );
  }
}

function update(resetPage = false) {
  if (resetPage) visibleCount = PAGE_SIZE;
  if (!catalog) return;
  const filtered = filterAssets(catalog.assets, currentFilters());
  const sorted = sortAssets(filtered, byId("sort").value);
  const visible = sorted.slice(0, visibleCount);
  grid.replaceChildren();
  grid.classList.toggle("grouped", byId("group").checked);
  if (byId("group").checked) {
    for (const [category, assets] of groupByCategory(visible)) {
      const section = document.createElement("section");
      section.className = "category-section";
      const heading = document.createElement("h2");
      heading.textContent = `${category.replaceAll("/", " / ")} · ${assets.length}`;
      const sectionGrid = document.createElement("div");
      sectionGrid.className = "asset-grid";
      renderCards(sectionGrid, assets, inspect);
      section.append(heading, sectionGrid);
      grid.append(section);
    }
  } else {
    renderCards(grid, visible, inspect);
  }
  byId("result-count").textContent =
    `Showing ${visible.length} of ${filtered.length} matching assets · ${catalog.assets.length} total`;
  byId("load-more").hidden = visible.length >= filtered.length;
  byId("empty").hidden = filtered.length > 0;
  syncChips();
}

async function refresh() {
  try {
    catalog = await loadCatalog();
    renderStats();
    renderCategoryControls();
    update();
    byId("last-updated").textContent =
      `Updated ${new Date().toLocaleTimeString()}`;
  } catch (error) {
    byId("result-count").textContent =
      `Could not load the library: ${error.message}`;
  }
}

byId("filters").addEventListener("submit", (event) => event.preventDefault());
byId("filters").addEventListener("input", () => update(true));
categorySelect.addEventListener("change", () => update(true));
byId("sort").addEventListener("change", () => update(true));
byId("group").addEventListener("change", () => update(true));
byId("reset").addEventListener("click", () => {
  byId("filters").reset();
  byId("sort").value = "title";
  byId("group").checked = false;
  update(true);
});
byId("load-more").addEventListener("click", () => {
  visibleCount += PAGE_SIZE;
  update();
});
byId("refresh").addEventListener("click", refresh);
dialog.addEventListener("click", (event) => {
  if (event.target === dialog) dialog.close();
});
document.addEventListener("visibilitychange", () => {
  if (!document.hidden) refresh();
});
setInterval(refresh, 30000);
refresh();
