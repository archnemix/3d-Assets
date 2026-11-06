import assert from "node:assert/strict";
import { chromium } from "playwright";

const browser = await chromium.launch({
  headless: true,
  args: [
    "--enable-webgl",
    "--use-angle=swiftshader",
    "--enable-unsafe-swiftshader",
  ],
});
const page = await browser.newPage({ viewport: { width: 1360, height: 900 } });
const errors = [];
page.on("pageerror", (error) => errors.push(error.message));

try {
  await page.goto("http://127.0.0.1:8000/gallery/", {
    waitUntil: "networkidle",
  });
  await page.waitForSelector(".asset-card");
  const catalog = await page.evaluate(async () => {
    const response = await fetch("../manifest.json", { cache: "no-cache" });
    return response.json();
  });
  assert.equal(
    await page.locator("#style").inputValue(),
    "",
    "all styles selected initially",
  );
  assert.equal(
    await page.locator(".asset-card").count(),
    catalog.assets.length,
    "every approved asset has a card without pagination",
  );
  assert.match(
    await page.locator("#result-count").textContent(),
    new RegExp(
      `Showing ${catalog.assets.length} of ${catalog.assets.length} matching assets`,
    ),
  );
  assert.equal(
    await page.locator("#load-more").count(),
    0,
    "all cards are visible without a show-more button",
  );
  await page
    .locator(".asset-card")
    .first()
    .evaluate((node) => {
      node.dataset.refreshMarker = "preserved";
    });
  await Promise.all([
    page.waitForResponse((response) =>
      response.url().includes("manifest.json"),
    ),
    page.locator("#refresh").click(),
  ]);
  await page.waitForLoadState("networkidle");
  assert.equal(
    await page
      .locator(".asset-card")
      .first()
      .getAttribute("data-refresh-marker"),
    "preserved",
    "refreshing an unchanged catalog does not rebuild the grid",
  );
  await page.locator(".asset-card").last().scrollIntoViewIfNeeded();
  await page.waitForFunction(() => {
    const image = document.querySelector(".asset-card:last-child img");
    return image?.complete && image.naturalWidth > 0;
  });
  await page.locator("#search").fill("yellow submersible");
  assert.equal(
    await page.locator(".asset-card").count(),
    1,
    "new stylized asset is discoverable by default",
  );
  await page.waitForFunction(() => {
    const image = document.querySelector(".asset-card img");
    return image?.complete && image.naturalWidth > 0;
  });
  await page.locator("#style").selectOption("realistic");
  assert.equal(
    await page.locator(".asset-card").count(),
    0,
    "style filter narrows results",
  );
  await page.locator("#reset").click();
  assert.equal(
    await page.locator("#style").inputValue(),
    "",
    "reset restores all styles",
  );
  assert.equal(
    await page.locator(".asset-card").count(),
    catalog.assets.length,
    "reset restores the full catalog",
  );
  await page.setViewportSize({ width: 390, height: 844 });
  assert.equal(
    await page.evaluate(
      () => document.documentElement.scrollWidth <= innerWidth,
    ),
    true,
    "filters and cards fit a mobile viewport without horizontal overflow",
  );
  await page.setViewportSize({ width: 1360, height: 900 });
  await page.locator("#style").selectOption("");
  assert.equal(
    await page.locator("#category-chips").count(),
    0,
    "no wall of category chips",
  );
  assert.equal(
    await page.locator('#main-category option[value="buildings"]').count(),
    1,
    "main categories appear once in the selector",
  );
  assert.equal(
    await page
      .locator('#main-category option[value="buildings/modular"]')
      .count(),
    0,
    "subcategories are not duplicated as main categories",
  );
  const vehicles = catalog.assets.filter(
    (asset) => asset.category.split("/")[0] === "vehicles",
  );
  assert.ok(vehicles.length > 4, "fixture contains more than four vehicles");
  await page.locator("#main-category").selectOption("vehicles");
  assert.equal(
    await page.locator(".asset-card").count(),
    vehicles.length,
    "vehicles category includes all styles by default",
  );
  assert.match(
    await page.locator("#result-count").textContent(),
    new RegExp(
      `Showing ${vehicles.length} of ${vehicles.length} matching assets`,
    ),
    "vehicle result count matches the actual card count",
  );
  await page.locator("#style").selectOption("realistic");
  assert.equal(
    await page.locator(".asset-card").count(),
    vehicles.filter((asset) => asset.style === "realistic").length,
    "realistic-only vehicles appear only when deliberately selected",
  );
  await page.locator("#style").selectOption("");
  await page.locator("#main-category").selectOption("buildings");
  assert.match(
    await page.locator("#result-count").textContent(),
    /37 matching assets/,
    "main category includes descendants once",
  );
  await page.locator("#category").selectOption("buildings/modular");
  assert.equal(
    await page.locator(".asset-card").count(),
    3,
    "parent selection excludes child subcategory",
  );
  await page.locator("#category").selectOption("buildings/modular/industrial");
  assert.equal(
    await page.locator(".asset-card").count(),
    12,
    "child selection contains only child assets",
  );
  await page.locator("#main-category").selectOption("");
  assert.equal(await page.locator("#category").isDisabled(), true);
  await page.locator("#animated").check();
  await page.locator("#search").fill("compact electric city car");
  assert.equal(
    await page.locator(".asset-card").count(),
    1,
    "animated filter finds authored clips",
  );
  await page.locator(".detail-button").click();
  await page.getByRole("button", { name: "View in 3D" }).click();
  await page.waitForFunction(
    () =>
      document
        .querySelector(".viewer-status")
        ?.textContent.includes("clips available"),
    { timeout: 90000 },
  );
  assert.equal(await page.locator(".viewer-clips option").count(), 2);
  assert.equal(await page.locator(".viewer-stage canvas").count(), 1);
  await page.locator(".viewer-clips").selectOption({ index: 1 });
  await page.locator(".viewer-play").click();
  assert.equal(await page.locator(".viewer-play").textContent(), "Play");
  await page.locator(".viewer-reset").click();
  await page.locator(".viewer-spin").check();
  await page.locator(".viewer-model").selectOption({ index: 0 });
  await page.waitForFunction(
    () =>
      document
        .querySelector(".viewer-status")
        ?.textContent.includes("no animation clips"),
    { timeout: 90000 },
  );
  await page.locator(".close-button").click();
  await page.locator("#animated").uncheck();
  await page.locator("#search").fill("medieval arched double castle door");
  await page.locator(".detail-button").click();
  await page.getByRole("button", { name: "View in 3D" }).click();
  await page.waitForFunction(
    () =>
      document
        .querySelector(".viewer-status")
        ?.textContent.includes("no animation clips"),
    { timeout: 90000 },
  );
  await page.keyboard.press("Escape");
  assert.equal(
    await page.locator("#asset-dialog").evaluate((el) => el.open),
    false,
  );
  assert.deepEqual(errors, []);
  console.log(
    "PASS: all approved cards and previews, reset and stable refresh, category filters, animated filter, animated GLB clips, controls, static GLB switch, external-texture glTF and close/reopen",
  );
} finally {
  await browser.close();
}
