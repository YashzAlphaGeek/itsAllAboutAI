# Paper Flight Physics

This game is about **throwing a paper ball** into a bin. Here’s how it works:

---

## 1. What the game “sees”

The computer looks at 4 numbers to know what is happening:

1. **dx** → How far the bin is from the ball (left or right).
2. **dy** → How high the ball is from the ground.
3. **vx** → How fast the ball is moving sideways.
4. **vy** → How fast the ball is moving up or down.

> These numbers help the computer decide how to throw the ball.

---

## 2. What the computer can do

The computer can choose **two things** for each throw:

1. **Angle** – how high the ball will go:

   * Small angle → ball goes straight and low
   * Big angle → ball goes high in the air

2. **Power** – how strong the throw is:

   * Small power → ball doesn’t go far
   * Big power → ball goes far

> Together, angle + power decide the ball’s speed and path.

---

## 3. Scoring (Reward)

* **+1 point** → if the ball goes into the bin
* **-0.5 points** → if it misses

> This tells the computer whether it did a good throw or not.

---

## 4. How the ball moves

The ball moves like **a real thrown ball**:

1. **Gravity** pulls it down slowly.
2. **Frame time** is like taking tiny steps to update the ball’s position.
3. **Velocity** tells how fast the ball moves sideways (vx) and up/down (vy).

> Every tiny step:
>
> * Move sideways → add vx to x
> * Move up/down → add vy to y
> * Pull down → add gravity to vy

---

## 5. When the ball lands

* When the ball touches the ground, it stops moving.
* Then the computer can throw again.

---

## 6. Putting it all together

1. Computer looks at where the bin is.
2. Decides **angle** and **power**.
3. Converts that into sideways and up/down speed:

```text
vx = cos(angle) * power   # speed left-right
vy = -sin(angle) * power  # speed up
```

4. Each tiny step, move the ball:

```text
x = x + vx * time
y = y + vy * time
vy = vy + gravity * time
```

5. When ball hits the ground → check if it’s in the bin → give points.

> That’s it! The ball flies like in real life, just like throwing a paper ball in your room.
