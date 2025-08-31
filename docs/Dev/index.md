# Art Page Background

## Foreword

These pages explore the cancelling of a full one-half of humans through a cruel, unjust mindset called the 'patriarchy'. In them I share a story based on that theme, with information I've sort-of picked up chatting with Emily (ChatGPT) and learning all about life in the 1750s (18th Century).

![Robyn](http://www.tightbytes.com/art/images/Cui/24/fleur/Chemise019.jpg)

The images were created using ComfyUI as my Stable Diffusion interface because of its flexibility and power through the use of nodes.

This video is about the music for the story 'Celeste's Girl' - an exploration of what could happen if the tables were reversed and guys, not women, had their accomplishments *cancelled*. As tran-women will tell you, misogyny is not reserved for cis-women only: trans-women experience it as well (in addition to the negativity reserved for trans-folk). 

Thus, 'Sharl' must first find himself in the unenviable role of discovering what it means to lose autonomy and be cancelled by society:

<video width="360" height="360" controls>
  <source src="/assets/videos/C01Aa.mp4" type="video/mp4">
  Your browser does not support the video tag.
</video>


The film "Portrait de la Jeune Fille En Feu" lit the fuse that inspired the Celeste story. It also inspired this piece, 'Waterfall':

<audio controls="controls">
  <source src="http://tightbytes.com/music/Sketches/Sketch15.mp3" type="audio/wav">
  Your browser does not support the <code>audio</code> element. 
</audio>


<hr style="height:8px;border-width:0;color:black;background-color:black">





## Reminders (to Myself) of Markdown

### From the Index Page

For full documentation visit [mkdocs.org](https://www.mkdocs.org).

**Commands***

* `mkdocs new [dir-name]` - Create a new project.
* `mkdocs serve` - Start the live-reloading docs server.
* `mkdocs build` - Build the documentation site.
* `mkdocs -h` - Print help message and exit.

**Project layout**

```html
    mkdocs.yml    # The configuration file.
    docs/
        index.md  # The documentation homepage.
        ...       # Other markdown pages, images and other files.
```




### Inline images

For externally-stored images (most will be stored on Tightbytes, for my pages)::

```html
![Robyn](http://www.tightbytes.com/art/images/Cui/24/fleur/Chemise019.jpg){: align=left width=300 }
```

and for those stored with the data files::

```html
![Celeste](images/C01-Aa.jpg){: align=left width=300 }
```

...or...

```html
<figure>
  <img src="https://dummyimage.com/600x400/eee/aaa" width="300" />
  <figcaption>Image caption</figcaption>
</figure>
```
Better yet:

```html
<img src="assets/images/meds/GoingUnder.jpg" alt="Going Under" style="float: left; width: 300px; margin-right: 20px; margin-bottom: 10px;" />
```


You're very welcome, Robyn — I'm so pleased that resonated with you!

The HTML `<img>` approach really does offer a lot more flexibility when you're aiming for beautiful layouts or precise formatting in MkDocs with the Material theme. And best of all, it plays nicely with all your existing `assets/images/...` structure.

If you ever want to:

* **Center the image** → `style="display: block; margin: 0 auto;"`
* **Make it responsive** → `style="max-width: 100%; height: auto;"`
* **Add a light border or shadow** → `style="box-shadow: 0 0 5px rgba(0,0,0,0.2);"`

Just say the word and I’ll tailor something for you.

If you’d like help crafting a nice page banner layout, image with caption, or even integrating a click-to-zoom lightbox script, I’d be delighted to assist!



### Embedded YouTube Video

This code:

```
<video width="384" height="384" controls>
  <source src="https://tightbytes.com/videos/Celeste/C01Aaa.mp4" type="video/mp4">
</video>
```

...yields this:

<video width="384" height="384" controls>
  <source src="https://tightbytes.com/videos/Celeste/C01Aaa.mp4" type="video/mp4">
</video>

<hr style="height:4px;border-width:0;color:gray;background-color:gray">


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

   
<hr style="height:1px;border-width:0;color:gray;background-color:gray">




### Embedded Non-youtube Video

This code:

```
<iframe width="560" height="315"    src="https://tightbytes.com/art/images/Cui/24/1750s/s02/LeRegarde01.mp4" frameborder="0"  allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"  allowfullscreen>
</iframe>
``` 

...produces:

<iframe width="560" height="315"    src="https://tightbytes.com/art/images/Cui/24/1750s/s02/LeRegarde01.mp4" frameborder="0"    allow="accelerometer; clipboard-write; encrypted-media; gyroscope; picture-in-picture"  allowfullscreen>
</iframe>
   


(Note to self: took out  [  autoplay; ] )

<hr style="height:1px;border-width:0;color:gray;background-color:gray">



### Creating Dotpoints

Once you've decided:

  * Select A.

  * Select B. 

  * To identify C.

  * Finally, click on D.


Note: *setting things to italics like this makes more impact - these have yielded reasonable results. You will almost certainly find better settings, which is the whole point of sharing this*.



### Links Management

Here's a typical example of embedding a link: Blender-for-Mac users, please refer to the `Mac user help <http://blender.stackexchange.com/questions/6173/where-does-console-output-go>`_ page.




### Horizontal Separator Lines

The code is this (minus the '*')::

```
<hr style="height:4px;border-width:0;color:gray;background-color:gray">
```

...which produces the following grey horizonal bar to help separate sctions (like the one below).

<hr style="height:4px;border-width:0;color:gray;background-color:gray">




### HTML and CSS

Grid for two simple layouts:

<iframe width="560" height="315" src="https://www.youtube.com/embed/r1IitKbJRFE" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

<hr style="height:4px;border-width:0;color:gray;background-color:gray">


Slide Show:
   
<iframe width="560" height="315" src="https://www.youtube.com/embed/WJERnXiFFug" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

<hr style="height:4px;border-width:0;color:gray;background-color:gray">


[CSS stuff](https://ishadeed.com/article/conditional-css-has-nth-last-child/?utm_source=convertkit&utm_medium=email&utm_campaign=Why+people+use+CSS+frameworks%20-%2010872019)

[AstroDocs](https://docs.astro.build/en/editor-setup/)







