import { exec } from "https://deno.land/x/exec/mod.ts";
import { join } from "https://deno.land/std/path/mod.ts";

// Get the input image path, input dimension, and output directory from command line arguments
const [inputImagePath, inputDimensionStr, outputDirectory] = Deno.args;

// Validate the number of command line arguments
if (!inputImagePath || !inputDimensionStr || !outputDirectory) {
  console.error(
    "Usage: deno run --allow-run --unstable script.ts <inputImagePath> <inputDimension> <outputDirectory>"
  );
  Deno.exit(1);
}

// Parse the input dimension as an integer
const inputDimension = parseInt(inputDimensionStr);

// Calculate the coordinates for each triangle based on the input dimension
const halfDimension = inputDimension / 2;
const topCoords = `0,0 ${inputDimension},0 ${halfDimension},${halfDimension}`;
const leftCoords = `0,0 0,${inputDimension} ${halfDimension},${halfDimension}`;
const bottomCoords = `0,${inputDimension} ${inputDimension},${inputDimension} ${halfDimension},${halfDimension}`;
const rightCoords = `${inputDimension},${inputDimension} ${inputDimension},0 ${halfDimension},${halfDimension}`;

// Create the output directory if it doesn't exist
await Deno.mkdir(outputDirectory, { recursive: true });

// Apply masks to each triangle section and save the output images in the output directory
await exec(
  `convert ${inputImagePath} -fill white -draw "polygon ${topCoords}" -transparent black ${join(outputDirectory, "top.png")}`
);
await exec(
  `convert ${inputImagePath} -fill white -draw "polygon ${leftCoords}" -transparent black ${join(outputDirectory, "left.png")}`
);
await exec(
  `convert ${inputImagePath} -fill white -draw "polygon ${bottomCoords}" -transparent black ${join(outputDirectory, "bottom.png")}`
);
await exec(
  `convert ${inputImagePath} -fill white -draw "polygon ${rightCoords}" -transparent black ${join(outputDirectory, "right.png")}`
);

console.log("Image successfully cut into four isosceles triangles!");
