"""
Impossible Hexagon - Python Turtle Tekening
Auteur: Ilija
"""

import turtle
import math


def bereken_hexagon_punten(centrum_x, centrum_y, radius, rotatie=0):
    """Bereken de 6 hoekpunten van een regelmatige zeshoek."""
    punten = []
    for i in range(6):
        hoek = math.radians(60 * i + rotatie)
        x = centrum_x + radius * math.cos(hoek)
        y = centrum_y + radius * math.sin(hoek)
        punten.append((x, y))
    return punten


def teken_hexagon(t, punten):
    """Teken een zeshoek door de gegeven punten te verbinden."""
    t.penup()
    t.goto(punten[0])
    t.pendown()
    for punt in punten[1:]:
        t.goto(punt)
    t.goto(punten[0])


def teken_spaken(t, centrum, punten):
    """Teken lijnen van het centrum naar elke hoek van de zeshoek."""
    for punt in punten:
        t.penup()
        t.goto(centrum)
        t.pendown()
        t.goto(punt)


def teken_verbindingen(t, punten_a, punten_b):
    """Teken lijnen tussen corresponderende punten van twee hexagonen."""
    for i in range(6):
        t.penup()
        t.goto(punten_a[i])
        t.pendown()
        t.goto(punten_b[i])


def main():
    scherm = turtle.Screen()
    scherm.setup(600, 650)
    scherm.title("Impossible Hexagon - Ilija")
    scherm.bgcolor("white")

    t = turtle.Turtle()
    t.speed(0)
    t.pencolor("#1a7aad")

    # Buitenste hexagon
    buiten_punten = bereken_hexagon_punten(0, 0, 200)
    t.pensize(3)
    teken_hexagon(t, buiten_punten)

    # Spaken van centrum naar buitenste hoeken
    teken_spaken(t, (0, 0), buiten_punten)

    # Middelste hexagon (30 graden gedraaid)
    midden_punten = bereken_hexagon_punten(0, 0, 140, rotatie=30)
    t.pensize(2)
    teken_hexagon(t, midden_punten)

    # Illusie-lijnen: buitenste hoek -> middelste hoek -> volgende buitenste hoek
    t.pensize(1)
    for i in range(6):
        t.penup()
        t.goto(buiten_punten[i])
        t.pendown()
        t.goto(midden_punten[i])
        t.goto(buiten_punten[(i + 1) % 6])

    # Binnenste hexagon
    binnen_punten = bereken_hexagon_punten(0, 0, 80)
    t.pensize(2)
    teken_hexagon(t, binnen_punten)

    # Verbindingen middelste naar binnenste hexagon
    t.pensize(1)
    teken_verbindingen(t, midden_punten, binnen_punten)

    # Titel onder de tekening
    t.penup()
    t.goto(0, -260)
    t.pendown()
    t.write("Impossible Hexagon", align="center",
            font=("Arial", 18, "bold"))

    t.hideturtle()
    scherm.exitonclick()


if __name__ == "__main__":
    main()
