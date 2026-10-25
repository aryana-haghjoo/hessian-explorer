# The Hessian, interactive

An interactive explorer for the Hessian matrix, H = J(∇f). Drag a patch over a surface and watch the Hessian, its eigenvalues, the eigenvector arrows, and the bowl / dome / saddle label update live.

**Live demo:** `<add your GitHub Pages or website URL here>`

## Credit

This is an interactive version of an animation by **Basem Rajjoub**:

> Basem Rajjoub, "The Hessian" (animation), LinkedIn post, 2026.
> https://www.linkedin.com/posts/rajjoub_math-optimization-fem-share-7519720158731571200-tjM1/
> Profile: https://www.linkedin.com/in/rajjoub/

The layout, colors and wording (orange for curving up and blue for curving down, the "SADDLE: up one way, down the other" label) follow that original. The original was a fixed animation. This version lets you move the point yourself and adds the following features.

## What you can do

- **Drag the green patch** over the 3D surface, or click and drag on the contour map. Arrow keys nudge the point (hold Shift for bigger steps).
- **Turn the 3D view** by dragging empty space.
- **Change the patch size** with the slider.
- **Overlay the quadratic model** f + ∇f·d + ½dᵀHd, to see where the second-order approximation stops matching the real surface.

The surface is a sum of two Gaussian hills, so the Hessian is computed analytically, not by finite differences.

## Files

| File | Purpose |
|---|---|
| `hessian_explorer.html` | The page source (body only) |
| `build_site.sh` | Wraps the source into a standalone `index.html` |
| `index.html` | Generated; open it in a browser or serve it with GitHub Pages |
| `hessian_movie.py` | Script that renders a non-interactive GIF version (`python3 hessian_movie.py out.gif`) |

The page has no build dependencies. Fonts load from Google Fonts, and the math is native MathML.

After editing `hessian_explorer.html`, run `./build_site.sh` to regenerate `index.html`.

## Hosting on GitHub Pages

Push the repository, then go to **Settings → Pages** and set the source to the `main` branch, root folder. The page is then served at `https://<user>.github.io/<repo>/`.

## License

Code released under the [MIT License](LICENSE). The visual design and the original animation are by Basem Rajjoub; see [Credit](#credit).
