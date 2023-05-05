# Assignment 05 - CUDA


[![Python 3.10.6](https://img.shields.io/badge/python-3.10.6-blue.svg)](https://www.python.org/downloads/release/python-3106/)

## Table of contents
- [Quick start](#quick-start)
- [Assignment description](#assignment-description)
- [Grayscale conversion formula](#grayscale-conversion-formula)
- [Performance comparison](#performance-comparison)
- [Examples of converted images](#examples-of-converted-images)
  - [Example 1](#example-1)
  - [Example 2](#example-2)
  - [Example 3](#example-3)


## Quick start
Before running the script, perform the following steps:
1. Set python interpreter version to 3.10.x.
2. Install `Numba` module (`pip install numba`).
3. Install `matplotlib` module (`pip install matplotlib`).
4. If your system does not support CUDA, set `NUMBA_ENABLE_CUDASIM` to `1` in your environment variables.
5. Restart your IDE to make sure it has access to the latest environment variables.

## Assignment description
The purpose of this assignment is to implement image grayscale conversion and performance comparison using both CPU and GPU - Numba CUDA.

Dataset contains 114 images with `640x480` resolution.

Original images are located in `input_images` folder. Output images are situated in
`cpu_output_images` for the CPU and `gpu_output_images` for the GPU - CUDA.


## Grayscale conversion formula
I used the following formula `Y' = 0.2989 * R + 0.5870 * G + 0.1140 * B` [^1]


## Performance comparison

| CPU total   	 (sec) | CPU average (sec)	 | GPU total (sec)	 | GPU average (sec)	 |
|---------------------|--------------------|------------------|--------------------|
| 	    1.862582       | 	     0.016303     | 	  1.631593      | 	       0.014303   | 
| 	      1.912311     | 	  0,016774        | 	     1.672732   | 	 0,014673         |   	
| 	         1.833413  | 0,016082           | 	      1.594831  | 	0,013989          |   	

![image](https://user-images.githubusercontent.com/70724986/236536417-58e66f3d-2de9-4591-9996-2916f7df59d2.png) 

![image](https://user-images.githubusercontent.com/70724986/236536554-0087b203-feb1-47eb-a513-b2fcf8f22bab.png)


## Examples of converted images
Images were taken from https://www.pexels.com/sk-sk/.
### Example 1
![pexels-josh-hild-2422259](https://user-images.githubusercontent.com/70724986/236335507-a116c3e8-5bfa-4400-89f3-98bc6604988d.jpg) ![pexels-josh-hild-2422259](https://user-images.githubusercontent.com/70724986/236335413-06bc191b-0d82-4eb8-9ce4-b58881652a15.jpg)


### Example 2
![pexels-roberto-nickson-2631613](https://user-images.githubusercontent.com/70724986/236335716-c950827b-304d-4811-a3a8-6291bf7df3d3.jpg) ![pexels-roberto-nickson-2631613](https://user-images.githubusercontent.com/70724986/236335756-180beb0a-a022-4649-a707-f0f324de0c83.jpg)


### Example 3
![pexels-designecologist-1779487](https://user-images.githubusercontent.com/70724986/236336050-29881433-b17c-4282-bdc8-977e8d50ceae.jpg) ![pexels-designecologist-1779487](https://user-images.githubusercontent.com/70724986/236336082-0eb5c842-3267-45c8-937f-e2d1b911633d.jpg)


[^1]: https://stackoverflow.com/a/12201744
[^2]: https://chat.openai.com

