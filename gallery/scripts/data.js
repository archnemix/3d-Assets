export async function loadCatalog() {
  const [response, taxonomyResponse] = await Promise.all([
    fetch(`../manifest.json?ts=${Date.now()}`, { cache: "no-cache" }),
    fetch(`../config/categories.json?ts=${Date.now()}`, { cache: "no-cache" }),
  ]);
  if (!response.ok) throw new Error(`Catalog unavailable (${response.status})`);
  if (!taxonomyResponse.ok)
    throw new Error(`Categories unavailable (${taxonomyResponse.status})`);
  const catalog = await response.json();
  catalog.categoryPaths = Object.keys(await taxonomyResponse.json());
  if (catalog.schema_version !== 1 || !Array.isArray(catalog.assets)) {
    throw new Error("Unsupported catalog format");
  }
  return catalog;
}

export function filterAssets(assets, filters) {
  const query = filters.query.trim().toLowerCase();
  return assets.filter((asset) => {
    const text = [asset.title, asset.creator, asset.category, ...asset.tags]
      .join(" ")
      .toLowerCase();
    return (
      (!query || text.includes(query)) &&
      (!filters.mainCategory ||
        asset.category.split("/")[0] === filters.mainCategory) &&
      (!filters.category ||
        asset.category === filters.category ||
        asset.category.startsWith(`${filters.category}/`)) &&
      (!filters.style || asset.style === filters.style) &&
      (!filters.rigged || asset.rigged) &&
      (!filters.animated || hasAnimation(asset))
    );
  });
}

export function hasAnimation(asset) {
  return Boolean(
    asset.animation_count > 0 ||
      asset.authored_animation_count > 0 ||
      asset.animated_model,
  );
}

export function sortAssets(assets, sort) {
  const items = [...assets];
  const byTitle = (a, b) => a.title.localeCompare(b.title);
  if (sort === "category") {
    return items.sort(
      (a, b) => a.category.localeCompare(b.category) || byTitle(a, b),
    );
  }
  if (sort === "triangles-asc") {
    return items.sort((a, b) => a.triangles - b.triangles || byTitle(a, b));
  }
  if (sort === "triangles-desc") {
    return items.sort((a, b) => b.triangles - a.triangles || byTitle(a, b));
  }
  return items.sort(byTitle);
}

export function groupByCategory(assets) {
  const groups = new Map();
  for (const asset of sortAssets(assets, "category")) {
    if (!groups.has(asset.category)) groups.set(asset.category, []);
    groups.get(asset.category).push(asset);
  }
  return groups;
}

export function categoryCounts(assets) {
  const counts = new Map();
  for (const asset of assets) {
    counts.set(asset.category, (counts.get(asset.category) ?? 0) + 1);
  }
  return new Map([...counts.entries()].sort(([a], [b]) => a.localeCompare(b)));
}

export function assetUrl(path) {
  return new URL(`../${path}`, document.baseURI).href;
}

// A main category is a navigation group, not another asset classification.
export function mainCategoryCounts(assets) {
  const counts = new Map();
  for (const asset of assets) {
    const main = asset.category.split("/")[0];
    counts.set(main, (counts.get(main) ?? 0) + 1);
  }
  return new Map([...counts.entries()].sort(([a], [b]) => a.localeCompare(b)));
}

// Return only immediate children, counting all descendants once. Segment
// boundaries prevent e.g. chairs from including chairs-extra.
export function childCategoryCounts(assets, parent = "", declaredPaths = []) {
  const counts = new Map();
  for (const asset of assets) {
    const parts = asset.category.split("/");
    const prefix = parent ? parent.split("/") : [];
    if (
      parts.length <= prefix.length ||
      prefix.some((part, i) => parts[i] !== part)
    )
      continue;
    const path = parts.slice(0, prefix.length + 1).join("/");
    counts.set(path, (counts.get(path) ?? 0) + 1);
  }
  for (const category of declaredPaths) {
    const parts = category.split("/");
    const prefix = parent ? parent.split("/") : [];
    if (
      parts.length <= prefix.length ||
      prefix.some((part, i) => parts[i] !== part)
    )
      continue;
    const path = parts.slice(0, prefix.length + 1).join("/");
    if (!counts.has(path)) counts.set(path, 0);
  }
  return new Map([...counts.entries()].sort(([a], [b]) => a.localeCompare(b)));
}
