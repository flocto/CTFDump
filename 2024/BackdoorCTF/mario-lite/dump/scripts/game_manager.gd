extends Node

var score = 0
var death = 0
@onready var score_label = $Control / ScoreLabel

func add_point():
	score += 1
	score_label.text = "Coins: " + str(score)

func death_count():
	death = 1
