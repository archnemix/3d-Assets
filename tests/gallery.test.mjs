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
