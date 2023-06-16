#!/usr/bin/env bash
# compresses an image with name hero-1.jpg using imagemagick cli program
# sets the brightness of the image to -50 and the contrast as well to -50
mogrify -compress JPEG -quality 50 hero-1.jpg
convert -brightness-contrast -50x-50 hero-1.jpg hero-1.jpg
