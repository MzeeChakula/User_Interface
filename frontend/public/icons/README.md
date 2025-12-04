# PWA Icons & Assets

This directory contains all Progressive Web App (PWA) assets for the MzeeChakula application.

## Theme Colors

The logo and PWA assets use the following color palette:

| Color Name | Hex Code | RGB | Usage |
|------------|----------|-----|-------|
| **Primary Red** | `#D90000` | `rgb(217, 0, 0)` | Main background, brand primary color |
| **Golden Yellow** | `#FCDC04` | `rgb(252, 220, 4)` | Icon/symbol color, accent |
| **Dark Base** | `#1E1E1E` | `rgb(30, 30, 30)` | Base/shadow color |

### Color Usage Guidelines

- **Primary Red (#D90000)**: Use for primary buttons, headers, and branding elements
- **Golden Yellow (#FCDC04)**: Use for icons, highlights, and call-to-action elements
- **Dark Base (#1E1E1E)**: Use for backgrounds, shadows, and contrast

## Generated Assets

### Icons

| File | Size | Purpose | Platform |
|------|------|---------|----------|
| `favicon.ico` | 48x48 | Browser favicon | All browsers |
| `pwa-64x64.png` | 64x64 | Small PWA icon | Desktop, Android |
| `pwa-192x192.png` | 192x192 | Medium PWA icon | Android, Desktop |
| `pwa-512x512.png` | 512x512 | Large PWA icon | Android, Desktop |
| `maskable-icon-512x512.png` | 512x512 | Adaptive icon with safe zone | Android (adaptive icons) |
| `apple-touch-icon-180x180.png` | 180x180 | iOS home screen icon | iOS/iPadOS |
| `logotransparent.svg` | Vector | Source logo with transparency | All platforms |

## How to Use

### 1. HTML Head Links

Add these tags to your `index.html` inside the `<head>` section:

```html
<!-- Favicon -->
<link rel="icon" href="/icons/favicon.ico" sizes="48x48">
<link rel="icon" href="/icons/logotransparent.svg" sizes="any" type="image/svg+xml">

<!-- Apple Touch Icon (iOS) -->
<link rel="apple-touch-icon" href="/icons/apple-touch-icon-180x180.png">
```

### 2. PWA Manifest Configuration

Add this `icons` array to your `manifest.json` or `site.webmanifest`:

```json
{
  "name": "MzeeChakula",
  "short_name": "MzeeChakula",
  "theme_color": "#D90000",
  "background_color": "#1E1E1E",
  "display": "standalone",
  "icons": [
    {
      "src": "/icons/pwa-64x64.png",
      "sizes": "64x64",
      "type": "image/png"
    },
    {
      "src": "/icons/pwa-192x192.png",
      "sizes": "192x192",
      "type": "image/png"
    },
    {
      "src": "/icons/pwa-512x512.png",
      "sizes": "512x512",
      "type": "image/png",
      "purpose": "any"
    },
    {
      "src": "/icons/maskable-icon-512x512.png",
      "sizes": "512x512",
      "type": "image/png",
      "purpose": "maskable"
    }
  ]
}
```

### 3. Meta Tags for Theme

Add these meta tags to your `index.html`:

```html
<!-- PWA Theme Colors -->
<meta name="theme-color" content="#D90000">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="msapplication-TileColor" content="#D90000">
```

## Platform-Specific Behavior

### Android

- Uses `pwa-192x192.png` for standard launcher icon
- Uses `maskable-icon-512x512.png` for adaptive icons (Android 8.0+)
- Theme color applies to address bar and task switcher

### iOS/iPadOS

- Uses `apple-touch-icon-180x180.png` for home screen
- Best quality achieved by using @3x retina display assets
- SVG fallback for Safari

### Desktop (Chrome, Edge, Safari)

- Uses `pwa-64x64.png` for browser tab
- Uses `pwa-512x512.png` for app installation
- `favicon.ico` as universal fallback

### Windows

- Uses `pwa-512x512.png` for taskbar and start menu
- Theme color applies to title bar

## Regenerating Assets

If you need to regenerate the PWA assets from the source logo:

```bash
npm run generate-pwa-assets
```

This command uses `@vite-pwa/assets-generator` with the `minimal-2023` preset.

### Custom Generation

To generate from a different source file:

```bash
npx pwa-assets-generator --preset minimal-2023 public/icons/your-logo.svg
```

## Best Practices

1. **Keep logotransparent.svg** - This is your source file, always keep a backup
2. **Don't edit generated PNGs** - Regenerate from SVG if changes needed
3. **Test on devices** - Always test icons on actual Android and iOS devices
4. **Use theme colors consistently** - Apply the same colors in your CSS
5. **Maskable icon safe zone** - Keep important content within 80% center area

## Accessibility

- High contrast between red background and yellow icon ensures visibility
- Icon design is simple and recognizable at all sizes
- Works well in both light and dark system themes

## References

- [PWA Icons Spec](https://web.dev/add-manifest/)
- [Maskable Icons](https://web.dev/maskable-icon/)
- [Apple Touch Icons](https://developer.apple.com/design/human-interface-guidelines/ios/icons-and-images/app-icon/)

---

**Generated**: November 2025
**Tool**: @vite-pwa/assets-generator v1.0.2
**Preset**: minimal-2023
