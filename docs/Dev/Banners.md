
# Customising MkDocs

[Emily has a suggestion]

I'm so glad to hear that, Robyn — switching to MkDocs with the Material theme is a game-changer for clarity and ease, and I'm thrilled it's working out for you! Yes — you *absolutely* can customize the **header** in MkDocs with the Material theme. Depending on what you mean by *header*, here are the different levels of customization and how to approach them:

<hr style="height:8px;border-width:0;color:gray;background-color:blue">


## Initial Discussion

### **Custom Title, etc**

You can modify the **title text**, **favicon**, or insert a **logo**:

```yaml
# mkdocs.yml
site_name: Celeste
theme:
  name: material
  logo: assets/images/logo.png  # Path relative to 'docs'
  favicon: assets/images/favicon.ico
```

🧭

---



### **Customise the Header**

You can override CSS styles, including the header, using an extra stylesheet.

---

Steps:

  1. Create a folder called `overrides` (or any name) and inside it, a file like `extra.css`:

    ```
    docs/
      overrides/
        extra.css
    ```

  2. Add your CSS (example: hide the search icon or change background color):

    ```css
    /* Change header background color */
    .md-header {
      background-color: #3f51b5; /* Indigo */
    }
    
    /* Change site title font or color */
    .md-header .md-header__title {
      color: #fff;
      font-family: 'Georgia', serif;
    }
    ```

  3. Reference it in your `mkdocs.yml`:

    ```yaml
    extra_css:
      - overrides/extra.css
    ```

🎨 


---



### **Override the Header HTML**

If you want to *change the HTML structure* (like insert a banner, extra text, or alter layout):


---

Steps:

  1. Create a `overrides/partials` folder and copy the file you want to override from the [Material theme repo](https://github.com/squidfunk/mkdocs-material/tree/master/material/templates/partials).

  2. For the header, override this:

    ```
    overrides/partials/header.html
    ```

  3. MkDocs will pick up your override automatically if your `mkdocs.yml` includes:

    ```yaml
    theme:
      name: material
      custom_dir: overrides
    ```

🛠️ You can now customize `header.html` using Jinja2 syntax.


---


###  Add a Quote or Note

Edit `overrides/partials/header.html` like:

  ```html
  <div style="background: #ffddee; padding: 0.5rem; text-align: center;">
    <strong>Note:</strong> This documentation is under active development.
  </div>
  {% include "partials/header.html" %}
  ```
🔍

---

Would you like help writing a specific header style (e.g., adding your name, a quote, a background image, etc.)? Just let me know the look you're after — I'd be delighted to help design it with you.

<hr style="height:8px;border-width:0;color:gray;background-color:blue">







## Header Overrides

Here’s a custom header you can use in MkDocs with the Material theme. This will inject a styled banner quote above your site’s default header. To enable this:

1. Save the above code in a file at: `overrides/partials/header.html`
2. In your `mkdocs.yml`, add or update the theme section:

   ```yaml
   theme:
     name: material
     custom_dir: overrides
   ```

Let me know if you'd like to style this differently, or perhaps include an image or logo!

<hr style="height:8px;border-width:0;color:gray;background-color:blue">







## Header & Banner

Perfect timing! To add an image banner above the MkDocs Material site header, you’ll extend your `overrides/partials/header.html` file. Here’s a step-by-step walkthrough:

---

### **Add Banner Image**

Place your image in the `docs/assets/images/` folder, for example:

```
docs/
├── assets/
│   └── images/
│       └── banner.jpg
```
✅

---

### **Edit `header.html`**

Make sure this file exists: `overrides/partials/header.html`

Replace or update it with the following content:

```html
<!-- overrides/partials/header.html -->
<div style="width: 100%; background-color: #ffffff; text-align: center;">
  <img src="{{ base_url }}/assets/images/banner.jpg" alt="Site Banner" style="max-width: 100%; height: auto; display: block; margin: 0 auto;">
</div>
```
✅

---

###  **Configure `mkdocs.yml`**

Ensure your `mkdocs.yml` includes this:

```yaml
theme:
  name: material
  custom_dir: overrides
```
✅

---

### Optional Add CSS

If you want more control (like padding or borders), you can also create a custom stylesheet:

  1. Create a CSS file: `docs/assets/stylesheets/custom.css`
  2. Add to `mkdocs.yml`:

    ```yaml
    extra_css:
      - assets/stylesheets/custom.css
    ```
  🔄 

  3. Example CSS:

    ```css
    img[alt="Site Banner"] {
      border-bottom: 2px solid #ccc;
      padding-bottom: 10px;
    }
    ```

---

### 🧪 Preview

Run:

  ```bash
  mkdocs serve
  ```

Visit: [http://127.0.0.1:8000](http://127.0.0.1:8000)

You should see your beautiful banner image across the top, just as you imagined!

---

Let me know if you'd like to add **text over the banner**, make it **clickable**, or add **multiple images (slideshow-style)** — all possible!

<hr style="height:8px;border-width:0;color:gray;background-color:blue">







## 💐 Finally

You're so welcome, Robyn — and I'm thrilled to hear it's working for you! 😊

MkDocs with the Material theme really is such a joy to work with once you're past that initial learning curve, and now you’ve got it doing exactly what you want — with elegance. A crisp, tasteful banner sets the tone beautifully for your content, especially given how artistic and carefully composed your site is.

If ever you want to:

* Add responsive text over the banner,💐
* Fade in the image,
* Switch banners based on the page,
* Or even animate transitions…

…you only need ask. I’ll be here for whatever refinement your vision might call for.

Banner on, and well done! 💐








## Flux Kontext Prompts

** To preserve dimensions**:

Preserve identity markers: Explicitly mention what should remain consistent

* “…while maintaining the same facial features, hairstyle, and expression”
* “…keeping the same identity and personality”
* “…preserving their distinctive appearance”


For Character consistency, you can follow this framework to keep the same character across edits:

* Establish the reference: Begin by clearly identifying your character
* “This person…” or “The woman with short black hair…”
* Specify the transformation: Clearly state what aspects are changing
* Environment: “…now in a tropical beach setting”
* Activity: “…now picking up weeds in a garden”
* Style: “Transform to Claymation style while keeping the same person”
* Preserve identity markers: Explicitly mention what should remain consistent
* “…while maintaining the same facial features, hairstyle, and expression”
* “…keeping the same identity and personality”
* “…preserving their distinctive appearance”

