import turtle

class StarHexagon:
    def __init__(robin, kleur="cyan", grootte=100):
        robin.kleur = kleur
        robin.grootte = grootte
        robin.t = turtle.Turtle()
        robin.t.speed(0)
        robin.t.width(15)
        robin.t.color(robin.kleur)

    def draw_star(robin):
        for i in range(6):
            robin.t.penup()
            robin.t.goto(0, 0)
            robin.t.setheading(i * 60)
            robin.t.pendown()
            robin.t.forward(robin.grootte)

    def draw_hexagon(robin):
        robin.t.penup()
        robin.t.goto(0, 0)
        robin.t.setheading(0)
        robin.t.forward(robin.grootte)
        robin.t.right(120)
        robin.t.pendown()

        for i in range(6):
            robin.t.forward(robin.grootte)
            robin.t.right(60)

    
    def draw(robin):
        robin.draw_star()
        robin.draw_hexagon()

tekening = StarHexagon(kleur="cyan", grootte=100)
tekening.draw()

turtle.done()