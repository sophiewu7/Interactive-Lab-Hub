# Little Interactions Everywhere

**NAMES OF COLLABORATORS HERE**

[Sophie Wu(NetID: sw2298)](https://github.com/sophiewu7/Interactive-Lab-Hub/tree/Fall2023/Lab%206), [Annetta Zheng(jz2272)](https://github.com/annetta-zheng/Interactive-Lab-Hub/tree/Fall2023/Lab%206)

## Prep

1. Pull the new changes from the class interactive-lab-hub. (You should be familiar with this already!)
2. Install [MQTT Explorer](http://mqtt-explorer.com/) on your laptop. If you are using Mac, MQTT Explorer only works when installed from the [App Store](https://apps.apple.com/app/apple-store/id1455214828).
3. Readings before class:
   * [MQTT](#MQTT)
   * [The Presence Table](https://dl.acm.org/doi/10.1145/1935701.1935800) and [video](https://vimeo.com/15932020)


## Overview

The point of this lab is to introduce you to distributed interaction. We have included some Natural Language Processing (NLP) and Generation (NLG) but those are not really the emphasis. Feel free to dig into the examples and play around the code which you can integrate into your projects if wanted. However, we want to emphasize that the grading will focus on your ability to develop interesting uses for messaging across distributed devices. Here are the four sections of the lab activity:

A) [MQTT](#part-a)

B) [Send and Receive on your Pi](#part-b)

C) [Streaming a Sensor](#part-c)

D) [The One True ColorNet](#part-d)

E) [Make It Your Own](#part-)

## Part 1.

### Part A
### MQTT

MQTT is a lightweight messaging portal invented in 1999 for low bandwidth networks. It was later adopted as a defacto standard for a variety of [Internet of Things (IoT)](https://en.wikipedia.org/wiki/Internet_of_things) devices. 

#### The Bits

* **Broker** - The central server node that receives all messages and sends them out to the interested clients. Our broker is hosted on the far lab server (Thanks David!) at `farlab.infosci.cornell.edu/8883`. Imagine that the Broker is the messaging center!
* **Client** - A device that subscribes or publishes information to/on the network.
* **Topic** - The location data gets published to. These are *hierarchical with subtopics*. For example, If you were making a network of IoT smart bulbs this might look like `home/livingroom/sidelamp/light_status` and `home/livingroom/sidelamp/voltage`. With this setup, the info/updates of the sidelamp's `light_status` and `voltage` will be store in the subtopics. Because we use this broker for a variety of projects you have access to read, write and create subtopics of `IDD`. This means `IDD/ilan/is/a/goof` is a valid topic you can send data messages to.
*  **Subscribe** - This is a way of telling the client to pay attention to messages the broker sends out on the topic. You can subscribe to a specific topic or subtopics. You can also unsubscribe. Following the previouse example of home IoT smart bulbs, subscribing to `home/livingroom/sidelamp/#` would give you message updates to both the light_status and the voltage.
* **Publish** - This is a way of sending messages to a topic. Again, with the previouse example, you can set up your IoT smart bulbs to publish info/updates to the topic or subtopic. Also, note that you can publish to topics you do not subscribe to. 


**Important note:** With the broker we set up for the class, you are limited to subtopics of `IDD`. That is, to publish or subcribe, the topics will start with `IDD/`. Also, setting up a broker is not much work, but for the purposes of this class, you should all use the broker we have set up for you!


#### Useful Tooling

Debugging and visualizing what's happening on your MQTT broker can be helpful. We like [MQTT Explorer](http://mqtt-explorer.com/). You can connect by putting in the settings from the image below.


![input settings](imgs/mqtt_explorer.png?raw=true)


Once connected, you should be able to see all the messages under the IDD topic. , go to the **Publish** tab and try publish something! From the interface you can send and plot messages as well. Remember, you are limited to subtopics of `IDD`. That is, to publish or subcribe, the topics will start with `IDD/`.


<img width="1026" alt="Screen Shot 2022-10-30 at 10 40 32 AM" src="https://user-images.githubusercontent.com/24699361/198885090-356f4af0-4706-4fb1-870f-41c15e030aba.png">



### Part B
### Send and Receive on your Pi

[sender.py](./sender.py) and and [reader.py](./reader.py) show you the basics of using the mqtt in python. Let's spend a few minutes running these and seeing how messages are transferred and shown up. Before working on your Pi, keep the connection of `farlab.infosci.cornell.edu/8883` with MQTT Explorer running on your laptop.

**Running Examples on Pi**

* Install the packages from `requirements.txt` under a virtual environment:

  ```
  pi@raspberrypi:~/Interactive-Lab-Hub $ source circuitpython/bin/activate
  (circuitpython) pi@raspberrypi:~/Interactive-Lab-Hub $ cd Lab\ 6
  (circuitpython) pi@raspberrypi:~/Interactive-Lab-Hub/Lab 6 $ pip install -r requirements.txt
  ...
  ```
* Run `sender.py`, fill in a topic name (should start with `IDD/`), then start sending messages. You should be able to see them on MQTT Explorer.

  ```
  (circuitpython) pi@raspberrypi:~/Interactive-Lab-Hub/Lab 6 $ python sender.py
  >> topic: IDD/AlexandraTesting
  now writing to topic IDD/AlexandraTesting
  type new-topic to swich topics
  >> message: testtesttest
  ...
  ```
* Run `reader.py`, and you should see any messages being published to `IDD/` subtopics. Type a message inside MQTT explorer and see if you can receive it with `reader.py`.

  ```
  (circuitpython) pi@raspberrypi:~ Interactive-Lab-Hub/Lab 6 $ python reader.py
  ...
  ```

<img width="890" alt="Screen Shot 2022-10-30 at 10 47 52 AM" src="https://user-images.githubusercontent.com/24699361/198885135-a1d38d17-a78f-4bb2-91c7-17d014c3a0bd.png">


**\*\*\*Consider how you might use this messaging system on interactive devices, and draw/write down 5 ideas here.\*\*\***

![image](https://hackmd.io/_uploads/BkjlXQomp.png)

![image](https://hackmd.io/_uploads/HJgjXXjQp.png)

![image](https://hackmd.io/_uploads/By4hHmsma.png)

![IMG_6138.jpg](https://hackmd.io/_uploads/SySD8Xi7T.jpg)

![IMG_6139.jpg](https://hackmd.io/_uploads/rk_m_Xo7a.jpg)

### Part C
### Streaming a Sensor

We have included an updated example from [lab 4](https://github.com/FAR-Lab/Interactive-Lab-Hub/tree/Fall2021/Lab%204) that streams the [capacitor sensor](https://learn.adafruit.com/adafruit-mpr121-gator) inputs over MQTT. 

Plug in the capacitive sensor board with the Qwiic connector. Use the alligator clips to connect a Twizzler (or any other things you used back in Lab 4) and run the example script:

<p float="left">
<img src="https://cdn-learn.adafruit.com/assets/assets/000/082/842/large1024/adafruit_products_4393_iso_ORIG_2019_10.jpg" height="150" />
<img src="https://cdn-shop.adafruit.com/970x728/4210-02.jpg" height="150">
<img src="https://cdn-learn.adafruit.com/guides/cropped_images/000/003/226/medium640/MPR121_top_angle.jpg?1609282424" height="150"/>
<img src="https://media.discordapp.net/attachments/679721816318803975/823299613812719666/PXL_20210321_205742253.jpg" height="150">
</p>


 ```
 (circuitpython) pi@raspberrypi:~ Interactive-Lab-Hub/Lab 6 $ python distributed_twizzlers_sender.py
 ...
 ```

**\*\*\*Include a picture of your setup here: what did you see on MQTT Explorer?\*\*\***


![lab6-partc](https://hackmd.io/_uploads/ByHcw0c7p.jpg)


![image](https://hackmd.io/_uploads/Hk0ivAqQp.png)


![447abb44e454cfdfded53f3f03547ff](https://hackmd.io/_uploads/BydhDRcm6.png)


**\*\*\*Pick another part in your kit and try to implement the data streaming with it.\*\*\***

Script located at `distributed_keyborard_sender.py`.


![Image_20231109170612](https://hackmd.io/_uploads/ryKWOA9Qa.jpg)


![a4c8c67029aa2874d4e6de211bc0049](https://hackmd.io/_uploads/Bk8CPCc7T.png)


![015b25d7199db2a264b97b2239ebf89](https://hackmd.io/_uploads/ry1AvRqQ6.png)


### Part D
### The One True ColorNet

It is with great fortitude and resilience that we shall worship at the altar of the *OneColor*. Through unity of the collective RGB, we too can find unity in our heart, minds and souls. With the help of machines, we can overthrow the bourgeoisie, get on the same wavelength (this was also a color pun) and establish [Fully Automated Luxury Communism](https://en.wikipedia.org/wiki/Fully_Automated_Luxury_Communism).

The first step on the path to *collective* enlightenment, plug the [APDS-9960 Proximity, Light, RGB, and Gesture Sensor](https://www.adafruit.com/product/3595) into the [MiniPiTFT Display](https://www.adafruit.com/product/4393). You are almost there!

<p float="left">
  <img src="https://cdn-learn.adafruit.com/assets/assets/000/082/842/large1024/adafruit_products_4393_iso_ORIG_2019_10.jpg" height="150" />
  <img src="https://cdn-shop.adafruit.com/970x728/4210-02.jpg" height="150">
  <img src="https://cdn-shop.adafruit.com/970x728/3595-03.jpg" height="150">
</p>


The second step to achieving our great enlightenment is to run `color.py`. We have talked about this sensor back in Lab 2 and Lab 4, this script is similar to what you have done before! Remember to activate the `circuitpython` virtual environment you have been using during this semester before running the script:

 ```
 (circuitpython) pi@raspberrypi:~ Interactive-Lab-Hub/Lab 6 $ systemctl stop mini-screen.service
 (circuitpython) pi@raspberrypi:~ Interactive-Lab-Hub/Lab 6 $ python color.py
 ...
 ```

By running the script, wou will find the two squares on the display. Half is showing an approximation of the output from the color sensor. The other half is up to the collective. Press the top button to share your color with the class. Your color is now our color, our color is now your color. We are one.

(A message from the previous TA, Ilan: I was not super careful with handling the loop so you may need to press more than once if the timing isn't quite right. Also, I haven't load-tested it so things might just immediately break when everyone pushes the button at once.)

**\*\*\*Can you set up the script that can read the color anyone else publish and display it on your screen?\*\*\***

Please refer to `msgcolor.py` for the code.

Please see the videos: `color_change_part1` and `color_change_part2` for the demo.

Video Folder: https://drive.google.com/drive/u/2/folders/1hbvnUMJ-cx8DhAtAyXRFDosOQR1tiwWC

<!-- <img src="./imgs/partc_img0.jpg" width="200"/>
<img src="./imgs/partc_img1.jpg" width="200"/>
<img src="./imgs/partc_img2.jpg" width="200"/>
<img src="./imgs/partc_img3.jpg" width="200"/>
<img src="./imgs/partc_img4.jpg" width="200"/> -->
![partc_img0.jpg](https://hackmd.io/_uploads/r1vtPJomp.jpg =x200) ![partc_img1.jpg](https://hackmd.io/_uploads/BkHFPysXp.jpg =x200)
![partc_img2.jpg](https://hackmd.io/_uploads/rJKdvyi76.jpg =x200) ![partc_img3.jpg](https://hackmd.io/_uploads/B1IuP1imp.jpg =x200) ![partc_img4.jpg](https://hackmd.io/_uploads/BJDDvJiX6.jpg =x200)

In the demo, we showed the process of changing the starter color: **light pink** with the published rgba messages with "GREEN" and "BLUE". 

The **light pink** color is gradually mixed into **pink** with "GREEN", then to **light purple** with "BLUE" messages.



### Part E
### Make it your own

Find at least one class (more are okay) partner, and design a distributed application together based on the exercise we asked you to do in this lab.

**\*\*\*1. Explain your design\*\*\*** 

Our design is a remote tarot card reading application. 

It allows users to have their fortunes told in various aspects of life, such as career, love, or family, without being in the same physical location as the tarot reader. 

The interaction is conducted over a digital platform using MQTT protocol to communicate between two users: the player and the tarot reader. 

The player/user can pick cards virtually, and the tarot reader interprets each card by sending audio back to the user. 

This system can cater to people interested in tarot readings but are unable to visit a reader in person due to distance, time constraints, or current health guidelines.

**\*\*\*2. Diagram the architecture of the system.\*\*\*** Be clear to document where input, output and computation occur, and label all parts and connections. For example, where is the banana, who is the banana player, where does the sound get played, and who is listening to the banana music?
![IMG_6134.jpg](https://hackmd.io/_uploads/HJ16eXoQ6.jpg)


![image](https://hackmd.io/_uploads/rJqzymoQT.png)


![image](https://hackmd.io/_uploads/HJ4SeQsQT.png)


**\*\*\*3. Build a working prototype of the system.\*\*\*** 

We build interface so that the user is very clear about how to use the device.

Player Interaction Parts:
![IMG_6128.JPG](https://hackmd.io/_uploads/rkO-G7sXa.jpg)
![IMG_6129.JPG](https://hackmd.io/_uploads/S1bLG7o7T.jpg)

Tarot Reader Interation Parts:
Please refer to `tarot_reader.py` for code of the reader side.
![IMG_6130.jpg](https://hackmd.io/_uploads/ryhqfmjXa.jpg)


**\*\*\*4. Document the working prototype in use.\*\*\*** 


Click to view the video:

[<img src="https://hackmd.io/_uploads/B1nNufsmT.jpg">](https://youtu.be/p0TKXzx_ljs)


<!--**\*\*\*5. BONUS (Wendy didn't approve this so you should probably ignore it)\*\*\*** get the whole class to run your code and make your distributed system BIGGER.-->

