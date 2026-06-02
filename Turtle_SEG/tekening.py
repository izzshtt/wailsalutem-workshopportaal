import turtle

scherm = turtle.Screen()
scherm.title("Mijn Turtle Tekening")
scherm.bgcolor("lightblue")

pen = turtle.Turtle()

def teken_rechthoek(x, y, breedte, hoogte, kleur):
    pen.penup()
    pen.goto(x, y)
    pen.pendown()
    pen.fillcolor(kleur)
    pen.begin_fill()

    for i in range(2):
        pen.forward(breedte)
        pen.left(90)
        pen.forward(hoogte)
        pen.left(90)

    pen.end_fill()

# gebouwen
teken_rechthoek(-200, -200, 80, 200, "gray")
teken_rechthoek(-100, -200, 80, 150, "darkgray")
teken_rechthoek(0, -200, 80, 250, "gray")

# ramen (gewoon handmatig, makkelijker!)
teken_rechthoek(-190, -150, 20, 30, "yellow")
teken_rechthoek(-150, -150, 20, 30, "yellow")

teken_rechthoek(-90, -150, 20, 30, "yellow")
teken_rechthoek(-50, -150, 20, 30, "yellow")

teken_rechthoek(10, -150, 20, 30, "yellow")
teken_rechthoek(50, -150, 20, 30, "yellow")

turtle.done()