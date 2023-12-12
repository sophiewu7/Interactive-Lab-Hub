# Final Project

**COLLABORATORS**
[Sophie Wu(NetID: sw2298)](https://github.com/sophiewu7/Interactive-Lab-Hub/tree/Fall2023/Lab%206), [Annetta Zheng(jz2272)](https://github.com/annetta-zheng/Interactive-Lab-Hub/tree/Fall2023/Lab%206)

## Project Plan

### Big Idea

LuminArt is a captivating and interactive art installation designed to enhance any space in your home. This unique piece consists of a multi-layered acrylic canvas, beautifully illuminated by interactive LED lights. It features six distinct acrylic layers, each encased in responsive LED lighting. Equipped with a joystick and a rotor, these components collaborate to seamlessly shift the layers, producing a dynamic, evolving visual spectacle as people engage with the artwork. LuminArt offers a personalized and immersive artistic experience, transforming ordinary spaces into extraordinary environments.

The installation showcases the possibilities of merging traditional artistic mediums with cutting-edge technology. It serves as an example of how innovation can enhance and redefine our understanding of art.

### Timeline

**Week 1:** Conceptualization and design planning. Acquire materials (acrylic boards, LED strips). Idea Pitched.
**Week 2:** Build the physical prototype and test basic functionality. 
**Week 3:** Use laser cutting to create designs on layers of the acrylic boards and refine the LED circuit based on test results. Functional checkoff.
**Week 4:** Final assembly, documentation, and video creation.

### Parts Needed

- [Raspberry Pi 4](https://www.raspberrypi.com/products/raspberry-pi-4-model-b/) (including SD card, power supply)
- Acrylic Sheet (18" x 24", 3mm thick)
- Wooden Board (18" x 24", 3mm thick)
- [SparkFun Qwiic Joystick](https://www.sparkfun.com/products/15168)
- [Adafruit I2C Stemma QT Rotary Encoder](https://www.adafruit.com/product/4991#technical-details)
- [Adafruit NeoPixel Digital RGB LED Strip](https://www.adafruit.com/product/1138)
- [I2C to NeoPixel Driver](https://learn.adafruit.com/adafruit-neodriver-i2c-to-neopixel-driver?view=all)
- [Female DC Power adapter](https://www.adafruit.com/product/368?gad_source=1&gclid=CjwKCAiAvdCrBhBREiwAX6-6UnZKKB3bTjMZxsHz2mxgq-S5J0xOsKOXSIHElIoT9Pwy33I_f0OquBoCasAQAvD_BwE)


### Fall-back plan

Start with 1 layer where we would try out the visibility of LED light on the design by using laser cutting.
    
In case of technical difficulties or budget constraints, simplify the design while maintaining the core interactive concept.
    
## Functioning Project:
![4681702164780_.pic](https://hackmd.io/_uploads/BJ1w-ofIa.jpg)

![cd8ee8c7e9d88f7f1fa467944c55792](https://hackmd.io/_uploads/ByXVXDGUa.jpg)

![1520ddae79f31bcfc300a8b73854004](https://hackmd.io/_uploads/Sk18mvzLa.jpg)

![543449697fef13ea0e346096992f1d5](https://hackmd.io/_uploads/SJ0vmvMUp.jpg)

The user can interact with the device by the following ways:
1. Turn the joystick to change the LED light to the desired color
2. Press the joystic (acts as a button) to swicth between light patterns
3. Turn the rotary encoder to change the speed of light movement

Detailed interactions can be viewed through the [video](https://youtu.be/3wqJpvPEugU) in the Video section.

## Design Process

### Prototyping

We started our project by doing laser cut training at the Maker Lab for week 1.

We first try out the feasibility of the output of our design: using lights to show only one layer of acrylic layers.

We first cut out 6 acrylic layers with a geometry design we found on the internet, each has a size of 2 inches * 2 inches.

![image](https://hackmd.io/_uploads/B1-64vMI6.png)

![image](https://hackmd.io/_uploads/BkopVvzLp.png)

By using the flashlight of our phone, we confirmed the feasibility of our project and decided to move forward with the original idea.

Our next step was figuring out how to use the LED light strip. We sought help from Hauk and got the light strip to work in week 2.

### Box Design

![image](https://hackmd.io/_uploads/ByKGKwM8a.png)

We also use wooden board to create a holder for the 2 inches * 2 inches prototype in week 2.

By having the output working, in week 3, the team worked on figuring out how to add interaction to our project and what should we do for the final design (i. e., what would be the size of LuminArt and what would be our theme, how can we design our holder box).

The team met up to discuss these detail and we agreed to move forward with:
- Each layer has a size of 3 inches by 4 inches with a 2 inches wide portion at the botton where we can use to clip it on to our box
- We will have the theme of sea life / marine life
- The user can interact with the device in the following ways:
    - change pattern
    - change color
    - change speed

Then we started to implement each part.

We started by finding vectors of sea life on the internet, designed them onto the 6 layers of acrylic. And cut them out using laser cutting at the Maker Lab.

Then we designed a box using boxes.py template with Adobe Illustrator. Because the template didn't match we wanted so we first use paper to cut out the design to make sure we have all the right meaurement before we cut on the actual wooden board.

With all the parts maded, we decided to use 4 LED pixel per row. We counted the index of these LEDs and started our coding process.

### Code

See `final_project.py` for details.
Step 1: Have control over LED lights
Step 2: Have the joystick connected and implement color change feature
Step 3: Have the rotary encoder connected to change the spped of light
Step 4: Design light patterns and use joystick as a button to switch the pattern.


## Video

[Video on YouTube](https://www.youtube.com/watch?v=3wqJpvPEugU)

[![6d4a68c4601e7bae80bc19661c42aac](https://hackmd.io/_uploads/HyU_dvGIa.jpg)](https://www.youtube.com/watch?v=3wqJpvPEugU)


## Work Distribution
Evenly divided between the two members.
    
## Appendix

INSPIRATION
![Screenshot 2023-11-13 at 23.15.16](https://hackmd.io/_uploads/Hk0AN_l46.jpg)

- http://www.publicspacedesign.com/article/741
- http://www.publicspacedesign.com/article/601
- http://www.publicspacedesign.com/article/621
- http://www.publicspacedesign.com/article/619

