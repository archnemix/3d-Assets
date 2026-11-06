import assert from "node:assert/strict";
import test from "node:test";

import {
  filterAssets,
  sortAssets,
  groupByCategory,
  categoryCounts,
} from "../gallery/scripts/data.js";

const assets = [
  {
    title: "Victorian armchair",
    creator: "Poly Haven",
    category: "furniture/chairs",
    tags: ["chair", "victorian"],
    style: "realistic",
    rigged: false,
  },
  {
    title: "KayKit knight",
    creator: "Kay Lousberg",
    category: "characters/humans",
    tags: ["human", "knight"],
    style: "stylized",
    rigged: true,
  },
];

const sortable = [
  { title: "B", category: "furniture/chairs", triangles: 30 },
  { title: "A", category: "characters/humans", triangles: 10 },
  { title: "C", category: "furniture/chairs", triangles: 20 },
];

test("search matches title, creator, category and tags", () => {
  assert.equal(
    filterAssets(assets, {
      query: "victorian",
      category: "",
      style: "",
      rigged: false,
    }).length,
    1,
  );
  assert.equal(
    filterAssets(assets, {
      query: "kay lousberg",
      category: "",
      style: "",
      rigged: false,
    }).length,
    1,
  );
  assert.equal(
    filterAssets(assets, {
      query: "humans",
      category: "",
      style: "",
      rigged: false,
    }).length,
    1,
  );
});

test("category, style and rig filters compose", () => {
  assert.equal(
    filterAssets(assets, {
      query: "",
      category: "characters/humans",
      style: "stylized",
      rigged: true,
    }).length,
    1,
  );
  assert.equal(
    filterAssets(assets, {
      query: "",
      category: "furniture/chairs",
      style: "stylized",
      rigged: false,
    }).length,
    0,
  );
});

test("empty query returns all assets", () => {
  assert.equal(
    filterAssets(assets, {
      query: "   ",
      category: "",
      style: "",
      rigged: false,
    }).length,
    2,
  );
});

test("sort by title, category and triangles", () => {
  assert.deepEqual(
    sortAssets(sortable, "title").map((a) => a.title),
    ["A", "B", "C"],
  );
  assert.deepEqual(
    sortAssets(sortable, "category").map((a) => a.title),
    ["A", "B", "C"],
  );
  assert.deepEqual(
    sortAssets(sortable, "triangles-asc").map((a) => a.triangles),
    [10, 20, 30],
  );
  assert.deepEqual(
    sortAssets(sortable, "triangles-desc").map((a) => a.triangles),
    [30, 20, 10],
  );
});

test("group by category keeps categories sorted", () => {
  const groups = groupByCategory(sortable);
  assert.deepEqual(
    [...groups.keys()],
    ["characters/humans", "furniture/chairs"],
  );
  assert.equal(groups.get("furniture/chairs").length, 2);
});

test("category counts summarize the visible library", () => {
  const counts = categoryCounts(sortable);
  assert.equal(counts.get("furniture/chairs"), 2);
  assert.equal(counts.get("characters/humans"), 1);
});

test("manifest carries per-asset license rights and caveats", async () => {
  const { readFile } = await import("node:fs/promises");
  const catalog = JSON.parse(
    await readFile(new URL("../manifest.json", import.meta.url), "utf8"),
  );
  assert.ok(catalog.assets.length > 0);
  for (const asset of catalog.assets) {
    assert.equal(asset.license, "CC0-1.0", asset.id);
    assert.match(asset.license_evidence, /^https:\/\//, asset.id);
    assert.ok(Array.isArray(asset.license_notes), asset.id);
    assert.ok(asset.resale_as_is.length > 20, asset.id);
  }
  // The author's request outranks the license: no KayKit asset may be published.
  assert.equal(
    catalog.assets.filter((a) => a.id.startsWith("kaykit-")).length,
    0,
    "KayKit was retired at the author's request and must not reappear",
  );
});

test("parent category filters include descendants but not sibling prefixes", () => {
  const nested = [
    { ...assets[0], category: "furniture/chairs/office" },
    { ...assets[0], category: "furniture/chairs-extra" },
  ];
  const filters = {
    query: "",
    category: "furniture/chairs",
    style: "",
    rigged: false,
  };
  assert.equal(filterAssets(nested, filters).length, 1);
  const counts = categoryCounts(nested);
  assert.equal(counts.get("furniture"), 2);
  assert.equal(counts.get("furniture/chairs"), 1);
  assert.equal(counts.get("furniture/chairs/office"), 1);
});

test("animated filter includes embedded and separately authored clips", () => {
  const variants = [
    { ...assets[0], animation_count: 2 },
    {
      ...assets[0],
      animation_count: 0,
      authored_animation_count: 1,
      animated_model: "a.glb",
    },
    { ...assets[0], animation_count: 0 },
  ];
  const filtered = filterAssets(variants, {
    query: "",
    category: "",
    style: "",
    animated: true,
  });
  assert.equal(filtered.length, 2);
});

test("catalog exposes per-asset review limitations", async () => {
  const { readFile } = await import("node:fs/promises");
  const catalog = JSON.parse(
    await readFile(new URL("../manifest.json", import.meta.url), "utf8"),
  );
  const bat = catalog.assets.find((asset) => asset.id === "gobkit-bat");
  assert.ok(
    bat.review_limitations.some((note) =>
      note.includes("continuous baked track"),
    ),
  );
});
