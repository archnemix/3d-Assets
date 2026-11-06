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
  assert.equal(
    await page.locator("#style").inputValue(),
    "realistic",
    "realistic style selected initially",
  );
  assert.equal(
    await page.locator(".asset-card").count(),
    36,
    "initial page is bounded",
  );
  await page.locator("#load-more").click();
  assert.equal(
    await page.locator(".asset-card").count(),
    72,
    "show more expands the page",
  );
  await page.locator("#style").selectOption("");
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
  await page.locator("#category").selectOption("");
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
    "PASS: default realistic style, exact subcategory filters, pagination, animated filter, animated GLB clips, controls, static GLB switch, external-texture glTF and close/reopen",
  );
} finally {
  await browser.close();
}
