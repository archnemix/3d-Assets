import { loadCatalog, filterAssets } from "./data.js";
import { renderCards } from "./cards.js";
import { showDetail } from "./detail.js";

const byId = (id) => document.getElementById(id);
const grid = byId("asset-grid");
const dialog = byId("asset-dialog");
const detail = byId("detail-content");

function stat(value, label) {
  const item = document.createElement("span");
  const number = document.createElement("strong");
  number.textContent = value;
  item.append(number, document.createTextNode(label));
  return item;
}

async function start() {
  const catalog = await loadCatalog();
  byId("stats").replaceChildren(
    stat(catalog.totals.assets, "reviewed assets"),
    stat(catalog.totals.categories, "categories"),
    stat("12", "views per asset"),
  );
  for (const category of Object.keys(catalog.totals.by_category)) {
    const option = document.createElement("option");
    option.value = category;
    option.textContent = category.replaceAll("/", " / ");
    byId("category").append(option);
  }
  function update() {
    const assets = filterAssets(catalog.assets, {
      query: byId("search").value,
      category: byId("category").value,
      style: byId("style").value,
      rigged: byId("rigged").checked,
    });
    renderCards(grid, assets, (asset) => showDetail(dialog, detail, asset));
    byId("result-count").textContent =
      `${assets.length} of ${catalog.assets.length} approved assets`;
    byId("empty").hidden = assets.length > 0;
  }
  byId("filters").addEventListener("submit", (event) => event.preventDefault());
  byId("filters").addEventListener("input", update);
  byId("reset").addEventListener("click", () => {
    byId("filters").reset();
    update();
  });
  dialog.addEventListener("click", (event) => {
    if (event.target === dialog) dialog.close();
  });
  update();
}

start().catch((error) => {
  byId("result-count").textContent =
    `Could not load the library: ${error.message}`;
});
