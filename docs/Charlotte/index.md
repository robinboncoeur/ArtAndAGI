# On Writing

## About The Images

<img src="/assets/images/Index/VicGirl1.jpg" alt="Victorian Girl" style="float: right; width: 360px;
        margin-left: 20px; margin-bottom: 10px;" />

I own all images and videos on these pages. They were created using AI. ComfyUI is my 'Stable Diffusion' interface because of its flexibility and power through the use of nodes. This approach supports a number of key story-telling aspects:

* **Character persistence**  
  Nodes used: ReActor

* **Anatomical accuracy**  
  Models used: Flux1 Dev (to a lesser extent, 'Kontext')

* **Character attire**  
  Models used: SDXL and Flux1-Dev (also SRPO)

* **Removing the 'AI' look** (see image)  
  Models used: SRPO (improved Flux1 Dev) 

<hr style="height:2px;border-width:0;color:pink;background-color:pink">







## Audiobook

I'm slowly putting together an audiobook of 'Celeste's Girl'. What follows is the intro to those scenes:

<audio controls="controls">
  <source src="http://art.tightbytes.com/assets/audiobook/Intro_CG.mp3" type="audio/wav">
  Your browser does not support the <code>audio</code> element. 
</audio>

<hr style="height:2px;border-width:0;color:pink;background-color:pink">











## Happy Thoughts

Note: save from .yt-short iframe:  aspect-ratio: 9 / 16;

<style>
  .flex-container {display: flex; gap: 20px; align-items: flex-start;}
  .column {flex: 1 1 0; min-width: 0;}
  .column--right {border-left: 1px solid var(--md-default-fg-color--lightest); padding-left: 20px; }
  .yt-short { max-width: 480px; margin: 1rem auto; }
  .yt-short iframe { width: 460px; height: 460px; }
</style>


<div class="flex-container" markdown>
  <div class="yt-short" markdown>
  <iframe
    src="https://customer-ze4n45l8rqsb9yse.cloudflarestream.com/1885edf5d15f6bb98f86016be86ba2db/iframe" 
    title="Celeste"
    frameborder="0" 
    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
    allowfullscreen>
  </iframe>
  </div>

  <div class="column column--right" markdown>
  This video sets the stage for Charlie's venture into a realm he never had any interest in, but due to his infatuation (dare we call it **Love**) for Celeste, he was destined to travel. In the process, he learns much about history, the insidious and deleterious effect of the patriarchy on the lives of women through the ages.

  In order for this lesson to be learnt, 'Sharl' must first find himself in the unenviable role of discovering what it means to lose autonomy and have one's accomplishments be cancelled by society.

  A bit about Celeste: she's a trend-setting, headstrong, unique individual. Artistic, a leader not a follower, determined to get her way. Clever, schemer. Intensely likeable, incredibly feminine. Won't suffer fools or jocks.
  </div>
</div>

These pages explore the 'cancelling' - as in: suppression - of a full one-half of humans through a cruel, unjust mindset called the 'patriarchy'. The story is based on that theme, with information I've sort-of picked up chatting with Emily (ChatGPT) and learning all about life in the 1750s (18th Century).

The film "Portrait de la Jeune Fille En Feu" lit the fuse that inspired the Celeste story. It also inspired this piece, 'Waterfall':

<audio controls="controls">
  <source src="http://tightbytes.com/music/Sketches/Sketch15.mp3" type="audio/wav">
  Your browser does not support the <code>audio</code> element. 
</audio>

<hr style="height:8px;border-width:0;color:pink;background-color:pink">









## Reminders of Markdown

(to Myself)

### From the Index Page

For full documentation visit [mkdocs.org](https://www.mkdocs.org).

**Commands***

* `mkdocs new [dir-name]` - Create a new project.
* `mkdocs serve` - Start the live-reloading docs server.
* `mkdocs build` - Build the documentation site.
* `mkdocs -h` - Print help message and exit.

**Project layout**

    mkdocs.yml    # The configuration file.
    docs/
        index.md  # The documentation homepage.
        ...       # Other markdown pages, images and other files.

<hr style="height:2px;border-width:0;color:pink;background-color:pink">



### Inline images

For externally-stored images (most will be stored on Tightbytes, for my pages)::

```
![Me](http://www.tightbytes.com/art/images/something/Chemise019.jpg){: align=left width=300 }
```

and for those stored with the data files::

```
![Celeste](images/C01-Aa.jpg){: align=left width=300 }
```

...or...

```
<figure>
  <img src="https://dummyimage.com/600x400/eee/aaa" width="300" />
  <figcaption>Image caption</figcaption>
</figure>
```
<hr style="height:2px;border-width:0;color:pink;background-color:pink">




### Embedded YouTube Video

This code for a remote link:

```
<video width="384" height="384" controls>
  <source src="https://tightbytes.com/videos/Celeste/C01Aaa.mp4" type="video/mp4">
</video>
```

...yields this:

<video width="384" height="384" controls>
  <source src="https://tightbytes.com/videos/Celeste/C01Aaa.mp4" type="video/mp4">
</video>

<hr style="height:2px;border-width:0;color:pink;background-color:pink">




This code for a local link:

```
<video width="480" height="480" controls>
  <source src="/assets/videos//C03.mp4" type="video/mp4">
</video>
```

...yields this:

<video width="480" height="480" controls>
  <source src="/assets/videos//C03.mp4" type="video/mp4">
</video>

<hr style="height:2px;border-width:0;color:pink;background-color:pink">




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


<hr style="height:2px;border-width:0;color:pink;background-color:pink">






### Non-youtube Video

This code:

```
<iframe width="560" height="315"    src="https://tightbytes.com/art/images/Cui/24/1750s/s02/LeRegarde01.mp4" frameborder="0"  allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"  allowfullscreen>
</iframe>
``` 

...produces:

<iframe width="560" height="315"    src="https://tightbytes.com/art/images/Cui/24/1750s/s02/LeRegarde01.mp4" frameborder="0"    allow="accelerometer; clipboard-write; encrypted-media; gyroscope; picture-in-picture"  allowfullscreen>
</iframe>
   


(Note to self: took out  [  autoplay; ] )

<hr style="height:2px;border-width:0;color:pink;background-color:pink">





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

<hr style="height:4px;border-width:0;color:pink;background-color:pink">






### HTML and CSS

Grid for two simple layouts:

<iframe width="560" height="315" src="https://www.youtube.com/embed/r1IitKbJRFE" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

<hr style="height:2px;border-width:0;color:pink;background-color:pink">




Slide Show:
   
<iframe width="560" height="315" src="https://www.youtube.com/embed/WJERnXiFFug" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

<hr style="height:2px;border-width:0;color:pink;background-color:pink">




[CSS stuff](https://ishadeed.com/article/conditional-css-has-nth-last-child/?utm_source=convertkit&utm_medium=email&utm_campaign=Why+people+use+CSS+frameworks%20-%2010872019)

[AstroDocs](https://docs.astro.build/en/editor-setup/)



<hr style="height:24px;border-width:0;color:pink;background-color:pink">

