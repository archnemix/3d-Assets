import {
  loadCatalog,
  filterAssets,
  sortAssets,
  groupByCategory,
  childCategoryCounts,
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
let catalogFingerprint = null;

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

// Paths are canonical slash-separated segments. Each selector and tile represents
// a subtree; selecting a parent includes both direct items and descendants.
let selectedCategory = "";

function categorySegment(path) {
  return categoryLabel(path.split("/").at(-1));
}

function renderCategoryControls() {
  const segments = selectedCategory ? selectedCategory.split("/") : [];
  const main = segments[0] || "";
  mainSelect.replaceChildren(new Option("All categories", ""));
  for (const [path, count] of childCategoryCounts(
    catalog.assets,
    "",
    catalog.categoryPaths,
  )) {
    mainSelect.append(new Option(`${categorySegment(path)} (${count})`, path));
  }
  mainSelect.value = main;
  const children = main
    ? childCategoryCounts(catalog.assets, main, catalog.categoryPaths)
    : new Map();
  categorySelect.replaceChildren(
    new Option(main ? "All subcategories" : "Choose a main category first", ""),
  );
  categorySelect.disabled = !main || children.size === 0;
  for (const [path, count] of children) {
    categorySelect.append(
      new Option(`${categorySegment(path)} (${count})`, path),
    );
  }
  categorySelect.value =
    segments.length > 1 ? segments.slice(0, 2).join("/") : "";

  const levels = byId("category-levels");
  levels.replaceChildren();
  for (let depth = 2; depth <= segments.length; depth++) {
    const parent = segments.slice(0, depth).join("/");
    const options = childCategoryCounts(
      catalog.assets,
      parent,
      catalog.categoryPaths,
    );
    if (!options.size) break;
    const label = document.createElement("label");
    const caption = document.createElement("span");
    caption.textContent = `Level ${depth + 1}`;
    const select = document.createElement("select");
    select.setAttribute("aria-label", `Category level ${depth + 1}`);
    select.dataset.categoryLevel = String(depth + 1);
    select.append(new Option("All within this category", ""));
    for (const [path, count] of options) {
      select.append(new Option(`${categorySegment(path)} (${count})`, path));
    }
    select.value =
      segments.length > depth ? segments.slice(0, depth + 1).join("/") : "";
    select.addEventListener("change", () =>
      selectCategory(select.value || parent),
    );
    label.append(caption, select);
    levels.append(label);
  }
  renderCategoryBrowser();
}

function selectCategory(path) {
  selectedCategory = path;
  renderCategoryControls();
  update();
}

function renderCategoryBrowser() {
  const browser = byId("category-browser");
  browser.hidden = !selectedCategory;
  if (!selectedCategory) return;
  const breadcrumb = byId("category-breadcrumb");
  breadcrumb.replaceChildren();
  const root = document.createElement("button");
  root.type = "button";
  root.textContent = "All categories";
  root.addEventListener("click", () => selectCategory(""));
  breadcrumb.append(root);
  const segments = selectedCategory.split("/");
  segments.forEach((segment, index) => {
    const path = segments.slice(0, index + 1).join("/");
    breadcrumb.append(document.createTextNode(" / "));
    const button = document.createElement("button");
    button.type = "button";
    button.textContent = categoryLabel(segment);
    if (path === selectedCategory) button.setAttribute("aria-current", "page");
    button.addEventListener("click", () => selectCategory(path));
    breadcrumb.append(button);
  });
  const list = byId("category-children");
  list.replaceChildren();
  const children = childCategoryCounts(
    catalog.assets,
    selectedCategory,
    catalog.categoryPaths,
  );
  const direct = catalog.assets.filter(
    (asset) => asset.category === selectedCategory,
  ).length;
  if (children.size) {
    for (const [path, count] of children) {
      const button = document.createElement("button");
      button.type = "button";
      button.className = "category-child";
      button.textContent = `${categorySegment(path)} · ${count}`;
      button.addEventListener("click", () => selectCategory(path));
      list.append(button);
    }
    if (direct) {
      const note = document.createElement("span");
      note.className = "category-direct";
      note.textContent = `${direct} additional item${direct === 1 ? "" : "s"} directly in this category`;
      list.append(note);
    }
  } else {
    list.textContent = "No deeper categories";
  }
}

function currentFilters() {
  return {
    query: byId("search").value,
    category: selectedCategory,
    style: byId("style").value,
    rigged: byId("rigged").checked,
    animated: byId("animated").checked,
  };
}

function inspect(asset) {
  showDetail(dialog, detail, asset);
}

function update() {
  if (!catalog) return;
  const filtered = filterAssets(catalog.assets, currentFilters());
  const sorted = sortAssets(filtered, byId("sort").value);
  const visible = sorted;
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
  byId("empty").hidden = filtered.length > 0;
}

async function refresh() {
  try {
    const nextCatalog = await loadCatalog();
    const fingerprint = JSON.stringify(nextCatalog);
    if (fingerprint !== catalogFingerprint) {
      catalog = nextCatalog;
      catalogFingerprint = fingerprint;
      renderStats();
      renderCategoryControls();
      update();
    }
    byId("last-updated").textContent =
      `Updated ${new Date().toLocaleTimeString()}`;
  } catch (error) {
    byId("result-count").textContent =
      `Could not load the library: ${error.message}`;
  }
}

byId("filters").addEventListener("submit", (event) => event.preventDefault());
byId("filters").addEventListener("input", () => update());
mainSelect.addEventListener("change", () => selectCategory(mainSelect.value));
categorySelect.addEventListener("change", () =>
  selectCategory(categorySelect.value || mainSelect.value),
);
byId("sort").addEventListener("change", () => update());
byId("group").addEventListener("change", () => update());
byId("reset").addEventListener("click", () => {
  byId("filters").reset();
  selectedCategory = "";
  renderCategoryControls();
  byId("sort").value = "title";
  byId("group").checked = false;
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
