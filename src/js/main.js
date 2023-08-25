import { SVGLoader } from "three/addons/loaders/SVGLoader.js";

export function exportSVG(contour) {
  let rect = cv.boundingRect(contour);
  let x = rect.x;
  let y = rect.y;
  let h = rect.height;
  let w = rect.width;

  var svg = `<svg width="${w}" height="${h}" xmlns="http://www.w3.org/2000/svg">`;
  svg += '<path d="M';
  for (let i = 0; i < contour.rows; i++) {
    let x1 = contour.data[i * 8];
    let y1 = contour.data[i * 8 + 4];
    svg += `${x1 - x} ${y1 - y} `;
  }
  svg += '"/>';
  svg += "</svg>";

  const loader = new SVGLoader();
  const svgData = loader.parse(svg);

  // Group that will contain all of our paths
  const svgGroup = new THREE.Group();

  const material = new THREE.MeshNormalMaterial();

  // Loop through all of the parsed paths
  svgData.paths.forEach((path, i) => {
    const shapes = path.toShapes(true);

    // Each path has array of shapes
    shapes.forEach((shape, j) => {
      // Finally we can take each shape and extrude it
      const geometry = new THREE.ExtrudeGeometry(shape, {
        depth: 20,
        bevelEnabled: false,
      });

      // Create a mesh and add it to the group
      const mesh = new THREE.Mesh(geometry, material);

      svgGroup.add(mesh);
    });
  });

  // Add our group to the scene (you'll need to create a scene)
  return svgGroup;
}
