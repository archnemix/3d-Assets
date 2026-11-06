import * as THREE from "three";
import { OrbitControls } from "three/addons/controls/OrbitControls.js";
import { GLTFLoader } from "three/addons/loaders/GLTFLoader.js";
import { assetUrl } from "./data.js";

function disposeObject(object) {
  const textures = new Set();
  const materials = new Set();
  const geometries = new Set();
  object.traverse((child) => {
    if (child.geometry) geometries.add(child.geometry);
    for (const material of [child.material].flat().filter(Boolean)) {
      materials.add(material);
      for (const value of Object.values(material)) {
        if (value?.isTexture) textures.add(value);
      }
    }
  });
  for (const texture of textures) {
    if (texture.source?.data?.close) texture.source.data.close();
    texture.dispose();
  }
  for (const material of materials) material.dispose();
  for (const geometry of geometries) geometry.dispose();
}

/** Mount one viewer; cleanup also handles a load finishing after the dialog closes. */
export function mountViewer(host, asset) {
  const stage = host.querySelector(".viewer-stage");
  const status = host.querySelector(".viewer-status");
  const clipSelect = host.querySelector(".viewer-clips");
  const play = host.querySelector(".viewer-play");
  const reset = host.querySelector(".viewer-reset");
  const modelSelect = host.querySelector(".viewer-model");
  const spin = host.querySelector(".viewer-spin");
  let renderer;
  try {
    renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
  } catch {
    status.textContent =
      "3D preview is unavailable in this browser. Use the inspection renders or download the model instead.";
    return () => {};
  }
  renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
  renderer.outputColorSpace = THREE.SRGBColorSpace;
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.toneMappingExposure = 1.15;
  renderer.domElement.setAttribute(
    "aria-label",
    `Interactive 3D view of ${asset.title}`,
  );
  stage.append(renderer.domElement);
  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(40, 1, 0.01, 1000);
  const controls = new OrbitControls(camera, renderer.domElement);
  controls.enableDamping = true;
  controls.autoRotateSpeed = 1.2;
  scene.add(new THREE.HemisphereLight(0xffffff, 0x657477, 2.4));
  const key = new THREE.DirectionalLight(0xffffff, 2.4);
  key.position.set(4, 8, 6);
  scene.add(key);
  const fill = new THREE.DirectionalLight(0xd4eaff, 1.2);
  fill.position.set(-5, 3, -4);
  scene.add(fill);
  const loader = new GLTFLoader();
  let object = null;
  let mixer = null;
  let clips = [];
  let action = null;
  let playing = true;
  let closed = false;
  let sequence = 0;
  let frame = 0;
  let homePosition = new THREE.Vector3();
  let homeTarget = new THREE.Vector3();
  const clock = new THREE.Clock();

  function fit() {
    const box = new THREE.Box3().setFromObject(object);
    if (box.isEmpty())
      throw new Error("The model contains no visible geometry");
    const sphere = box.getBoundingSphere(new THREE.Sphere());
    if (!Number.isFinite(sphere.radius) || sphere.radius <= 0)
      throw new Error("The model has invalid bounds");
    const halfFov = THREE.MathUtils.degToRad(camera.fov / 2);
    const distance =
      (sphere.radius / Math.sin(halfFov)) *
      Math.max(1, 1 / camera.aspect) *
      1.15;
    homeTarget.copy(sphere.center);
    homePosition
      .copy(sphere.center)
      .add(new THREE.Vector3(1, 0.7, 1).normalize().multiplyScalar(distance));
    camera.near = Math.max(sphere.radius / 1000, 0.0001);
    camera.far = Math.max(distance * 100, 100);
    camera.updateProjectionMatrix();
    controls.minDistance = sphere.radius / 20;
    controls.maxDistance = sphere.radius * 50;
    resetView();
  }
  function resetView() {
    camera.position.copy(homePosition);
    controls.target.copy(homeTarget);
    controls.update();
  }
  function resize() {
    const width = stage.clientWidth;
    const height = stage.clientHeight;
    if (!width || !height) return;
    renderer.setSize(width, height, false);
    camera.aspect = width / height;
    camera.updateProjectionMatrix();
  }
  function chooseClip() {
    if (!mixer) return;
    if (action) action.stop();
    action = mixer.clipAction(clips[Number(clipSelect.value)]);
    action.reset().play();
    action.paused = !playing;
  }
  async function load(path) {
    const current = ++sequence;
    status.textContent = "Loading 3D model…";
    clipSelect.disabled = true;
    play.disabled = true;
    try {
      const gltf = await loader.loadAsync(assetUrl(path));
      if (closed || current !== sequence) {
        disposeObject(gltf.scene);
        return;
      }
      if (object) {
        scene.remove(object);
        if (mixer) mixer.stopAllAction();
        disposeObject(object);
      }
      object = gltf.scene;
      scene.add(object);
      clips = gltf.animations;
      mixer = clips.length ? new THREE.AnimationMixer(object) : null;
      clipSelect.replaceChildren();
      clips.forEach((clip, index) =>
        clipSelect.add(
          new Option(clip.name || `Clip ${index + 1}`, String(index)),
        ),
      );
      clipSelect.disabled = !clips.length;
      play.disabled = !clips.length;
      playing = true;
      play.textContent = "Pause";
      action = null;
      if (clips.length) chooseClip();
      resize();
      fit();
      status.textContent = clips.length
        ? `${clips.length} animation ${clips.length === 1 ? "clip" : "clips"} available.`
        : "Static model · no animation clips in this file.";
    } catch (error) {
      if (!closed && current === sequence)
        status.textContent = `Could not load the 3D model: ${error.message}. Inspection renders and downloads remain available.`;
    }
  }
  const observer = new ResizeObserver(resize);
  observer.observe(stage);
  clipSelect.addEventListener("change", chooseClip);
  play.addEventListener("click", () => {
    playing = !playing;
    if (action) action.paused = !playing;
    play.textContent = playing ? "Pause" : "Play";
  });
  reset.addEventListener("click", resetView);
  spin.addEventListener("change", () => {
    controls.autoRotate = spin.checked;
  });
  modelSelect.addEventListener("change", () => load(modelSelect.value));
  function draw() {
    if (closed) return;
    frame = requestAnimationFrame(draw);
    const delta = Math.min(clock.getDelta(), 0.1);
    if (mixer) mixer.update(delta);
    controls.update();
    renderer.render(scene, camera);
  }
  resize();
  draw();
  load(modelSelect.value);
  return () => {
    closed = true;
    sequence++;
    cancelAnimationFrame(frame);
    observer.disconnect();
    controls.dispose();
    if (mixer) mixer.stopAllAction();
    if (object) disposeObject(object);
    renderer.dispose();
    renderer.forceContextLoss();
    renderer.domElement.remove();
  };
}
