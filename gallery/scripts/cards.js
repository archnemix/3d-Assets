import { assetUrl, hasAnimation } from "./data.js";

function element(tag, className, text) {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (text !== undefined) node.textContent = text;
  return node;
}

export function renderCards(container, assets, onInspect) {
  container.replaceChildren();
  for (const asset of assets) {
    const card = element("article", "asset-card");
    const imageButton = element("button", "card-image");
    imageButton.type = "button";
    imageButton.setAttribute("aria-label", `Inspect ${asset.title}`);
    const image = element("img");
    image.src = assetUrl(asset.preview);
    image.alt = `${asset.title}, three-quarter inspection view`;
    image.loading = "lazy";
    image.width = 640;
    image.height = 640;
    imageButton.append(image);
    imageButton.addEventListener("click", () => onInspect(asset));
    const body = element("div", "card-body");
    body.append(
      element("span", "card-category", asset.category.replaceAll("/", " / ")),
      element("h2", "", asset.title),
      element("p", "", `By ${asset.creator}`),
    );
    const meta = element("p", "card-meta");
    meta.append(
      element("span", "", `${asset.triangles.toLocaleString()} tris`),
      element(
        "span",
        "",
        hasAnimation(asset) ? "Animated" : asset.rigged ? "Rigged" : "Static",
      ),
    );
    const footer = element("div", "card-footer");
    const inspect = element("button", "detail-button", "Inspect ↗");
    inspect.type = "button";
    inspect.addEventListener("click", () => onInspect(asset));
    footer.append(element("span", "pill", asset.style), inspect);
    body.append(meta, footer);
    card.append(imageButton, body);
    container.append(card);
  }
}
