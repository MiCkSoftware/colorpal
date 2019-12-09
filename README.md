# Colorpal
CLI Tool to help with color harmonics (triadic, tetradic,...)

```
$ colorpal --help
usage: colorpal [-h] [-y]
                [color]
                [{comp,triadic,tetradic,mono,analog,splitcomp,info,gui}]

Color harmonics tool

positional arguments:
  color                 Hex color (eg #ffffff) or - to read clipboard
  {comp,triadic,tetradic,mono,analog,splitcomp,info,gui}
                        Harmonic to compute

optional arguments:
  -h, --help            show this help message and exit
  -y, --ryb             Use RYB colorspace

$ colorpal 1144dd 
#1144dd
rgb:(0.06666666666666667, 0.26666666666666666, 0.8666666666666667)
hsv:(225.0, 0.9230769230769231, 0.8666666666666667)
hsl:(225.0, 0.8571428571428572, 0.4666666666666667)
2664K

$ colorpal 1144dd comp --ryb
#dda611

$ colorpal 1144dd comp --ryb | colorpal - comp
#1148dd

$ colorpal 1144dd tetradic
#aa11dd
#ddaa11
#44dd11

$ colorpal 1144dd gui
```
![Sample](/colorpalette.png)


## Getting Started

### Prerequisites

This python script requires the following libraries:

```
Pillow
Grapefruit
pyperclip (optional)
```

### Installing

The script can sit anywhere. Move it to a directoty in path for more convenience. 

```
cp colorpal /usr/local/bin/
```

Check everything is OK by running the script. Eg:

```
colorpal ff00ff
```

## Author

* **MiCk Sodtware** - *Initial work* - [MiCkSoftware](https://github.com/MiCkSoftware)

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

Check my website: https://sites.google.com/view/micksoftware/home

## License

This project is licensed under the GNU GENERAL PUBLIC LICENSE - see the [LICENSE.md](LICENSE.md) file for details


