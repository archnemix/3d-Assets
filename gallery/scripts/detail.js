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
    link("Open model", asset.model),
    link("Metadata", asset.metadata, true),
    link("Asset folder", `${asset.directory}/`, true),
  );
  facts.append(
    list,
    actions,
    node(
      "p",
      "Keep neighboring buffers and textures with the model. Engine shading and animation import behavior can vary.",
      "detail-note",
    ),
  );
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
