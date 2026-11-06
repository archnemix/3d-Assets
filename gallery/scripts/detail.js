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
  const grid = node("div", "", "score-grid");
  for (const [label, value] of Object.entries(scores ?? {})) {
    const item = node("div", "", "score");
    item.append(
      node("strong", String(value)),
      node("span", label.replaceAll("_", " ")),
    );
    grid.append(item);
  }
  return grid;
}

function makeViewer(asset, hero, dialog) {
  const section = node("section", "", "viewer");
  const launch = node("button", "View in 3D", "viewer-launch");
  launch.type = "button";
  const hint = node(
    "p",
    "Drag to rotate · Scroll to zoom · Right-drag to pan",
    "viewer-hint",
  );
  const body = node("div", "", "viewer-body");
  body.hidden = true;
  const stage = node("div", "", "viewer-stage");
  const status = node("p", "Loading 3D model…", "viewer-status");
  status.setAttribute("role", "status");
  const tools = node("div", "", "viewer-tools");
  const modelLabel = node("label", "Model file");
  const model = node("select", "", "viewer-model");
  model.add(new Option("Original model", asset.model));
  if (asset.animated_model) {
    model.add(new Option("Animated version", asset.animated_model));
    model.value = asset.animated_model;
  }
  modelLabel.append(model);
  const clipLabel = node("label", "Animation clip");
  const clips = node("select", "", "viewer-clips");
  clips.disabled = true;
  clipLabel.append(clips);
  const play = node("button", "Pause", "viewer-play");
  play.type = "button";
  play.disabled = true;
  const reset = node("button", "Reset view", "viewer-reset");
  reset.type = "button";
  const spinLabel = node("label", "", "viewer-spin-label");
  const spin = node("input", "", "viewer-spin");
  spin.type = "checkbox";
  spinLabel.append(spin, document.createTextNode(" Auto-rotate"));
  tools.append(modelLabel, clipLabel, play, reset, spinLabel);
  body.append(stage, status, tools, hint);
  section.append(launch, body);
  let dispose = null;
  let stopped = false;
  dialog.addEventListener(
    "close",
    () => {
      stopped = true;
      if (dispose) dispose();
    },
    { once: true },
  );
  launch.addEventListener("click", async () => {
    launch.disabled = true;
    try {
      const { mountViewer } = await import("./viewer.js");
      if (stopped || !section.isConnected) return;
      hero.hidden = true;
      body.hidden = false;
      launch.hidden = true;
      dispose = mountViewer(body, asset);
    } catch (error) {
      launch.disabled = false;
      status.textContent = `3D viewer could not start: ${error.message}`;
      body.hidden = false;
    }
  });
  return section;
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
      asset.animated_model
        ? `Animated version available · ${asset.authored_animation_count} clips`
        : asset.animation_count
          ? `${asset.rigged ? "Rigged · " : ""}${asset.animation_count} clips`
          : asset.rigged
            ? "Rigged · no animation clips"
            : "Static model",
    ],
    ["Catalog status", "Approved · Inspection views available"],
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
  if (asset.animated_model)
    actions.append(
      downloadLink("Download animated version", asset.animated_model),
    );
  const sources = node("div", "", "detail-actions");
  sources.append(
    externalLink("Source", asset.source_url),
    externalLink("License evidence", asset.license_evidence),
    link("License audit", "docs/licenses.md", true),
  );
  const rights = node("div", "", "detail-rights");
  rights.append(
    node("h3", "What you may do"),
    node(
      "p",
      "Free · No attribution required · Commercial use · Use and redistribute the files as-is · Public display",
      "detail-note",
    ),
  );
  if (asset.resale_as_is) {
    rights.append(
      node("p", `Reselling the files: ${asset.resale_as_is}`, "detail-note"),
    );
  }
  for (const note of asset.license_notes ?? []) {
    rights.append(node("p", note, "detail-note"));
  }
  facts.append(
    list,
    actions,
    sources,
    rights,
    node("h3", "Review scores"),
    scoreGrid(asset.review_scores),
    node(
      "p",
      "Keep neighboring buffers and textures with the model. Engine shading and animation import behavior can vary.",
      "detail-note",
    ),
  );
  if (asset.tags?.length) {
    const tags = node("div", "", "tag-row");
    for (const tag of asset.tags) tags.append(node("span", tag, "pill"));
    facts.append(tags);
  }
  const visual = node("div", "", "detail-visual");
  visual.append(hero, makeViewer(asset, hero, dialog));
  layout.append(visual, facts);
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
