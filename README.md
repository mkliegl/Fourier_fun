# Fun with the Fourier transform


## Images

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


## Audio

Trying the same trick with audio is a little more complicated. The
Fourier transform is nonlocal, but humans do not hear a whole song
at once. So in audio processing, instead of taking the Fourier transform
of the whole signal, it is common to break up the signal into short
time windows and do a Fourier transform on each of these windows.

A naive implementation of swapping magnitude and phase of two audio
files on such windows may be found in
[this Python script](swap_wav_mag_phase.py).
The results sound a little smoother using the
[Short-Time Fourier Transform][stft] (essentially: overlapping windows
and a more carefully designed filter than simply a rectangular indicator).
An implementation using [this Python stft package][stft-python] may
be found in [this Python script](swap_waf_mag_phase_stft.py).

The results are very window-size-dependent and are much harder to describe
than in the case of images,
but are still quite interesting and fun. I put some short examples in
the [speech][speech/] and [music][music/] folders.


## Audio sources and processing

* Carefree Kevin MacLeod (incompetech.com)  
Licensed under Creative Commons: By Attribution 3.0 License  
http://creativecommons.org/licenses/by/3.0/
* Gymnopedie No. 2 Kevin MacLeod (incompetech.com)  
Licensed under Creative Commons: By Attribution 3.0 License  
http://creativecommons.org/licenses/by/3.0/
* Address to the Women of America - Gloria Steinem  
https://ia802302.us.archive.org/10/items/Greatest_Speeches_of_the_20th_Century/AddresstotheWomenofAmerica_64kb.mp3  
Public domain
* Address to Congress - Hank Aaron  
https://ia802302.us.archive.org/10/items/Greatest_Speeches_of_the_20th_Century/AddresstoCongress-1974_64kb.mp3  
Public domain

These files were processed using [sox][sox]. See the
[music/music.sh](music/music.sh) and [speech/speech.sh](speech/speech.sh)
scripts for details.

## License

MIT. See the [LICENSE](LICENSE) file for more details.


[imidentify]: http://www.imagemagick.org/script/identify.php
[imconvert]: http://www.imagemagick.org/script/convert.php
[berkeleycourse]: http://robotics.eecs.berkeley.edu/~sastry/ee20/vision2/node6.html
[sox]: http://sox.sourceforge.net
[stft]: https://en.wikipedia.org/wiki/Short-time_Fourier_transform
[stft-python]: https://github.com/audiolabs/stft
