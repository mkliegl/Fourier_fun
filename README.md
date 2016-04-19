# Fun with the Fourier transform

What happens when you switch the Fourier magnitudes of two pictures, while
leaving their phases intact? Are the pictures still recognizable? If so,
which is which? Is the magnitude or the phase more important to
human visual perception?

Have a look at this [Jupyter notebook](Fourier_fun.ipynb) to find out.


## Credit

I'm not sure whom to attribute this "parlor trick" to - it's been
around for a while and I've seen it in at least a couple of talks
by different people. The earliest reference I could find is
this [Berkeley course][berkeleycourse] from 1997, taught by
S. Shankar Sastry.


## Image sources and processing

- `Hillary_Clinton.jpg`: resized version of https://en.wikipedia.org/wiki/Hillary_Clinton#/media/File:Hillary_Clinton_official_Secretary_of_State_portrait_crop.jpg (public domain)
- `Bernie_Sanders.jpg`: https://en.wikipedia.org/wiki/Bernie_Sanders#/media/File:Bernie_Sanders.jpg (public domain)
- `frogs.jpg`: resized version of https://en.wikipedia.org/wiki/Frog#/media/File:Anoures.jpg (public domain)

Resized using the ImageMagick [identify][imidentify] and
[convert][imconvert] commands to the dimensions of `Bernie_Sanders.jpg`:

~~~ bash
DIMS=`identify -format '%wx%h!' Bernie_Sanders.jpg`
convert Hillary_Clinton_official_Secretary_of_State_portrait_crop.jpg \
    -resize $DIMS Hillary_Clinton.jpg
convert Anoures.jpg -resize $DIMS frogs.jpg
~~~


## License

MIT. See the [LICENSE](LICENSE) file for more details.


[imidentify]: http://www.imagemagick.org/script/identify.php
[imconvert]: http://www.imagemagick.org/script/convert.php
[berkeleycourse]: http://robotics.eecs.berkeley.edu/~sastry/ee20/vision2/node6.html
