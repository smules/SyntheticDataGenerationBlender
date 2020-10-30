# SyntheticDataGenerationBlender - LEGO
This is a Blender script with the sole purpose of mass producing Domain Randomized. The purpose is to train TensorFlow to identify LEGO pieces.

# Usage
First download generate_images.py. Open the .py file and configure it to your computer. Currently it is set for Linux, with the Linux filesystem format. You will also have to dowload the LDraw library, which a 3D model of every LEGO piece ever produced, and the loadldraw library, which enables you to load you LDraw files into Blender. <br />Note: loadldraw only works on Blender 2.79 and 2.81, so any new version of Blender is incompatable.
#### Finally, when you are ready to start the program, run in terminal or equivelant this command
```python
blender -P generate_images.py
```
# Results
Here are three images that show what is produced
![3003_0001](/images/3003_0001.png)
![3003_0002](/images/3003_0002.png)
![2339_0001](/images/2339_0001.png)
# Credits
[LDraw](https://www.ldraw.org/)<br />
[TobyLobster](https://github.com/TobyLobster) - creator of loadldraw<br />
[Dianiel West](https://twitter.com/JustASquid/) - helped point me to Domain Randomization<br />
The LEGO Group<br />
