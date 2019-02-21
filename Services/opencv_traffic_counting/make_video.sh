#!/usr/bin/env bash
ffmpeg -start_number 0 -framerate 15 -i /Users/abhinavrohilla/Downloads/out/processed_%04d.png -s:v 1920:1080 -c:v libx265 -profile:v high -crf 20 -pix_fmt yuv420p /Users/abhinavrohilla/Downloads/out/out.mp4
