import { assetUrl } from "./data.js";

const VIEWS = [
  ["orbit-00", "Front"],
  ["orbit-01", "Front-right"],
  ["orbit-02", "Right"],
  ["orbit-03", "Back-right"],
  ["orbit-04", "Back"],
  ["orbit-05", "Back-left"],
  ["orbit-06", "Left"],
  ["orbit-07", "Front-left"],
  ["top", "Top"],
  ["bottom", "Bottom"],
  ["clay", "Clay"],
  ["wireframe", "Wireframe"],
];

function node(tag, text, className) {
  const element = document.createElement(tag);
  if (text) element.textContent = text;
  if (className) element.className = className;
  return element;
}

function link(text, path, secondary = false) {
  const anchor = node("a", text, secondary ? "secondary" : "");
  anchor.href = assetUrl(path);
  anchor.target = "_blank";
  anchor.rel = "noopener";
  return anchor;
}

function externalLink(text, url) {
  const anchor = node("a", text, "secondary");
  anchor.href = url;
  anchor.target = "_blank";
  anchor.rel = "noopener";
  return anchor;
}

function downloadLink(text, path) {
  const anchor = link(text, path);
  anchor.download = path.split("/").pop();
  return anchor;
}

function scoreGrid(scores) {
  const grid = node("div", "score-grid");
  for (const [label, value] of Object.entries(scores ?? {})) {
    const item = node("div", "score");
    item.append(
      node("strong", String(value)),
      node("span", label.replaceAll("_", " ")),
    );
    grid.append(item);
  }
  return grid;
}

export function showDetail(dialog, container, asset) {
  container.replaceChildren();
  const header = node("header", "", "detail-header");
  const title = node("h2", asset.title);
  title.id = "detail-title";
  const close = node("button", "Close", "close-button");
  close.type = "button";
  close.addEventListener("click", () => dialog.close());
  header.append(title, close);
  const layout = node("div", "", "detail-layout");
  const hero = node("img", "", "detail-main-image");
  hero.src = assetUrl(asset.preview);
  hero.alt = `${asset.title}, detailed inspection render`;
  const facts = node("div", "", "detail-facts");
  const list = node("dl");
  for (const [label, value] of [
    ["Category", asset.category.replaceAll("/", " / ")],
    ["Creator", asset.creator],
    ["License", "CC0-1.0 · No attribution required"],
    ["Geometry", `${asset.triangles.toLocaleString()} triangles`],
    [
      "Textures",
      `${asset.texture_count} images · up to ${asset.max_texture_resolution}px`,
    ],
    [
      "Animation",
      asset.rigged ? `Rigged · ${asset.animation_count} clips` : "Static model",
    ],
    ["Visual review", "Approved · All 12 inspection views"],
  ]) {
    list.append(node("dt", label), node("dd", value));
  }
  const actions = node("div", "", "detail-actions");
  actions.append(
    downloadLink("Download model", asset.model),
    link("Open model", asset.model, true),
    link("Contact sheet", asset.contact_sheet, true),
    link("Metadata", asset.metadata, true),
    link("Asset folder", `${asset.directory}/`, true),
  );
  const sources = node("div", "", "detail-actions");
  sources.append(
    externalLink("Source", asset.source_url),
    externalLink("License evidence", asset.license_evidence),
  );
  facts.append(
    list,
    actions,
    sources,
    node("h3", "Review scores"),
    scoreGrid(asset.review_scores),
    node(
      "p",
      "Keep neighboring buffers and textures with the model. Engine shading and animation import behavior can vary.",
      "detail-note",
    ),
  );
  if (asset.tags?.length) {
    const tags = node("div", "tag-row");
    for (const tag of asset.tags) tags.append(node("span", tag, "pill"));
    facts.append(tags);
  }
  layout.append(hero, facts);
  const views = node("section", "", "view-section");
  views.append(node("h3", "Every side, before approval"));
  const grid = node("div", "", "view-grid");
  for (const [file, label] of VIEWS) {
    const anchor = link("", `${asset.directory}/previews/${file}.jpg`);
    const image = node("img");
    image.src = anchor.href;
    image.alt = `${asset.title}: ${label}`;
    image.loading = "lazy";
    anchor.append(image, document.createTextNode(label));
    grid.append(anchor);
  }
  views.append(grid);
  container.append(header, layout, views);
  if (!dialog.open) dialog.showModal();
}
