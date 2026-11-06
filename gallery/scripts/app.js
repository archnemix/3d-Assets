import {
  loadCatalog,
  filterAssets,
  sortAssets,
  groupByCategory,
  categoryCounts,
  mainCategoryCounts,
} from "./data.js";
import { renderCards } from "./cards.js";
import { showDetail } from "./detail.js";

const byId = (id) => document.getElementById(id);
const grid = byId("asset-grid");
const dialog = byId("asset-dialog");
const detail = byId("detail-content");
const categorySelect = byId("category");
const mainSelect = byId("main-category");
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

function categoryLabel(value) {
  return value
    .replaceAll("-", " ")
    .replaceAll("/", " / ")
    .replace(/^./, (c) => c.toUpperCase());
}

function renderSubcategories(selected = "") {
  const main = mainSelect.value;
  categorySelect.replaceChildren(
    new Option(main ? "All subcategories" : "Choose a main category first", ""),
  );
  categorySelect.disabled = !main;
  if (main) {
    for (const [category, count] of categoryCounts(catalog.assets)) {
      if (category.split("/")[0] !== main) continue;
      const rest = category.split("/").slice(1).join("/") || "General";
      categorySelect.append(
        new Option(`${categoryLabel(rest)} (${count})`, category),
      );
    }
  }
  categorySelect.value = [...categorySelect.options].some(
    (option) => option.value === selected,
  )
    ? selected
    : "";
}

function renderCategoryControls() {
  const selectedMain = mainSelect.value;
  const selectedSubcategory = categorySelect.value;
  mainSelect.replaceChildren(new Option("All categories", ""));
  for (const [category, count] of mainCategoryCounts(catalog.assets)) {
    const label = categoryLabel(category);
    mainSelect.append(new Option(`${label} (${count})`, category));
  }
  mainSelect.value = [...mainSelect.options].some(
    (option) => option.value === selectedMain,
  )
    ? selectedMain
    : "";
  renderSubcategories(selectedSubcategory);
}

function currentFilters() {
  return {
    query: byId("search").value,
    mainCategory: mainSelect.value,
    category: categorySelect.value,
    style: byId("style").value,
    rigged: byId("rigged").checked,
    animated: byId("animated").checked,
  };
}

function inspect(asset) {
  showDetail(dialog, detail, asset);
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
mainSelect.addEventListener("change", () => {
  renderSubcategories();
  update(true);
});
categorySelect.addEventListener("change", () => update(true));
byId("sort").addEventListener("change", () => update(true));
byId("group").addEventListener("change", () => update(true));
byId("reset").addEventListener("click", () => {
  byId("filters").reset();
  renderSubcategories();
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
