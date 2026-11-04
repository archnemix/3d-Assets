import assert from "node:assert/strict";
import test from "node:test";

import { filterAssets } from "../gallery/scripts/data.js";

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
