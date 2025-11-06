# Site Tech

## Markdown Cheatsheet

<a href="/assets/images/blog25/06-16Office.jpg" 
   target="_blank" rel="noopener" 
   style="box-shadow: 0 0 25px rgba(0.9,0.9,0.9,0.2);">
<img src="/assets/images/blog25/06-16Office.jpg" 
     alt="Me" 
     width="300" 
     align="right"></a>

This site uses MkDocs, which is a superset of markdown. This section will serve as reminder on markdown syntax. As I get information from [Emily](../../visual/Emilyai/) on other tech -- tasks that are more involved -- that tech will be given its own dedicated page.

For full documentation on MkDocs markdown, visit [mkdocs.org](https://www.mkdocs.org).  
Here's the link for [the material theme](https://squidfunk.github.io/mkdocs-material/).

**Install Commands**

* `mkdocs new [dir-name]` - Create a new project.
* `mkdocs serve` - Start the live-reloading docs server.
* `mkdocs build` - Build the documentation site.
* `mkdocs -h` - Print help message and exit.

**Project layout**

```
mkdocs.yml    # The configuration file.
docs/
    index.md  # The documentation homepage.
    ...       # Other markdown pages, images and other files.
```

<hr style="height:4px;border-width:0;color:pink;background-color:pink">








### Inline images

**Emily-Assisted**  
For externally-stored images (most will be stored on GitHub, for my pages)::

```
![Me](https://art.tightbytes.com/assets/images/blog25/06-16Office.jpg){: align=left width=300 }
```

and for those stored with the data files::

```
![Celeste](images/C01-Aa.jpg){: align=left width=300 }
```

Not sure about this approach:

```
<figure>
  <img src="https://dummyimage.com/600x400/eee/aaa" width="300" />
  <figcaption>Image caption</figcaption>
</figure>
```
These pages more commonly have a html link:

```
<a href="/assets/images/blog25/06-16Office.jpg" target="_blank" rel="noopener">
<img src="/assets/images/blog25/06-16Office.jpg" alt="Me" width="300"align="right"></a>
```

...as it allows for a clickable image to open a larger version in a new tab. The HTML `<img>` approach really does offer a lot more flexibility when you're aiming for beautiful layouts or precise formatting in MkDocs with the Material theme. And best of all, it plays nicely with all your existing `assets/images/...` structure.

If you need to:

* **Center the image** → `style="display: block; margin: 0 auto;"`
* **Make it responsive** → `style="max-width: 100%; height: auto;"`
* **Add a light border or shadow** → `style="box-shadow: 0 0 5px rgba(0,0,0,0.2);"`

<hr style="height:4px;border-width:0;color:pink;background-color:pink">








### Embedded YouTube Video

This code is no longer being used:

```
<video width="384" height="384" controls>
  <source src="https://tightbytes.com/videos/Celeste/C01Aaa.mp4" type="video/mp4">
</video>
```

Instead, videos are being hosted on Cloudflare. 

```
<div style="position:relative;padding-top:100%">
    <iframe src="https://customer-ze4n45l8rqsb9yse.cloudflarestream.com/420e07a7d02c25184d2faf7e6ff0b53c/iframe"
    allow="accelerometer;gyroscope;autoplay;encrypted-media;picture-in-picture"
    style="border:none;position:absolute;inset:0;width:100%;height:100%"></iframe>
</div>
```

Simply change the number after '.com/' -- 420e07a7d02c25184d2faf7e6ff0b53c -- and before '/iframe'.  Quick-n-dirty way to make it not huge:

```
<style>
  .flex-container {display: flex; gap: 20px; align-items: flex-start;}
  .column {flex: 1 1 0; min-width: 0;}
  .column--right {border-left: 1px solid var(--md-default-fg-color--lightest); padding-left: 20px; }
</style>

<!-- NOTE! DO NOT INDENT! MARKDOWN WILL FAIL!! /-->

<div class="flex-container" markdown>
<div class="column">

<div style="position:relative;padding-top:100%">
    <iframe src="https://customer-ze4n45l8rqsb9yse.cloudflarestream.com/6c50151790d66b09f2d94d7c3096ec7d/iframe"
    allow="accelerometer;gyroscope;autoplay;encrypted-media;picture-in-picture"
    style="border:none;position:absolute;inset:0;width:100%;height:100%"></iframe>
</div>

</div>

<div class="column column--right" markdown>
</div>

</div>

```


<style>
  .flex-container {display: flex; gap: 20px; align-items: flex-start;}
  .column {flex: 1 1 0; min-width: 0;}
  .column--right {border-left: 1px solid var(--md-default-fg-color--lightest); padding-left: 20px; }
</style>

<div class="flex-container" markdown>
<div class="column">

<div style="position:relative;padding-top:100%">
    <iframe src="https://customer-ze4n45l8rqsb9yse.cloudflarestream.com/420e07a7d02c25184d2faf7e6ff0b53c/iframe"
    allow="accelerometer;gyroscope;autoplay;encrypted-media;picture-in-picture"
    style="border:none;position:absolute;inset:0;width:100%;height:100%"></iframe>
</div>


</div>
<div class="column column--right" markdown>
.
</div>
</div>












### Embedded Audio

This code:

```
		<audio controls="controls">
		  <source src="http://tightbytes.com/music/Sketches/Sketch15.mp3" type="audio/wav">
		  Your browser does not support the <code>audio</code> element. 
		</audio>
```

...produced:

<audio controls="controls">
  <source src="http://tightbytes.com/music/Sketches/Sketch15.mp3" type="audio/wav">
  Your browser does not support the <code>audio</code> element. 
</audio>

<hr style="height:4px;border-width:0;color:pink;background-color:pink">







### Embedded Video

This code:

```
<iframe width="560" height="315"    src="https://tightbytes.com/art/images/Cui/24/1750s/s02/LeRegarde01.mp4" frameborder="0"  allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"  allowfullscreen>
</iframe>
``` 

...produces, from my site:

<iframe width="560" height="315"    src="https://tightbytes.com/art/images/Cui/24/1750s/s02/LeRegarde01.mp4" frameborder="0"    allow="accelerometer; clipboard-write; encrypted-media; gyroscope; picture-in-picture"  allowfullscreen>
</iframe>

(Note to self: took out  [  autoplay; ] )

---

For Cloudflare, simply change out the number string after ".com/" and before "/iframe", in this instance, this number:  'f16255e78c021b7a0e5fae66ae554133'. So, this code:

```
<div style="position:relative;padding-top:56.25%">
  <iframe src="https://customer-ze4n45l8rqsb9yse.cloudflarestream.com/f16255e78c021b7a0e5fae66ae554133/iframe"
          allow="accelerometer;gyroscope;autoplay;encrypted-media;picture-in-picture"
          allowfullscreen
          style="border:none;position:absolute;inset:0;width:100%;height:100%"></iframe>
</div>
```

... produces, from Cloudflare:

<div style="position:relative;padding-top:56.25%">
  <iframe src="https://customer-ze4n45l8rqsb9yse.cloudflarestream.com/f16255e78c021b7a0e5fae66ae554133/iframe"
          allow="accelerometer;gyroscope;autoplay;encrypted-media;picture-in-picture"
          allowfullscreen
          style="border:none;position:absolute;inset:0;width:100%;height:100%"></iframe>
</div>

<!-- Save this:

<video width="480" height="480" controls>
  <source src="/assets/videos/C01.mp4" type="video/mp4">
</video>

/-->


Emily suggests:

<div style="position:relative;padding-top:56.25%">
  <iframe src="https://customer-ze4n45l8rqsb9yse.cloudflarestream.com/f16255e78c021b7a0e5fae66ae554133/iframe"
          allow="accelerometer;gyroscope;autoplay;encrypted-media;picture-in-picture"
          allowfullscreen
          style="border:none;position:absolute;inset:0;width:100%;height:100%"></iframe>
</div>

or

<div class="cf-player">
  <iframe src="https://customer-ze4n45l8rqsb9yse.cloudflarestream.com/f16255e78c021b7a0e5fae66ae554133/iframe"
          allow="accelerometer;gyroscope;autoplay;encrypted-media;picture-in-picture"
          allowfullscreen></iframe>
</div>

<style>
  .cf-player{
    aspect-ratio:1/1;
    width:100%;
    max-width:480px;     /* cap size if you like */
    margin:auto;         /* center it */
  }
  .cf-player iframe{
    width:100%;
    height:100%;
    border:0;
  }

  /* Fallback for very old browsers:
  .cf-player{position:relative;padding-top:100%}
  .cf-player iframe{position:absolute;inset:0}
  */
</style>

... and even ...

<div class="cf-player">
  <iframe
    src="https://customer-ze4n45l8rqsb9yse.cloudflarestream.com/f16255e78c021b7a0e5fae66ae554133/iframe"
    title="Cloudflare Stream video"
    allow="accelerometer;gyroscope;autoplay;encrypted-media;picture-in-picture"
    allowfullscreen
    loading="lazy"></iframe>
</div>

<style>
  .cf-player{
    aspect-ratio:1/1;
    width:100%;
    max-width:480px;
    margin:auto;
    background:#111;          /* pleasant placeholder while loading */
    border-radius:12px;
    overflow:hidden;
  }
  .cf-player iframe{
    display:block;
    width:100%;
    height:100%;
    border:0;
  }
</style>

... **05.Nov.2025**  
Added this - thanks, Emily.

<style>
  /* two 384×384 iframes side by side */
  .video-row {
    display: flex;
    gap: 16px;
    flex-wrap: wrap;
    justify-content: center;
    align-items: flex-start;
  }
  .video-row iframe {
    width: 384px;
    height: 384px;
    border: 0;
    border-radius: 8px; /* optional */
  }
  /* Stack on narrow screens */
  @media (max-width: 820px) {
    .video-row { flex-direction: column; align-items: center; }
  }
</style>

<div class="video-row">
  <iframe
    src="https://customer-ze4n45l8rqsb9yse.cloudflarestream.com/6978db4dbc1c3046f3aa321ff664b1dd/iframe"
    title="Version Française"
    loading="lazy"
    allow="autoplay; fullscreen; picture-in-picture"
    allowfullscreen>
  </iframe>

  <iframe
    src="https://customer-ze4n45l8rqsb9yse.cloudflarestream.com/4dfe30900934badaea9190c99103c567/iframe"
    title="English Version"
    loading="lazy"
    allow="autoplay; fullscreen; picture-in-picture"
    allowfullscreen>
  </iframe>
</div>


<hr style="height:4px;border-width:0;color:pink;background-color:pink">








### Creating Dotpoints

Once you've decided:

* Select A.  
* Select B.  
* To identify C.  
* Finally, click on D.  

Note: *setting things to italics like this makes more impact - these have yielded reasonable results. You will almost certainly find better settings, which is the whole point of sharing this*.

<hr style="height:4px;border-width:0;color:pink;background-color:pink">









### Links Management

Here's a typical example of embedding a link: Blender-for-Mac users, please refer to the [Mac user help](http://blender.stackexchange.com/questions/6173/where-does-console-output-go) page.

<hr style="height:4px;border-width:0;color:pink;background-color:pink">








### Horizontal Separator Lines

The code is this (minus the '*')::

```
<hr style="height:4px;border-width:0;color:pink;background-color:pink">
```

...which produces the following grey horizonal bar to help separate sctions (like the one below).

<hr style="height:4px;border-width:0;color:pink;background-color:pink">








### HTML and CSS

**Grid for two simple layouts**:

<iframe width="560" height="315" src="https://www.youtube.com/embed/r1IitKbJRFE" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

---

**Slide Show**:
 
<iframe width="560" height="315" src="https://www.youtube.com/embed/WJERnXiFFug" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

---

[CSS stuff](https://ishadeed.com/article/conditional-css-has-nth-last-child/?utm_source=convertkit&utm_medium=email&utm_campaign=Why+people+use+CSS+frameworks%20-%2010872019)

[AstroDocs](https://docs.astro.build/en/editor-setup/)

---

**Do Not Show On Page**

<!-- Everything within these tags will not show on the page 

extra:
  social:
    - icon: fontawesome/brands/github
      link: https://www.tightbytes.com/index.html
    - icon: fontawesome/brands/bluesky
      link: https://bluesky.com/_____sveil


/-->

<hr style="height:20px;border-width:0;color:pink;background-color:pink">
