export async function loadCatalog() {
  const response = await fetch("../manifest.json", { cache: "no-cache" });
  if (!response.ok) throw new Error(`Catalog unavailable (${response.status})`);
  const catalog = await response.json();
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
      (!filters.category || asset.category === filters.category) &&
      (!filters.style || asset.style === filters.style) &&
      (!filters.rigged || asset.rigged)
    );
  });
}

export function assetUrl(path) {
  return new URL(`../${path}`, document.baseURI).href;
}
