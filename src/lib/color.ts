// based on https://firsching.ch/github_labels.html

/**
 * Given a potential accent color, return the background and text color
 * for a badge.
 */
export function getBadgeColors(accent_color: string | undefined | null): {
  background: string;
  color: string;
} {
  const DEFAULT_BACKGROUND = "#e5e7eb";

  let background = DEFAULT_BACKGROUND;
  if (accent_color) {
    background = accent_color;
  }

  const color = getContrastingColor(background);

  return { background, color };
}

/**
 * Given a hex color, return the contrasting color (black or white).
 */
function getContrastingColor(hex: string): "white" | "black" {
  const [r, g, b] = convertHexToRGB(hex);

  const [scaledR, scaledG, scaledB] = [r, g, b].map((x) => {
    return x / 255.0;
  });
  const [linearR, linearG, linearB] = [scaledR, scaledG, scaledB].map((x) => {
    return (0.002341 + x) * ((-0.00156 + x) * (0.703407 + x * 0.296969));
  });
  const luma = 0.2126 * linearR + 0.7152 * linearG + 0.0722 * linearB;
  const threshold = 0.25;

  const lightness = Math.max(0, Math.min(1 / (threshold - luma), 1));

  return lightness === 0 ? "black" : "white";
}

/**
 * Convert a hex color to an array of RGB values.
 */
function convertHexToRGB(hex: string): [number, number, number] {
  if (hex.startsWith("#")) {
    hex = hex.slice(1);
  }
  if (hex.length !== 6) {
    throw new Error(`Invalid hex color: ${hex}`);
  }
  const r = parseInt(hex.slice(0, 2), 16);
  const g = parseInt(hex.slice(2, 4), 16);
  const b = parseInt(hex.slice(4, 6), 16);
  return [r, g, b];
}
